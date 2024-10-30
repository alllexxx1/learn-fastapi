from datetime import date
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles

from sqladmin import Admin

from pydantic import BaseModel

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

import uvicorn

from config import settings
from database import engine
from hotels_app.bookings.router import router as router_bookings
from hotels_app.users.router import router as router_users
from hotels_app.hotels.router import router as router_hotels
from hotels_app.rooms.router import router as router_rooms
from hotels_app.pages.router import router as router_pages
from hotels_app.images.router import router as router_images

from hotels_app.users.admin import AdminAuth
from hotels_app.users.admin import UsersAdmin
from hotels_app.bookings.admin import BookingsAdmin
from hotels_app.hotels.admin import HotelsAdmin
from hotels_app.rooms.admin import RoomsAdmin


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix='cache')
    yield


app = FastAPI(lifespan=lifespan)
app.mount(
    '/static',
    StaticFiles(directory='hotels_app/static'),
    name='static'
)

# All project routers
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_pages)
app.include_router(router_images)

# Admin panel
authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


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
