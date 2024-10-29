from sqladmin import ModelView

from hotels_app.rooms.models import Rooms


class RoomsAdmin(ModelView, model=Rooms):
    name = "Room"
    name_plural = "Rooms"
    icon = "fa-solid fa-bed"
    can_delete = False

    column_list = [c.name for c in Rooms.__table__.columns] + [Rooms.hotel, Rooms.booking]
    column_searchable_list = [Rooms.name]
