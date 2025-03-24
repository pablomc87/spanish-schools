# Spanish Schools Scraper

A Python-based scraper for collecting information about Spanish schools from the Ministry of Education's website.

## Features

- Scrapes school information from the Ministry of Education's website
- Stores data in SQLite database
- Handles pagination and concurrent requests
- Supports incremental updates (only scrapes new schools)
- Parses detailed school information including:
  - Basic information (name, code, contact details)
  - Location information
  - Classification (public/private, type)
  - Services
  - Imparted studies

## Requirements

- Python 3.8+
- SQLite3
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pablomc87/spanish-schools.git
cd schools
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Scraping New Schools

To scrape only new schools that aren't in the database:
```bash
python main.py --action scrape
```

### Force Update All Schools

To update all schools, even if they exist in the database:
```bash
python main.py --action scrape --force-update
```

### Reset Database

To reset the database (drop and recreate all tables):
```bash
python main.py --action reset-db
```

## Configuration

The project uses a YAML configuration file (`config/config.yml`) for various settings:
- API endpoints and default payload
- Database connection
- Scraping parameters (concurrent requests, timeouts, retries)
- Logging configuration

## Project Structure

```
schools/
├── config/
│   ├── config.py
│   └── config.yml
├── data/
│   └── raw/          # Raw HTML files
├── logs/             # Log files
├── src/
│   ├── database/
│   │   ├── models.py
│   │   └── operations.py
│   ├── managers/
│   │   └── school_manager.py
│   ├── parsers/
│   │   ├── base_parser.py
│   │   └── details_parser.py
│   └── scrapers/
│       ├── base_scraper.py
│       ├── details_scraper.py
│       └── list_scraper.py
├── main.py
├── parse_all.py
└── requirements.txt
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
