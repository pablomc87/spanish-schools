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
            soup = BeautifulSoup(html_content, 'lxml')
            school_ids = []
            
            # Find the results table
            table = soup.find('table', {'class': 'table table-hover table-sm'})
            if not table:
                logger.warning("No results table found in the response")
                return []
            
            # Find the index of the "Código" column
            headers = table.find_all('th')
            codigo_index = None
            for i, header in enumerate(headers):
                if 'Código' in header.text:
                    codigo_index = i
                    break
            
            if codigo_index is None:
                logger.warning("No 'Código' column found in the table")
                return []
            
            # Process each row in the table
            for i, row in enumerate(table.find_all('tr')[1:], 1):  # Skip header row
                cells = row.find_all('td')
                if len(cells) > codigo_index:
                    school_id = cells[codigo_index].text.strip()
                    if school_id:
                        school_ids.append(school_id)
                        # Log progress every 500 schools
                        if len(school_ids) % 500 == 0:
                            logger.info(f"Processed {len(school_ids)} schools...")
            
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