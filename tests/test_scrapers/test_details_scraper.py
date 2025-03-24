import pytest
from aioresponses import aioresponses
from src.scrapers.details_scraper import DetailsScraper

@pytest.mark.asyncio
async def test_scrape_school_success():
    """Test successful scraping of school details."""
    with aioresponses() as m:
        # Mock the response
        m.post(
            "https://www.educacionyfp.gob.es/servicios-al-ciudadano/catalogo/centros-educativos/centros-educativos.html",
            payload={"html": "<div>Test School Details</div>"}
        )
        
        scraper = DetailsScraper()
        html_content = await scraper.scrape_school("123456")
        
        assert html_content == "<div>Test School Details</div>"

@pytest.mark.asyncio
async def test_scrape_school_not_found():
    """Test scraping when school is not found."""
    with aioresponses() as m:
        # Mock not found response
        m.post(
            "https://www.educacionyfp.gob.es/servicios-al-ciudadano/catalogo/centros-educativos/centros-educativos.html",
            status=404,
            payload={"error": "School not found"}
        )
        
        scraper = DetailsScraper()
        with pytest.raises(Exception):
            await scraper.scrape_school("123456")

@pytest.mark.asyncio
async def test_scrape_school_error():
    """Test error handling during scraping."""
    with aioresponses() as m:
        # Mock error response
        m.post(
            "https://www.educacionyfp.gob.es/servicios-al-ciudadano/catalogo/centros-educativos/centros-educativos.html",
            status=500,
            payload={"error": "Internal Server Error"}
        )
        
        scraper = DetailsScraper()
        with pytest.raises(Exception):
            await scraper.scrape_school("123456")

@pytest.mark.asyncio
async def test_scrape_school_retry():
    """Test retry mechanism on temporary failures."""
    with aioresponses() as m:
        # Mock temporary failure then success
        m.post(
            "https://www.educacionyfp.gob.es/servicios-al-ciudadano/catalogo/centros-educativos/centros-educativos.html",
            status=503,
            payload={"error": "Service Unavailable"}
        )
        m.post(
            "https://www.educacionyfp.gob.es/servicios-al-ciudadano/catalogo/centros-educativos/centros-educativos.html",
            payload={"html": "<div>Test School Details</div>"}
        )
        
        scraper = DetailsScraper()
        html_content = await scraper.scrape_school("123456")
        
        assert html_content == "<div>Test School Details</div>"

@pytest.mark.asyncio
async def test_process_batch():
    """Test processing a batch of school IDs."""
    with aioresponses() as m:
        # Mock responses for multiple schools
        for school_id in ["123456", "789012"]:
            m.post(
                "https://www.educacionyfp.gob.es/servicios-al-ciudadano/catalogo/centros-educativos/centros-educativos.html",
                payload={"html": f"<div>School {school_id} Details</div>"}
            )
        
        scraper = DetailsScraper()
        results = await scraper.process_batch(["123456", "789012"])
        
        assert len(results) == 2
        assert results["123456"] == "<div>School 123456 Details</div>"
        assert results["789012"] == "<div>School 789012 Details</div>" 