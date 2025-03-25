# Schools Scraper

A Python-based scraper for educational institutions data.

## Development Workflow

### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch for features
- Feature branches: `feature/*`
- Bug fix branches: `fix/*`
- Release branches: `release/*`

### Development Process
1. Create a new branch from `develop`:
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

3. Push your changes:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request to merge into `develop`

### Pre-commit Hooks
The repository uses pre-commit framework for Git hooks. The following hooks are configured:
- `pytest`: Runs all tests before each commit
- `black`: Formats Python code
- `isort`: Sorts Python imports
- `flake8`: Checks Python code style

To set up pre-commit hooks:
```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install
```

To run hooks manually:
```bash
pre-commit run --all-files
```

### Running Tests
```bash
pytest
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for public functions and classes
- Keep functions focused and small

### Commit Messages
Follow conventional commits format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for code style changes
- `refactor:` for code refactoring
- `test:` for adding or modifying tests
- `chore:` for maintenance tasks

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
