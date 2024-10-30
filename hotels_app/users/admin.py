from typing import Optional

from fastapi import Request
from fastapi.responses import RedirectResponse

from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend

from hotels_app.users.auth import verify_password, create_access_token
from hotels_app.users.dependencies import get_current_user
from hotels_app.users.models import Users
from hotels_app.users.dao import UserDAO


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await UserDAO.find_one_or_none(email=email)
        if not user or not verify_password(password, user.hashed_password):
            return False

        access_token = create_access_token({'sub': str(user.id)})
        request.session.update({"token": access_token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse] | bool:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for('admin:login'), status_code=302)

        user = await get_current_user(token)
        if not user:
            return RedirectResponse(request.url_for('admin:login'), status_code=302)

        return True


class UsersAdmin(ModelView, model=Users):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user-gear"
    can_delete = False

    column_list = [Users.id, Users.email, Users.booking]
    column_searchable_list = [Users.email]

    column_details_exclude_list = [Users.hashed_password]
