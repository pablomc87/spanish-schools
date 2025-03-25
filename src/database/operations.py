from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config.config import config

from .models import Base, ImpartedStudy, School


class DatabaseManager:
    def __init__(self):
        # Convert SQLite URL to async
        db_url = config.database.url.replace("sqlite:///", "sqlite+aiosqlite:///")

        self.engine = create_async_engine(db_url, echo=config.database.echo)
        self.SessionLocal = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            expire_on_commit=False,
        )

    async def create_tables(self) -> None:
        """Create all database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self) -> None:
        """Drop all database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session."""
        session = self.SessionLocal()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def save_school(
        self, school_data: Dict[str, Any], session: Optional[AsyncSession] = None
    ) -> School:
        """Save or update a school and its imparted studies."""
        should_close_session = False
        if session is None:
            session = self.SessionLocal()
            should_close_session = True

        try:
            # Extract imparted studies data
            imparted_studies_data = school_data.pop("imparted_studies", [])
            school_id = school_data["id"]

            # Create or update school
            school = await session.get(School, school_id)
            if school is None:
                school = School(**school_data)
                session.add(school)
            else:
                for key, value in school_data.items():
                    setattr(school, key, value)

            # Handle imparted studies
            # First, clear existing relationships
            school.imparted_studies = []

            # Then add or update studies
            for study_data in imparted_studies_data:
                # Try to find an existing study with the same attributes
                stmt = select(ImpartedStudy).where(
                    ImpartedStudy.name == study_data["name"],
                    ImpartedStudy.degree == study_data["degree"],
                    ImpartedStudy.family == study_data["family"],
                    ImpartedStudy.modality == study_data["modality"],
                )
                result = await session.execute(stmt)
                study = result.scalars().first()

                if study is None:
                    # Create new study if it doesn't exist
                    study = ImpartedStudy(**study_data)
                    session.add(study)

                # Add the study to the school's imparted_studies
                school.imparted_studies.append(study)

            if should_close_session:
                await session.commit()
            return school

        except Exception as e:
            if should_close_session:
                await session.rollback()
            raise e

        finally:
            if should_close_session:
                await session.close()

    async def get_school_by_id(self, school_id: str) -> Optional[School]:
        """Get a school by its ID."""
        async with self.get_session() as session:
            return await session.get(School, school_id)

    async def get_all_schools(self) -> Any:
        """Get all schools."""
        async with self.get_session() as session:
            result = await session.execute(School.__table__.select())
            return result.scalars().all()

    async def get_school_imparted_studies(self, school_id: str) -> Any:
        """Get all imparted studies for a school."""
        async with self.get_session() as session:
            result = await session.execute(
                ImpartedStudy.__table__.select().where(
                    ImpartedStudy.schools.any(School.id == school_id)
                )
            )
            return result.scalars().all()


# Global database manager instance
db = DatabaseManager()
