from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from config import settings
from database import engine
from hotels_app.bookings.admin import BookingsAdmin
from hotels_app.bookings.router import router as router_bookings
from hotels_app.hotels.admin import HotelsAdmin
from hotels_app.hotels.router import router as router_hotels
from hotels_app.images.router import router as router_images
from hotels_app.pages.router import router as router_pages
from hotels_app.rooms.admin import RoomsAdmin
from hotels_app.rooms.router import router as router_rooms
from hotels_app.users.admin import AdminAuth, UsersAdmin
from hotels_app.users.router import router as router_users


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix='cache')
    yield


app = FastAPI(
    title='Hotels booking', version='0.1.0', root_path='/api', lifespan=lifespan
)

app.mount('/static', StaticFiles(directory='hotels_app/static'), name='static')

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


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
