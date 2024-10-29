from sqladmin import ModelView

from hotels_app.hotels.models import Hotels


class HotelsAdmin(ModelView, model=Hotels):
    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"
    can_delete = False

    column_list = [c.name for c in Hotels.__table__.columns] + [Hotels.room]
    column_searchable_list = [Hotels.name]
