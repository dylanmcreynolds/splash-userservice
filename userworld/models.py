from typing import List, Optional

from pydantic import BaseModel, Field

class UniqueId(BaseModel):
    id: str = Field("globally unique identifier for user")
    source: Optional[str] = Field("indicates source of identifier, e.g. ORCID")

class User(BaseModel):
    uid: str = Field(description="system unique identifier")
    authenticators: Optional[List[UniqueId]] = Field(description="list of accounts that user can be known by")
    given_name: Optional[str] = Field(description="user's given name")
    family_name: Optional[str] = Field(description="user's family name")


class AccessGroup(BaseModel):
    uid: str = Field("group's system unique identifier")
    name: str = Field("group's name")
    members: List[UniqueId] = Field("list of users in the access group")