from typing import List

from fastapi import APIRouter

from hotels_app.bookings.dao import BookingDAO
from hotels_app.bookings.schemas import SchemaBooking


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_bookings() -> List[SchemaBooking]:
    result = BookingDAO.find_all()
    return await result
