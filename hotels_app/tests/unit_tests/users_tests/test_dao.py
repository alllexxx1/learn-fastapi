from types import NoneType

import pytest
from sqlalchemy.testing import is_instance_of

from hotels_app.users.dao import UserDAO


@pytest.mark.parametrize(
    'user_id, email',
    [(1, 'test@test.com'),
     (2, 'alex@example.com')]
)
async def test_find_one_or_none(user_id, email):
    user = await UserDAO.find_one_or_none(id=user_id)
    assert user.email == email
