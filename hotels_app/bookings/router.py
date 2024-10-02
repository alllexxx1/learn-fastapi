from typing import List

from fastapi import APIRouter, Depends

from hotels_app.bookings.dao import BookingDAO
from hotels_app.bookings.schemas import SchemaBooking
from hotels_app.users.models import Users
from hotels_app.users.dependencies import get_current_user


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user))-> List[SchemaBooking]:
    result = BookingDAO.find_all(user_id=user.id)
    return await result
