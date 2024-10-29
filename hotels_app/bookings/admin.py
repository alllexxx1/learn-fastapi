from sqladmin import ModelView

from hotels_app.bookings.models import Bookings


class BookingsAdmin(ModelView, model=Bookings):
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-b"
    can_delete = True

    column_list = [c.name for c in Bookings.__table__.columns] + [Bookings.user, Bookings.room]
    column_searchable_list = [Bookings.user, Bookings.id]
