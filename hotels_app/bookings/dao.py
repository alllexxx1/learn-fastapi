from datetime import date

from sqlalchemy import and_, func, or_, insert, select
from sqlalchemy.exc import SQLAlchemyError

from database import async_session_maker
from logger import logger
from hotels_app.bookings.models import Bookings
from hotels_app.dao.base import BaseDAO
from hotels_app.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add_booking(
        cls, user_id: int, room_id: int, date_from: date, date_to: date
    ):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from >= '2023-05-25' AND date_from <= '2023-06-20') OR
            (date_from <= '2023-05-25' AND date_to > '2023-05-25')
        )

        SELECT rooms.quantity - COUNT(booked_rooms.room_id) AS rooms_left
            FROM rooms
            LEFT JOIN booked_rooms ON
            booked_rooms.room_id = rooms.id
            WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id;
        """
        try:
            async with async_session_maker() as session:

                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
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
                    )
                    .cte('booked_rooms')
                )

                query_rooms_left = (
                    select(
                        Rooms.quantity
                        - func.count(booked_rooms.c.room_id).label('rooms_left')
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )
                # print(query_rooms_left.compile(engine, compile_kwargs={'literal_binds': True}))  # Show the raw SQL queries

                query_rooms_left_result = await session.execute(query_rooms_left)
                rooms_left: int = query_rooms_left_result.scalar()

                if rooms_left > 0:
                    query_price = select(Rooms.price).filter_by(id=room_id)
                    query_price_result = await session.execute(query_price)
                    price: int = query_price_result.scalar()

                    query_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )
                    booking = await session.execute(query_booking)
                    await session.commit()
                    return booking.scalar()  # return booking.mappings().one()
                else:
                    return None

        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = 'Database Exception: Cannot add booking'
            elif isinstance(e, Exception):
                msg = 'Unknown Exception: Cannot add booking'
            extra = {
                'room_id': room_id,
                'user_id': user_id,
                'date_from': date_from,
                'date_to': date_to
            }
            logger.error(msg, extra=extra, exc_info=True)


    @classmethod
    async def find_all_bookings(cls, user_id):
        async with async_session_maker() as session:
            query = (
                select(
                    cls.model.__table__.columns,
                    Rooms.__table__.columns,
                )
                .join(Rooms, cls.model.room_id == Rooms.id, isouter=True)
                .where(cls.model.user_id == user_id)
            )

            result = await session.execute(query)
            return result.mappings().all()
