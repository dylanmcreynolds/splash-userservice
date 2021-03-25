from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .models import (
    AccessGroup,
    User,
    UniqueId
)

slartibartfast = User(**{
    "uid": "42",
    "authenticators": [{
       "id": "0000-0000-00042",
       "source": "orcid"
    }],
    "given_name": "slartibartfast"
})

magrathea_group = AccessGroup(**{
    "uid": "42",
    "name": "magrathea builder",
    "members": [
        {
            "id": "0000-0000-00042",
            "source": "orcid"
        }
    ]
})


class GroupSummary(BaseModel):
    group_id: UniqueId
    group_name: str

# Response Models
class GetUsersGroupsResponse(BaseModel):
    groups: List[GroupSummary] = Field(description="list of group IDs and names")


app = FastAPI()


@app.get("/users/{id}")
async def get_user(id: str) -> User:
    return slartibartfast

@app.get("users/{id}/groups", response_model=GetUsersGroupsResponse)
async def get_user_groups(id: str):
    return magrathea_group