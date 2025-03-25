from typing import Any, Dict, List, cast

from bs4 import Tag
from loguru import logger

from .base_parser import BaseParser


class DetailsParser(BaseParser):
    def parse_basic_info(self) -> Dict[str, str]:
        """Parse basic school information."""
        try:
            return {
                "id": self._extract_text(
                    'div.col-md-6:-soup-contains("Código de centro:") span'
                ),
                "name": self._extract_text(
                    'div.col-md-6:-soup-contains("Denominación específica:") span'
                ),
                "phone": self._extract_text(
                    'div.col-md-6:-soup-contains("Teléfono:") span'
                ),
                "fax": self._extract_text('div.col-md-6:-soup-contains("Fax:") span'),
                "email": self._extract_text(
                    'div.col-md-6:-soup-contains("Correo electrónico:") span'
                ),
                "website": self._extract_text(
                    'div.col-md-6:-soup-contains("Página Web del centro:") a'
                ),
            }
        except Exception as e:
            logger.warning(f"Error parsing basic info: {str(e)}")
            return {}

    def parse_location_info(self) -> Dict[str, str]:
        """Parse school location information."""
        try:
            return {
                "autonomous_community": self._extract_text(
                    'div.col-md-6:-soup-contains("Autonomía:") span'
                ),
                "province": self._extract_text(
                    'div.col-md-6:-soup-contains("Provincia:") span'
                ),
                "country": self._extract_text(
                    'div.col-md-6:-soup-contains("País:") span'
                ),
                "region": self._extract_text(
                    'div.col-md-6:-soup-contains("Comarca:") span'
                ),
                "sub_region": self._extract_text(
                    'div.col-md-6:-soup-contains("Sub.Provincial / Isla:") span'
                ),
                "municipality": self._extract_text(
                    'div.col-md-6:-soup-contains("Municipio:") span'
                ),
                "locality": self._extract_text(
                    'div.col-md-6:-soup-contains("Localidad:") span'
                ),
                "address": self._extract_text(
                    'div.col-md-6:-soup-contains("Domicilio:") span'
                ),
                "postal_code": self._extract_text(
                    'div.col-md-6:-soup-contains("Código postal:") span'
                ),
            }
        except Exception as e:
            logger.warning(f"Error parsing location info: {str(e)}")
            return {}

    def parse_classification_info(self) -> Dict[str, str]:
        """Parse school classification information."""
        try:
            return {
                "nature": self._extract_text(
                    'div.col-md-6:-soup-contains("Naturaleza:") span'
                ),
                "is_concerted": self._extract_text(
                    'div.col-md-6:-soup-contains("Concertado:") span'
                ),
                "center_type": self._extract_text(
                    'div.col-md-6:-soup-contains("Tipo de centro:") span'
                ),
                "generic_name": self._extract_text(
                    'div.col-md-6:-soup-contains("Denominación genérica:") span'
                ),
            }
        except Exception as e:
            logger.warning(f"Error parsing classification info: {str(e)}")
            return {}

    def parse_services(self) -> List[str]:
        """Parse school services."""
        try:
            services = []
            # First try to find the services section by looking for the header text
            services_header = self.soup.find(
                string=lambda t: t and "Servicios complementarios" in t
            )
            if not services_header:
                logger.debug("No services section found")
                return []

            # Find the closest table after the header
            parent_div = services_header.find_parent("div")
            if not parent_div:
                logger.debug("No parent div found for services header")
                return []

            table = parent_div.find_next("table")
            if not table:
                logger.debug("No services table found")
                return []

            # Extract services from table rows
            table_tag = cast(Tag, table)
            rows = cast(List[Tag], table_tag.find_all("tr"))
            for row in rows:
                td = row.find("td")
                if td:
                    # Get the text and normalize it to ensure proper encoding
                    service = td.get_text(strip=True)
                    if service:
                        services.append(service)
                        logger.debug(f"Found service: {service}")

            if services:
                logger.debug(f"Found {len(services)} services: {services}")
            else:
                logger.debug("No services found in table")
            return services

        except Exception as e:
            logger.warning(f"Error parsing services: {str(e)}")
            return []

    def parse_imparted_studies(self) -> List[Dict[str, str]]:
        """Parse imparted studies information."""
        try:
            studies = []
            # Look for the studies section by text content
            studies_header = self.soup.find(
                string=lambda t: t and "Enseñanzas impartidas" in t
            )
            if not studies_header:
                logger.debug("No studies section found")
                return []

            # Find the closest table after the header
            parent_div = studies_header.find_parent("div")
            if not parent_div:
                logger.debug("No parent div found for studies header")
                return []

            table = parent_div.find_next("table")
            if not table:
                logger.debug("No table found")
                return []

            # Process all rows
            table_tag = cast(Tag, table)
            rows = cast(List[Tag], table_tag.find_all("tr"))
            for row in rows:
                cells = cast(List[Tag], row.find_all("td"))
                if len(cells) >= 4:  # We expect at least 4 columns
                    study = {
                        "degree": cells[0].text.strip(),
                        "family": cells[1].text.strip(),
                        "name": cells[2].text.strip(),
                        "modality": cells[3].text.strip(),
                    }
                    # Add if there's a valid study name
                    if study["name"]:
                        studies.append(study)
                        logger.debug(f"Found study: {study}")

            if studies:
                logger.debug(f"Found {len(studies)} studies: {studies}")
            else:
                logger.debug("No studies found in table")
            return studies

        except Exception as e:
            logger.warning(f"Error parsing imparted studies: {str(e)}")
            return []

    def parse_all(self) -> Dict[str, Any]:
        """Parse all school information."""
        try:
            basic_info = self.parse_basic_info()
            if not basic_info.get(
                "id"
            ):  # If we can't get the basic info, something is wrong
                raise ValueError("Could not parse basic school information")

            return {
                **basic_info,
                **self.parse_location_info(),
                **self.parse_classification_info(),
                "services": self.parse_services(),
                "imparted_studies": self.parse_imparted_studies(),
            }
        except Exception as e:
            logger.error(f"Error parsing school details: {str(e)}")
            # Return a minimal valid structure instead of raising
            return {"id": None, "name": None, "services": [], "imparted_studies": []}
