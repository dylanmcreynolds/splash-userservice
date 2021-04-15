
from abc import ABC, abstractmethod


from .models import (
    AccessGroup,
    User,
    UniqueId
)

class UserService(ABC):

    @abstractmethod
    async def get_user(self, id: str) -> User:
        raise NotImplementedError()

class UserNotFound(Exception):
    pass