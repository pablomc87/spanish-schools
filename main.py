import argparse
import asyncio
import sys

from loguru import logger

from src.database.operations import db
from src.managers.school_manager import SchoolManager
from src.scrapers.list_scraper import ListScraper


async def reset_database():
    """Drop and recreate all database tables."""
    logger.info("Dropping all tables...")
    await db.drop_tables()
    logger.info("Creating new tables...")
    await db.create_tables()
    logger.info("Database reset complete!")


async def scrape_school_list() -> list[str]:
    """Scrape the list of school IDs."""
    scraper = ListScraper()
    school_ids = await scraper.run()
    logger.info(f"Found {len(school_ids)} schools")
    return school_ids


async def main():
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
        "| <level>{level: <8}</level> "
        "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:"
        "<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True,
    )

    parser = argparse.ArgumentParser(description="School data scraper and parser")
    parser.add_argument(
        "--action",
        type=str,
        required=True,
        choices=["scrape", "reset-db"],
        help="Action to perform: 'scrape' to process schools, "
        "'reset-db' to reset the database",
    )
    parser.add_argument(
        "--workers", type=int, default=10, help="Number of worker processes for parsing"
    )
    parser.add_argument(
        "--force-update",
        action="store_true",
        help="Force update of all schools, even if they exist in database",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Update logging level if debug flag is set
    if args.debug:
        logger.remove()  # Remove previous handler
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
            "| <level>{level: <8}</level> "
            "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:"
            "<cyan>{line}</cyan> - <level>{message}</level>",
            level="DEBUG",
            colorize=True,
        )
        logger.debug("Debug logging enabled")

    if args.action == "reset-db":
        await reset_database()
        return

    # For scraping action
    manager = SchoolManager()
    school_ids = await scrape_school_list()

    if args.force_update:
        # Update all schools regardless of whether they exist
        await manager.process_all_schools(school_ids, batch_size=args.workers)
    else:
        # Only process new schools (default behavior)
        await manager.process_new_schools(school_ids, batch_size=args.workers)


if __name__ == "__main__":
    asyncio.run(main())
