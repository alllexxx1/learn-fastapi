from hotels_app.bookings.models import Bookings
from hotels_app.dao.base import BaseDAO


class BookingDAO(BaseDAO):
    model = Bookings
