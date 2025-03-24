from typing import List
from bs4 import BeautifulSoup
from loguru import logger

from .base_scraper import BaseScraper

class ListScraper(BaseScraper):
    """Scraper for getting the list of all schools from the education ministry website."""
    
    def __init__(self):
        super().__init__()
        self.base_url = 'https://www.educacion.gob.es/centros/buscarCentros'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    
    def _build_payload(self) -> dict:
        """Build the payload for the request to get all schools."""
        return {
            "ssel_natur": "0",  # All types (public, private, etc.)
            "comboprov": "00",  # All provinces
            "comboens": "0",    # All education levels
            "nombreCentro": "",  # No specific name filter
            "tipocentro": "0",  # All center types
            "combofami": "0",   # All families
            "combomodalidad": "0",  # All modalities
            "selectRegCap": "0",  # All regions/capitals
            "codprov": "00",    # All provinces (again)
            "combopais": "0",   # Spain
            "submitBuscar": "Buscar"  # Search button
        }
    
    async def _extract_school_ids(self, html_content: str) -> List[str]:
        """Extract school IDs from the search results page."""
        try:
            logger.debug(f"Processing HTML content with length: {len(html_content)}")
            soup = BeautifulSoup(html_content, 'lxml')
            school_ids = []
            
            # Find all tables in the document
            tables = soup.find_all('table')
            logger.debug(f"Found {len(tables)} tables in the HTML")
            
            # Search for the right table with school data
            school_table = None
            codigo_index = None
            
            for table in tables:
                # Look for the header row with "Código"
                headers = table.select('th')
                if not headers:
                    continue
                    
                for i, header in enumerate(headers):
                    header_text = header.get_text(strip=True)
                    if 'Código' in header_text or 'Código' in header_text:
                        school_table = table
                        codigo_index = i
                        logger.debug(f"Found school table with 'Código' in column {i}")
                        break
                
                if school_table:
                    break
            
            if not school_table:
                logger.warning("No table with school data found in the response")
                return []
            
            if codigo_index is None:
                logger.warning("Could not determine which column contains the school codes")
                return []
            
            # Extract rows from the table (skip header rows)
            rows = school_table.select('tbody tr')
            logger.debug(f"Found {len(rows)} rows in the school table")
            
            for row in rows:
                cells = row.select('td')
                if len(cells) > codigo_index:
                    school_id = cells[codigo_index].get_text(strip=True)
                    if school_id:
                        school_ids.append(school_id)
                        logger.debug(f"Extracted school ID: {school_id}")
                        # Log progress every 500 schools
                        if len(school_ids) % 500 == 0:
                            logger.info(f"Processed {len(school_ids)} schools...")
            
            logger.info(f"Extracted {len(school_ids)} school IDs")
            return school_ids
            
        except Exception as e:
            logger.error(f"Error extracting school IDs: {str(e)}")
            return []
    
    async def run(self) -> List[str]:
        """
        Main entry point for the scraper.
        
        Returns:
            List of school IDs found in the search results.
        """
        try:
            logger.info("Starting to fetch list of schools...")
            
            async with self:  # This will create and close the aiohttp session
                # Make the initial search request
                content = await self._make_request(
                    url=self.base_url,
                    method="POST",
                    data=self._build_payload(),
                    headers=self.headers
                )
                
                # Extract school IDs from the response
                school_ids = await self._extract_school_ids(content)
            
            logger.success(f"Successfully found {len(school_ids)} schools")
            return school_ids
            
        except Exception as e:
            logger.error(f"Error in list scraper: {str(e)}")
            raise 