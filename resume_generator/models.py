"""Pydantic models for the JSON Resume schema."""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class Profile(BaseModel):
    network: Optional[str] = None
    username: Optional[str] = None
    url: Optional[str] = None
    model_config = {"extra": "allow"}


class Location(BaseModel):
    address: Optional[str] = None
    postalCode: Optional[str] = None
    city: Optional[str] = None
    countryCode: Optional[str] = None
    region: Optional[str] = None
    model_config = {"extra": "allow"}


class Basics(BaseModel):
    name: Optional[str] = None
    label: Optional[str] = None
    image: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    url: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[Location] = None
    profiles: list[Profile] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class Work(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    position: Optional[str] = None
    url: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    summary: Optional[str] = None
    highlights: list[str] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class Volunteer(BaseModel):
    organization: Optional[str] = None
    position: Optional[str] = None
    url: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    summary: Optional[str] = None
    highlights: list[str] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class Education(BaseModel):
    institution: Optional[str] = None
    url: Optional[str] = None
    area: Optional[str] = None
    studyType: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    score: Optional[str] = None
    courses: list[str] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class Award(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    awarder: Optional[str] = None
    summary: Optional[str] = None
    model_config = {"extra": "allow"}


class Certificate(BaseModel):
    name: Optional[str] = None
    date: Optional[str] = None
    url: Optional[str] = None
    issuer: Optional[str] = None
    model_config = {"extra": "allow"}


class Publication(BaseModel):
    name: Optional[str] = None
    publisher: Optional[str] = None
    releaseDate: Optional[str] = None
    url: Optional[str] = None
    summary: Optional[str] = None
    model_config = {"extra": "allow"}


class Skill(BaseModel):
    name: Optional[str] = None
    level: Optional[str] = None
    keywords: list[str] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class Language(BaseModel):
    language: Optional[str] = None
    fluency: Optional[str] = None
    model_config = {"extra": "allow"}


class Interest(BaseModel):
    name: Optional[str] = None
    keywords: list[str] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class Reference(BaseModel):
    name: Optional[str] = None
    reference: Optional[str] = None
    model_config = {"extra": "allow"}


class Project(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    highlights: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    url: Optional[str] = None
    roles: list[str] = Field(default_factory=list)
    entity: Optional[str] = None
    type: Optional[str] = None
    model_config = {"extra": "allow"}


class Meta(BaseModel):
    canonical: Optional[str] = None
    version: Optional[str] = None
    lastModified: Optional[str] = None
    model_config = {"extra": "allow"}


class Resume(BaseModel):
    basics: Optional[Basics] = None
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
    meta: Optional[Meta] = None
    model_config = {"extra": "allow"}


# All sections that can be filtered/selected
ALL_SECTIONS = [
    "basics", "work", "volunteer", "education", "awards",
    "certificates", "publications", "skills", "languages",
    "interests", "references", "projects",
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
