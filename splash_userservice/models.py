from typing import List, Optional

from pydantic import BaseModel, Field


class UniqueId(BaseModel):
    id: str = Field("globally unique identifier for user")
    source: Optional[str] = Field("indicates source of identifier, e.g. ORCID")


class User(BaseModel):
    uid: str = Field(description="system unique identifier")
    authenticators: Optional[List[UniqueId]] = Field(description="list of accounts that user can be known by")
    given_name: Optional[str] = Field(description="user's given name", schema="https://schema.org/givenName")
    family_name: Optional[str] = Field(description="user's family name")
    current_institution: Optional[str] = Field(description="user's currently known institution")
    current_email: Optional[str] = Field(description="user's currently known email")
    groups: Optional[List[str]] = Field(description="list of groups a user belongs to")
    orcid: str = Field(description="user's ORCID")


class AccessGroup(BaseModel):
    uid: str = Field(description="group's system unique identifier")
    name: str = Field(description="group's name")
    members: Optional[List[UniqueId]] = Field(description="list of users in the access group")


class MappedField(BaseModel):
    source: str
    source_name: str
    source_dtype: str
