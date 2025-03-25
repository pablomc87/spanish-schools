from typing import Union

from bs4 import BeautifulSoup
from loguru import logger


class BaseParser:
    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, "lxml")

    def _extract_text(self, selector: str, default: str = "") -> str:
        """Extract text from an element using a CSS selector."""
        try:
            element = self.soup.select_one(selector)
            if element is None:
                return default
            return element.text.strip()
        except Exception as e:
            logger.warning(
                f"Error extracting text with selector '{selector}': {str(e)}"
            )
            return default

    def _extract_attribute(
        self, selector: str, attribute: str, default: Union[str, list[str]] = ""
    ) -> Union[str, list[str]]:
        """Extract an attribute from an element using a CSS selector."""
        try:
            element = self.soup.select_one(selector)
            if element is None:
                return default
            value = element[attribute]
            if isinstance(value, str):
                return value.strip()
            return value
        except Exception as e:
            logger.warning(
                f"Error extracting attribute '{attribute}' with selector "
                f"'{selector}': {str(e)}"
            )
            return default

    def _extract_all_text(self, selector: str) -> list[str]:
        """Extract text from all elements matching a CSS selector."""
        try:
            elements = self.soup.select(selector)
            return [
                element.text.strip() for element in elements if element.text.strip()
            ]
        except Exception as e:
            logger.warning(
                f"Error extracting all text with selector '{selector}': {str(e)}"
            )
            return []

    def _extract_table_data(self, table_selector: str) -> list[dict[str, str]]:
        """Extract data from a table into a list of dictionaries."""
        try:
            table = self.soup.select_one(table_selector)
            if not table:
                return []

            headers = []
            for th in table.select("th"):
                headers.append(th.text.strip().lower().replace(" ", "_"))

            rows = []
            for tr in table.select("tr"):
                row_data = {}
                cells = tr.select("td")
                if cells and len(cells) == len(headers):
                    for header, cell in zip(headers, cells):
                        row_data[header] = cell.text.strip()
                    rows.append(row_data)

            return rows
        except Exception as e:
            logger.warning(
                f"Error extracting table data with selector "
                f"'{table_selector}': {str(e)}"
            )
            return []
