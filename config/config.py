import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Union

import yaml


@dataclass
class APIConfig:
    base_url: str
    details_url: str
    default_payload: Dict[str, str]


@dataclass
class DatabaseConfig:
    url: str
    echo: bool = False


@dataclass
class StorageConfig:
    raw_data_path: Path
    processed_data_path: Path


@dataclass
class ScrapingConfig:
    max_concurrent_requests: int
    request_timeout: int
    retry_attempts: int
    retry_delay: int


@dataclass
class LoggingConfig:
    level: str
    format: str
    file: Path


class Config:
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        if config_path is None:
            config_path = Path(__file__).parent / "config.yml"
        elif isinstance(config_path, str):
            config_path = Path(config_path)

        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)

        self.api = APIConfig(
            base_url=config_data["api"]["base_url"],
            details_url=config_data["api"]["details_url"],
            default_payload=config_data["api"]["default_payload"],
        )

        # Get database URL from environment variable or use default from config
        db_url = os.getenv("DATABASE_URL", config_data["database"]["url"])
        self.database = DatabaseConfig(
            url=db_url,
            echo=config_data["database"].get("echo", False),
        )

        self.storage = StorageConfig(
            raw_data_path=Path(config_data["storage"]["raw_data_path"]),
            processed_data_path=Path(config_data["storage"]["processed_data_path"]),
        )

        self.scraping = ScrapingConfig(
            max_concurrent_requests=config_data["scraping"]["max_concurrent_requests"],
            request_timeout=config_data["scraping"]["request_timeout"],
            retry_attempts=config_data["scraping"]["retry_attempts"],
            retry_delay=config_data["scraping"]["retry_delay"],
        )

        self.logging = LoggingConfig(
            level=config_data["logging"]["level"],
            format=config_data["logging"]["format"],
            file=Path(config_data["logging"]["file"]),
        )

    def ensure_directories(self) -> None:
        """Create all necessary directories if they don't exist."""
        directories = [
            self.storage.raw_data_path,
            self.storage.processed_data_path,
            self.logging.file.parent,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Global config instance
config = Config()
