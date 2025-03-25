import os
from pathlib import Path

import pytest

from config.config import Config, DatabaseConfig
from src.database.operations import DatabaseManager


@pytest.fixture
def test_config(test_db_path):
    """Create a test configuration."""
    return Config(config_path=None)


@pytest.fixture
def test_db_path(tmp_path):
    """Create a temporary database path."""
    return str(tmp_path / "test.db")


@pytest.fixture
async def test_db(test_db_path, monkeypatch):
    """Create a test database and return its path."""
    # Create test config with test database
    test_config = Config(config_path=None)
    test_config.database = DatabaseConfig(url=f"sqlite:///{test_db_path}", echo=False)

    # Patch the global config
    monkeypatch.setattr("config.config.config", test_config)

    # Create database manager with test config
    db = DatabaseManager()
    await db.create_tables()

    yield db

    # Cleanup
    await db.engine.dispose()
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


@pytest.fixture
def sample_school_html():
    """Load sample school HTML for testing."""
    html_path = Path(__file__).parent / "fixtures" / "school.html"
    return html_path.read_text()


@pytest.fixture
def sample_schools_html():
    """Load sample schools list HTML for testing."""
    html_path = Path(__file__).parent / "fixtures" / "schools.html"
    return html_path.read_text()
