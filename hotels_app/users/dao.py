from hotels_app.users.models import Users
from hotels_app.dao.base import BaseDAO


class UserDAO(BaseDAO):
    model = Users
