from typing import Optional

from fastapi import APIRouter, Depends

from fastapi_cache.decorator import cache

from exeptions import DateMessException, TooLongBookingPeriodException
from hotels_app.hotels.dao import HotelDAO
from hotels_app.hotels.schemas import (
    SchemaHotelInfo,
    HotelSearchArgs,
    SchemaHotel
)


router = APIRouter(
    prefix='/hotels',
    tags=['Hotels & Rooms']
)


@router.get('')
@cache(expire=30)
async def get_hotels_by_location_and_date(
    search_args: HotelSearchArgs = Depends()
) -> list[SchemaHotelInfo]:
    if search_args.date_from > search_args.date_to:
        raise DateMessException

    if (search_args.date_to - search_args.date_from).days > 31:
        raise TooLongBookingPeriodException

    hotels = await HotelDAO.find_by_location_and_date(
        search_args.location,
        search_args.date_from,
        search_args.date_to
    )
    return hotels


@router.get('/{hotel_id}')
@cache(expire=60)
async def get_hotel(hotel_id: int) -> Optional[SchemaHotel]:
    result = await HotelDAO.find_one_or_none(id=hotel_id)
    return result
