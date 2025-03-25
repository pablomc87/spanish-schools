import pytest
from aioresponses import aioresponses

from src.scrapers.list_scraper import ListScraper


@pytest.mark.asyncio
async def test_scrape_school_list_success(sample_schools_html):
    """Test successful scraping of school list."""
    with aioresponses() as m:
        # Mock the response
        m.post(
            "https://www.educacion.gob.es/centros/buscarCentros",
            body=sample_schools_html,
            headers={"Content-Type": "text/html; charset=utf-8"},
        )

        scraper = ListScraper()
        result = await scraper.run()

        # Verify the results match our anonymized data
        assert len(result) == 4
        assert result[0] == "00000001"
        assert result[1] == "00000002"
        assert result[2] == "00000003"
        assert result[3] == "00000004"


@pytest.mark.asyncio
async def test_scrape_school_list_empty():
    """Test scraping when no schools are found."""
    empty_html = """
    <!DOCTYPE html>
    <html>
    <body>
        <table>
            <thead>
                <tr>
                    <th>Provincia</th>
                    <th>Localidad</th>
                    <th>Denominación Genérica</th>
                    <th>Denominación Específica</th>
                    <th>Código</th>
                    <th>Naturaleza</th>
                    <th>&nbsp;</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    </body>
    </html>
    """

    with aioresponses() as m:
        # Mock empty response
        m.post(
            "https://www.educacion.gob.es/centros/buscarCentros",
            body=empty_html,
            headers={"Content-Type": "text/html; charset=utf-8"},
        )

        scraper = ListScraper()
        result = await scraper.run()
        assert len(result) == 0


@pytest.mark.asyncio
async def test_scrape_school_list_error():
    """Test error handling during scraping."""
    with aioresponses() as m:
        # Mock error response
        m.post(
            "https://www.educacion.gob.es/centros/buscarCentros",
            status=500,
            body="Internal Server Error",
            headers={"Content-Type": "text/plain"},
        )

        scraper = ListScraper()
        with pytest.raises(Exception):
            await scraper.run()


@pytest.mark.asyncio
async def test_scrape_school_list_retry(sample_schools_html):
    """Test retry mechanism on temporary failures."""
    with aioresponses() as m:
        # Mock temporary failure then success
        m.post(
            "https://www.educacion.gob.es/centros/buscarCentros",
            status=503,
            body="Service Unavailable",
            headers={"Content-Type": "text/plain"},
        )
        m.post(
            "https://www.educacion.gob.es/centros/buscarCentros",
            body=sample_schools_html,
            headers={"Content-Type": "text/html; charset=utf-8"},
        )

        scraper = ListScraper()
        result = await scraper.run()

        # Verify the results match our anonymized data
        assert len(result) == 4
        assert result[0] == "00000001"
        assert result[1] == "00000002"
        assert result[2] == "00000003"
        assert result[3] == "00000004"


@pytest.mark.asyncio
async def test_scrape_school_list_malformed():
    """Test handling of malformed HTML response."""
    malformed_html = """
    <!DOCTYPE html>
    <html>
    <body>
        <table>
            <thead>
                <tr>
                    <th>Wrong Headers</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>No school data</td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>
    """

    with aioresponses() as m:
        # Mock malformed response
        m.post(
            "https://www.educacion.gob.es/centros/buscarCentros",
            body=malformed_html,
            headers={"Content-Type": "text/html; charset=utf-8"},
        )

        scraper = ListScraper()
        result = await scraper.run()
        assert len(result) == 0  # Should handle malformed HTML gracefully


@pytest.mark.asyncio
async def test_scrape_school_list_no_tables():
    """Test handling of response with no tables."""
    no_tables_html = """
    <!DOCTYPE html>
    <html>
    <body>
        <div>No tables in this response</div>
    </body>
    </html>
    """

    with aioresponses() as m:
        # Mock response with no tables
        m.post(
            "https://www.educacion.gob.es/centros/buscarCentros",
            body=no_tables_html,
            headers={"Content-Type": "text/html; charset=utf-8"},
        )

        scraper = ListScraper()
        result = await scraper.run()
        assert len(result) == 0  # Should handle HTML with no tables gracefully
