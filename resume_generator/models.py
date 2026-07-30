"""Pydantic models for the JSON Resume schema."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Profile(BaseModel):
    network: str | None = None
    username: str | None = None
    url: str | None = None
    model_config = {"extra": "allow"}


class Location(BaseModel):
    address: str | None = None
    postalCode: str | None = None
    city: str | None = None
    countryCode: str | None = None
    region: str | None = None
    model_config = {"extra": "allow"}


class Basics(BaseModel):
    name: str | None = None
    label: str | None = None
    image: str | None = None
    email: str | None = None
    phone: str | None = None
    url: str | None = None
    summary: str | None = None
    location: Location | None = None
    profiles: list[Profile] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class Work(BaseModel):
    name: str | None = None
    location: str | None = None
    description: str | None = None
    position: str | None = None
    url: str | None = None
    startDate: str | None = None
    endDate: str | None = None
    summary: str | None = None
    highlights: list[str] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class Volunteer(BaseModel):
    organization: str | None = None
    position: str | None = None
    url: str | None = None
    startDate: str | None = None
    endDate: str | None = None
    summary: str | None = None
    highlights: list[str] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class Education(BaseModel):
    institution: str | None = None
    url: str | None = None
    area: str | None = None
    studyType: str | None = None
    startDate: str | None = None
    endDate: str | None = None
    score: str | None = None
    courses: list[str] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class Award(BaseModel):
    title: str | None = None
    date: str | None = None
    awarder: str | None = None
    summary: str | None = None
    model_config = {"extra": "allow"}


class Certificate(BaseModel):
    name: str | None = None
    date: str | None = None
    url: str | None = None
    issuer: str | None = None
    model_config = {"extra": "allow"}


class Publication(BaseModel):
    name: str | None = None
    publisher: str | None = None
    releaseDate: str | None = None
    url: str | None = None
    summary: str | None = None
    model_config = {"extra": "allow"}


class Skill(BaseModel):
    name: str | None = None
    level: str | None = None
    keywords: list[str] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class Language(BaseModel):
    language: str | None = None
    fluency: str | None = None
    model_config = {"extra": "allow"}


class Interest(BaseModel):
    name: str | None = None
    keywords: list[str] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class Reference(BaseModel):
    name: str | None = None
    reference: str | None = None
    model_config = {"extra": "allow"}


class Project(BaseModel):
    name: str | None = None
    description: str | None = None
    highlights: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    startDate: str | None = None
    endDate: str | None = None
    url: str | None = None
    roles: list[str] = Field(default_factory=list)
    entity: str | None = None
    type: str | None = None
    model_config = {"extra": "allow"}


class Meta(BaseModel):
    canonical: str | None = None
    version: str | None = None
    lastModified: str | None = None
    language: str | None = None  # BCP 47 tag; drives renderer labels (see i18n)
    model_config = {"extra": "allow"}


class Resume(BaseModel):
    basics: Basics | None = None
    work: list[Work] = Field(default_factory=list)
    volunteer: list[Volunteer] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    awards: list[Award] = Field(default_factory=list)
    certificates: list[Certificate] = Field(default_factory=list)
    publications: list[Publication] = Field(default_factory=list)
    skills: list[Skill] = Field(default_factory=list)
    languages: list[Language] = Field(default_factory=list)
    interests: list[Interest] = Field(default_factory=list)
    references: list[Reference] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    meta: Meta | None = None
    model_config = {"extra": "allow"}


# All sections that can be filtered/selected
ALL_SECTIONS = [
    "basics",
    "work",
    "volunteer",
    "education",
    "awards",
    "certificates",
    "publications",
    "skills",
    "languages",
    "interests",
    "references",
    "projects",
]

# Sections that contain date-filterable entries; maps section -> date field
DATE_FIELD_MAP: dict[str, str] = {
    "work": "startDate",
    "volunteer": "startDate",
    "education": "startDate",
    "projects": "startDate",
    "awards": "date",
    "certificates": "date",
    "publications": "releaseDate",
}
