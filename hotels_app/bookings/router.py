from fastapi import APIRouter, Depends, status

from fastapi_cache.decorator import cache

from pydantic import TypeAdapter

from exeptions import (
    RoomCannotBeBookedException,
    BookingCannotBeDeletedException
)
from hotels_app.bookings.dao import BookingDAO
from hotels_app.bookings.schemas import (
    SchemaBooking,
    SchemaNewBooking,
    SchemaBookingInfo
)
from hotels_app.users.models import Users
from hotels_app.users.dependencies import get_current_user
from hotels_app.tasks.tasks import send_confirmation_email


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
@cache(expire=15)
async def get_bookings(
        user: Users = Depends(get_current_user)
) -> list[SchemaBookingInfo]:
    result = await BookingDAO.find_all_bookings(user_id=user.id)
    return result


@router.post('/add', status_code=status.HTTP_201_CREATED)
async def add_booking(
    booking: SchemaNewBooking,
    user: Users = Depends(get_current_user),
):
    new_booking = await BookingDAO.add_booking(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to
    )
    if not new_booking:
        raise RoomCannotBeBookedException
    # new_booking_dict = parse_obj_as(SchemaBooking, new_booking).dict()  # deprecated
    adapter = TypeAdapter(SchemaBooking)
    new_booking_dict = adapter.validate_python(new_booking).dict()
    send_confirmation_email.delay(new_booking_dict, user.email)
    return new_booking_dict


@router.delete('/{booking_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
        booking_id: int,
        user: Users = Depends(get_current_user)
):
    deleted_booking = await BookingDAO.delete(
        id=booking_id,
        user_id=user.id
    )
    if not deleted_booking:
        raise BookingCannotBeDeletedException
