from pathlib import Path

import pytest
from aioresponses import aioresponses

from src.scrapers.details_scraper import DetailsScraper


@pytest.fixture
def school_html():
    """Load the school HTML fixture."""
    fixture_path = Path(__file__).parent.parent / "fixtures" / "school.html"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.mark.asyncio
async def test_scrape_school_success(school_html):
    """Test successful scraping of school details."""
    with aioresponses() as m:
        m.post(
            "https://www.educacion.gob.es/centros/detalleCentro",
            body=school_html,
            status=200,
            headers={"Content-Type": "text/html"},
        )

        async with DetailsScraper() as scraper:
            result = await scraper.scrape_school("123456")
            assert result is not None
            assert result == school_html


@pytest.mark.asyncio
async def test_scrape_school_not_found():
    """Test scraping when school is not found."""
    with aioresponses() as m:
        m.post(
            "https://www.educacion.gob.es/centros/detalleCentro",
            status=404,
            body="Not Found",
        )

        async with DetailsScraper() as scraper:
            result = await scraper.scrape_school("999999")
            assert result is None


@pytest.mark.asyncio
async def test_scrape_school_server_error():
    """Test scraping when server returns an error."""
    with aioresponses() as m:
        m.post(
            "https://www.educacion.gob.es/centros/detalleCentro",
            status=500,
            body="Internal Server Error",
        )

        async with DetailsScraper() as scraper:
            result = await scraper.scrape_school("123456")
            assert result is None


@pytest.mark.asyncio
async def test_scrape_school_network_error():
    """Test scraping when network error occurs."""
    with aioresponses() as m:
        m.post(
            "https://www.educacion.gob.es/centros/detalleCentro",
            exception=Exception("Network Error"),
        )

        async with DetailsScraper() as scraper:
            result = await scraper.scrape_school("123456")
            assert result is None


@pytest.mark.asyncio
async def test_process_batch_success(school_html):
    """Test processing a batch of schools successfully."""
    school_ids = ["123456", "789012"]

    with aioresponses() as m:
        for school_id in school_ids:
            m.post(
                "https://www.educacion.gob.es/centros/detalleCentro",
                body=school_html,
                status=200,
                headers={"Content-Type": "text/html"},
            )

        async with DetailsScraper() as scraper:
            results = await scraper.process_batch(school_ids)

            assert len(results) == 2
            for school_id in school_ids:
                assert school_id in results
                assert results[school_id] == school_html


@pytest.mark.asyncio
async def test_process_batch_partial_failure(school_html):
    """Test processing a batch where some schools fail."""
    school_ids = ["123456", "789012", "999999"]

    with aioresponses() as m:
        # First school succeeds
        m.post(
            "https://www.educacion.gob.es/centros/detalleCentro",
            body=school_html,
            status=200,
            headers={"Content-Type": "text/html"},
        )
        # Second school fails with 404
        m.post(
            "https://www.educacion.gob.es/centros/detalleCentro",
            status=404,
            body="Not Found",
        )
        # Third school fails with network error
        m.post(
            "https://www.educacion.gob.es/centros/detalleCentro",
            exception=Exception("Network Error"),
        )

        async with DetailsScraper() as scraper:
            results = await scraper.process_batch(school_ids)

            assert len(results) == 1
            assert "123456" in results
            assert results["123456"] == school_html
            assert "789012" not in results
            assert "999999" not in results
