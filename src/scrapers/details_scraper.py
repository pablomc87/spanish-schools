import asyncio
from typing import Dict, List, Optional

from loguru import logger

from .base_scraper import BaseScraper


class DetailsScraper(BaseScraper):
    """Scraper for school details from the education ministry website."""

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.educacion.gob.es/centros/detalleCentro"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            ),
        }

    def _build_payload(self, school_id: str) -> Dict[str, str]:
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
            "tipoCentro": "0",
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
                headers=self.headers,
            )

            logger.debug(f"Successfully scraped school {school_id}")
            return content

        except Exception as e:
            logger.error(f"Error processing school {school_id}: {str(e)}")
            return None

    async def process_batch(self, school_ids: List[str]) -> Dict[str, str]:
        """
        Process a batch of schools concurrently.

        Returns:
            Dictionary mapping school IDs to their HTML content
        """
        async with self:  # This will create and close the aiohttp session
            tasks = [self.scrape_school(school_id) for school_id in school_ids]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            return {
                school_id: result
                for school_id, result in zip(school_ids, results)
                if isinstance(result, str)
            }

    async def run(self, school_ids: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Main entry point for the scraper.

        Args:
            school_ids: List of school IDs to scrape.

        Returns:
            Dictionary mapping school IDs to their HTML content
        """
        if not school_ids:
            school_ids = []

        try:
            total_schools = len(school_ids)
            logger.info(f"Starting to scrape {total_schools} schools")

            all_results = {}
            all_results = await self.process_batch(school_ids)

            logger.success(
                f"Successfully processed {len(all_results)} "
                f"out of {total_schools} schools"
            )
            return all_results

        except Exception as e:
            logger.error(f"Error in scraper: {str(e)}")
            raise
