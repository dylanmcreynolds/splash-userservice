
from abc import ABC, abstractmethod
from enum import Enum

from splash_userservice.models import (
    User
)


class IDType(Enum):
    orcid = "orcid"
    email = "email"


class UserService(ABC):

    @abstractmethod
    async def get_user(self, id: str, id_type: IDType) -> User:
        raise NotImplementedError()


class CommunicationError(Exception):
    pass

class UserNotFound(Exception):
    pass