import json
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# Association table for the many-to-many relationship
school_studies = Table(
    "school_studies",
    Base.metadata,
    Column("school_id", String, ForeignKey("schools.id"), primary_key=True),
    Column("study_id", Integer, ForeignKey("imparted_studies.id"), primary_key=True),
)


class TimestampMixin:
    created_at: Mapped[str] = mapped_column(
        String, default=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        default=lambda: datetime.now(timezone.utc).isoformat(),
        onupdate=lambda: datetime.now(timezone.utc).isoformat(),
    )


class School(Base, TimestampMixin):
    __tablename__ = "schools"

    id: Mapped[str] = mapped_column(
        String, primary_key=True
    )  # School code from the website
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String)
    fax: Mapped[Optional[str]] = mapped_column(String)
    email: Mapped[Optional[str]] = mapped_column(String)
    website: Mapped[Optional[str]] = mapped_column(String)

    # Location info
    autonomous_community: Mapped[Optional[str]] = mapped_column(String)
    province: Mapped[Optional[str]] = mapped_column(String)
    country: Mapped[Optional[str]] = mapped_column(String)
    region: Mapped[Optional[str]] = mapped_column(String)
    sub_region: Mapped[Optional[str]] = mapped_column(String)
    municipality: Mapped[Optional[str]] = mapped_column(String)
    locality: Mapped[Optional[str]] = mapped_column(String)
    address: Mapped[Optional[str]] = mapped_column(String)
    postal_code: Mapped[Optional[str]] = mapped_column(String)

    # Classification info
    nature: Mapped[Optional[str]] = mapped_column(String)  # Public, Private, etc.
    is_concerted: Mapped[Optional[str]] = mapped_column(String)
    center_type: Mapped[Optional[str]] = mapped_column(String)
    generic_name: Mapped[Optional[str]] = mapped_column(String)

    # Additional info stored as JSON arrays
    _services: Mapped[Optional[str]] = mapped_column(
        "services", Text
    )  # Store as JSON string

    @property
    def services(self) -> List[str]:
        if self._services:
            return json.loads(self._services)
        return []

    @services.setter
    def services(self, value: List[str]):
        if value is not None:
            self._services = json.dumps(value, ensure_ascii=False)
        else:
            self._services = None

    # Many-to-many relationship with ImpartedStudy
    imparted_studies: Mapped[List["ImpartedStudy"]] = relationship(
        "ImpartedStudy", secondary=school_studies, back_populates="schools"
    )


class ImpartedStudy(Base, TimestampMixin):
    __tablename__ = "imparted_studies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Study details
    degree: Mapped[Optional[str]] = mapped_column(
        String
    )  # e.g., "Ciclos Formativos de FP de Grado Medio"
    family: Mapped[Optional[str]] = mapped_column(String)  # e.g., "SANIDAD"
    name: Mapped[str] = mapped_column(
        String, nullable=False
    )  # e.g., "Cuidados Auxiliares de Enfermería"
    modality: Mapped[Optional[str]] = mapped_column(
        String
    )  # e.g., "Diurno", "Vespertino", "Virtual"

    # Many-to-many relationship with School
    schools: Mapped[List["School"]] = relationship(
        "School", secondary=school_studies, back_populates="imparted_studies"
    )
