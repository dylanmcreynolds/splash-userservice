
import logging
import sys
from typing import List

from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field

from .models import (
    AccessGroup,
    User,
    UniqueId
)
from .service import UserService, UserNotFound


class GroupSummary(BaseModel):
    group_id: UniqueId
    group_name: str

# Response Models
class GetUsersGroupsResponse(BaseModel):
    groups: List[GroupSummary] = Field(description="list of group IDs and names")

logger = logging.getLogger("users")
app = FastAPI()

@app.on_event("startup")
def startup():
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

# do this slightly complicated thing to make dependency injection work
# and make unit tests easier
this = sys.modules[__name__]
this.service = {}
def get_service() -> UserService:
    if not this.service:
        from alshub.service import ALSHubUserService
        this.service = ALSHubUserService()
    return this.service


@app.get("/users/{orcid}")
async def get_user(orcid: str, user_service: UserService = Depends(get_service)) -> User:
    try:
        return await user_service.get_user(orcid)
    except UserNotFound as e:
        raise HTTPException(404, detail=e.args[0]) from e

# @app.get("users/{id}/groups", response_model=GetUsersGroupsResponse)
# async def get_user_groups(id: str):
#     return magrathea_group
