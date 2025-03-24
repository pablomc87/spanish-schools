from typing import Optional, Any
from bs4 import BeautifulSoup
from loguru import logger


class BaseParser:
    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, 'lxml')

    def _extract_text(self, selector: str, default: Any = "") -> str:
        """Extract text from an element using a CSS selector."""
        try:
            element = self.soup.select_one(selector)
            return element.text.strip() if element else default
        except Exception as e:
            logger.warning(f"Error extracting text with selector '{selector}': {str(e)}")
            return default

    def _extract_attribute(self, selector: str, attribute: str, default: Any = "") -> str:
        """Extract an attribute from an element using a CSS selector."""
        try:
            element = self.soup.select_one(selector)
            return element[attribute].strip() if element else default
        except Exception as e:
            logger.warning(f"Error extracting attribute '{attribute}' with selector '{selector}': {str(e)}")
            return default

    def _extract_all_text(self, selector: str) -> list[str]:
        """Extract text from all elements matching a CSS selector."""
        try:
            elements = self.soup.select(selector)
            return [element.text.strip() for element in elements if element.text.strip()]
        except Exception as e:
            logger.warning(f"Error extracting all text with selector '{selector}': {str(e)}")
            return []

    def _extract_table_data(self, table_selector: str) -> list[dict[str, str]]:
        """Extract data from a table into a list of dictionaries."""
        try:
            table = self.soup.select_one(table_selector)
            if not table:
                return []

            headers = []
            for th in table.select('th'):
                headers.append(th.text.strip().lower().replace(' ', '_'))

            rows = []
            for tr in table.select('tr'):
                row_data = {}
                cells = tr.select('td')
                if cells and len(cells) == len(headers):
                    for header, cell in zip(headers, cells):
                        row_data[header] = cell.text.strip()
                    rows.append(row_data)

            return rows
        except Exception as e:
            logger.warning(f"Error extracting table data with selector '{table_selector}': {str(e)}")
            return [] 