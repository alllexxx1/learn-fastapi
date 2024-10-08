from datetime import date
from typing import Optional

from fastapi import FastAPI, Query, Depends

from pydantic import BaseModel

import uvicorn

from hotels_app.bookings.router import router as router_bookings
from hotels_app.users.router import router as router_users
from hotels_app.hotels.router import router as router_hotels
from hotels_app.rooms.router import router as router_rooms

app = FastAPI()

app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)


class HotelSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date,
            date_to: date,
            stars: Optional[int] = Query(None, ge=1, le=5),
            has_spa: Optional[bool] = None
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa


class SchemaHotel(BaseModel):
    address: str
    name: str
    stars: int


# @app.get('/hotels')
# def get_hotels(
#         search_args: HotelSearchArgs = Depends()
# ) -> list[SchemaHotel]:
#
#     hotels = [
#         {
#             'address': 'Gorgia Street, 14. Atlanta ',
#             'name' : 'Meraki Resort',
#             'stars': 5
#         }
#     ]
#
#     return hotels


# class SchemaBooking(BaseModel):
#     room_id: int
#     date_from: date
#     date_to: date


# @app.post('/bookings')
# def add_booking(booking: SchemaBooking):
#     pass


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
