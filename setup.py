from setuptools import setup, find_packages

setup(
    name="spanish-schools",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.9.3",
        "pyyaml>=6.0",
        "requests==2.31.0",
        "SQLAlchemy>=1.4.0",
        "aiosqlite==0.19.0",
        "python-dotenv==1.0.1",
        "lxml>=4.9.0",
        "tqdm==4.66.2",
        "loguru>=0.6.0",
        "aiofiles==23.2.1",
    ],
    extras_require={
        "dev": [
            "semantic-release>=8.7.2",
        ],
    },
    python_requires=">=3.11",
) 