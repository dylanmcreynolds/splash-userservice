import pytest

from alshub.service import get_user
from alshub.models import User, AccessGroup

@pytest.mark.asyncio
def test_user():
    async 