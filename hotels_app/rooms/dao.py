from datetime import date

from sqlalchemy import select, func, and_, or_

from database import async_session_maker
from hotels_app.bookings.models import Bookings
from hotels_app.dao.base import BaseDAO
from hotels_app.rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_hotel_rooms_by_date(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        """
        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked
            FROM bookings
            WHERE (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                  (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            GROUP BY room_id
        )
        SELECT
            -- all columns from Rooms,
            (quantity - COALESCE(rooms_booked, 0)) AS rooms_left FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE hotel_id = 1
        """

        booked_rooms = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to,
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from,
                    ),
                ),
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

        query_hotel_rooms = (
            select(
                Rooms.__table__.columns,
                (Rooms.price * (date_to - date_from).days).label('total_cost'),
                (Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label('rooms_left'),
            )
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .where(
                Rooms.hotel_id == hotel_id
            )
        )

        async with async_session_maker() as session:
            hotel_rooms = await session.execute(query_hotel_rooms)
            return hotel_rooms.mappings().all()
