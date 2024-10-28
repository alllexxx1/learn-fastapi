from fastapi import APIRouter, Depends

from fastapi_cache.decorator import cache

from exeptions import DateMessException, TooLongBookingPeriodException
from hotels_app.rooms.schemas import SchemaRoomInfo, RoomSearchArgs
from hotels_app.rooms.dao import RoomDAO


router = APIRouter(
    prefix='/hotels',
    tags=['Hotels & Rooms']
)


@router.get('/{hotel_id}/rooms')
@cache(expire=25)
async def get_rooms_by_date(
    hotel_id: int,
    search_args: RoomSearchArgs = Depends()
) -> list[SchemaRoomInfo]:
    if search_args.date_from > search_args.date_to:
        raise DateMessException

    if (search_args.date_to - search_args.date_from).days > 31:
        raise TooLongBookingPeriodException

    rooms = await RoomDAO.find_hotel_rooms_by_date(
        hotel_id,
        search_args.date_from,
        search_args.date_to
    )
    return rooms
