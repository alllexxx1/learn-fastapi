from datetime import datetime

import pytest

from hotels_app.bookings.dao import BookingDAO


@pytest.mark.parametrize(
    'user_id, room_id',
    [(2, 2),
     (2, 3),
     (1, 4),
     (1, 4)]
)
async def test_booking_crud(user_id, room_id):
    new_booking = await BookingDAO.add_booking(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime('2026-05-08', '%Y-%m-%d'),
        date_to=datetime.strptime('2026-06-08', '%Y-%m-%d')
    )

    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    new_booking = await BookingDAO.find_one_or_none(id=new_booking.id, room_id=room_id)
    assert new_booking is not None

    await BookingDAO.delete(
        id=new_booking.id,
        user_id=user_id
    )
    new_booking = await BookingDAO.find_one_or_none(id=new_booking.id, room_id=room_id)
    assert new_booking is None
