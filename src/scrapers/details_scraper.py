import sqlite3
import requests
from concurrent.futures import ThreadPoolExecutor
import os
from typing import Optional, List, Dict, Any
from loguru import logger
import asyncio

from .base_scraper import BaseScraper

class DetailsScraper(BaseScraper):
    """Scraper for school details from the education ministry website."""
    
    def __init__(self):
        super().__init__()
        self.base_url = 'https://www.educacion.gob.es/centros/detalleCentro'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    
    def _build_payload(self, school_id: str) -> dict:
        """Build the payload for the request."""
        return {
            "codCentro": school_id,
            "idComunidad": "00",
            "idProvincia": "00",
            "nivel": "0",
            "naturaleza": "0",
            "concertado": "",
            "familia": "0",
            "ensenanza": "0",
            "modalidad": "0",
            "tipoCentro": "0"
        }
    
    async def scrape_school(self, school_id: str) -> Optional[str]:
        """
        Scrape details for a specific school.
        
        Args:
            school_id: The ID of the school to scrape.
            
        Returns:
            The HTML content of the school details page if successful, None otherwise.
        """
        try:
            logger.debug(f"Scraping school {school_id}")
            payload = self._build_payload(school_id)
            content = await self._make_request(
                url=self.base_url,
                method="POST",
                data=payload,
                headers=self.headers
            )
            
            logger.debug(f"Successfully scraped school {school_id}")
            return content
            
        except Exception as e:
            logger.error(f"Error processing school {school_id}: {str(e)}")
            return None
    
    async def process_batch(self, school_ids: List[str]) -> Dict[str, Optional[str]]:
        """
        Process a batch of schools concurrently.
        
        Returns:
            Dictionary mapping school IDs to their HTML content
        """
        async with self:  # This will create and close the aiohttp session
            tasks = [self.scrape_school(school_id) for school_id in school_ids]
            results = await asyncio.gather(*tasks)
            return {school_id: content for school_id, content in zip(school_ids, results) if content is not None}
    
    async def run(self, school_ids: List[str], batch_size: Optional[int] = None) -> Dict[str, str]:
        """
        Main entry point for the scraper.
        
        Args:
            school_ids: List of school IDs to scrape.
            batch_size: Optional number of schools to process in one batch.
                       If None, process all schools at once.
                       
        Returns:
            Dictionary mapping school IDs to their HTML content
        """
        try:
            total_schools = len(school_ids)
            logger.info(f"Starting to scrape {total_schools} schools")
            
            all_results = {}
            if batch_size:
                # Process schools in batches
                for i in range(0, total_schools, batch_size):
                    batch = school_ids[i:i + batch_size]
                    logger.debug(f"Processing batch {i//batch_size + 1} ({len(batch)} schools)")
                    batch_results = await self.process_batch(batch)
                    all_results.update(batch_results)
                    logger.debug(f"Completed batch {i//batch_size + 1}")
            else:
                # Process all schools at once
                all_results = await self.process_batch(school_ids)
            
            logger.success(f"Successfully processed {len(all_results)} out of {total_schools} schools")
            return all_results
            
        except Exception as e:
            logger.error(f"Error in scraper: {str(e)}")
            raise