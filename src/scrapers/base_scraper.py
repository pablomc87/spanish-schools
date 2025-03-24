import asyncio
from typing import Any, Dict, Optional

import aiohttp
from loguru import logger

from config.config import config


class BaseScraper:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.config = config
        self.semaphore = asyncio.Semaphore(config.scraping.max_concurrent_requests)

    async def __aenter__(self) -> "BaseScraper":
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any],
    ) -> None:
        if self.session:
            await self.session.close()

    async def _make_request(
        self,
        url: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> str:
        """Make an HTTP request with retry logic."""
        if not self.session:
            raise RuntimeError(
                "Session not initialized. Use async with context manager."
            )

        async with self.semaphore:
            for attempt in range(self.config.scraping.retry_attempts):
                try:
                    async with self.session.request(
                        method=method,
                        url=url,
                        data=data,
                        headers=headers,
                        timeout=self.config.scraping.request_timeout,
                    ) as response:
                        response.raise_for_status()
                        return await response.text()

                except aiohttp.ClientError as e:
                    logger.warning(
                        f"Request failed (attempt {attempt + 1}/"
                        f"{self.config.scraping.retry_attempts}): {str(e)}"
                    )
                    if attempt + 1 == self.config.scraping.retry_attempts:
                        raise
                    await asyncio.sleep(self.config.scraping.retry_delay)

            raise RuntimeError("Max retry attempts reached")
