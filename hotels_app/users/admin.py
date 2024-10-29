from sqladmin import ModelView

from hotels_app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user-gear"
    can_delete = False

    column_list = [Users.id, Users.email, Users.booking]
    column_searchable_list = [Users.email]

    column_details_exclude_list = [Users.hashed_password]
