from typing import List, Optional, Set
from loguru import logger
from sqlalchemy import select

from ..database.operations import db
from ..database.models import School
from ..parsers.details_parser import DetailsParser
from ..scrapers.details_scraper import DetailsScraper

class SchoolManager:
    def __init__(self):
        self.scraper = DetailsScraper()
        
    async def get_existing_school_ids(self) -> Set[str]:
        """Get all school IDs that are already in the database."""
        async with db.get_session() as session:
            result = await session.execute(select(School.id))
            return {row[0] for row in result}
    
    async def scrape_and_parse(self, school_ids: List[str], batch_size: int = 10) -> None:
        """
        Scrape and parse schools, storing them in the database.
        
        Args:
            school_ids: List of school IDs to process
            batch_size: Number of schools to process in each batch
        """
        # Get the HTML content for all schools
        html_contents = await self.scraper.run(school_ids, batch_size=batch_size)
        
        # Parse and save each school
        for school_id, html_content in html_contents.items():
            try:
                # Parse the HTML content
                parser = DetailsParser(html_content)
                school_data = parser.parse_all()
                
                # Save to database
                await db.save_school(school_data)
                logger.debug(f"Successfully processed and saved school {school_id}")
                
            except Exception as e:
                logger.error(f"Error processing school {school_id}: {str(e)}")
    
    async def process_new_schools(self, school_ids: List[str], batch_size: int = 10) -> None:
        """
        Process only schools that don't exist in the database.
        
        Args:
            school_ids: List of school IDs to check and potentially process
            batch_size: Number of schools to process in each batch
        """
        existing_ids = await self.get_existing_school_ids()
        new_ids = [id for id in school_ids if id not in existing_ids]
        
        if new_ids:
            logger.info(f"Found {len(new_ids)} new schools to process")
            await self.scrape_and_parse(new_ids, batch_size)
        else:
            logger.info("No new schools to process")
    
    async def process_all_schools(self, school_ids: List[str], batch_size: int = 10) -> None:
        """
        Process all schools regardless of whether they exist in the database.
        
        Args:
            school_ids: List of school IDs to process
            batch_size: Number of schools to process in each batch
        """
        logger.info(f"Processing {len(school_ids)} schools")
        await self.scrape_and_parse(school_ids, batch_size) 