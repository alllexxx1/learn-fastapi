import asyncio
from asyncio import new_event_loop
from datetime import datetime
import json

from httpx import AsyncClient, ASGITransport

import pytest
from pytest_asyncio.plugin import event_loop_policy

from sqlalchemy import insert

from config import settings
from database import Base, async_session_maker, engine
from hotels_app.bookings.models import Bookings
from hotels_app.hotels.models import Hotels
from hotels_app.rooms.models import Rooms
from hotels_app.users.models import Users
from main import app as fastapi_app


@pytest.fixture(scope='module', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'hotels_app/tests/fixtures/mock_{model}.json', 'r') as file:
            return json.load(file)

    hotels = open_mock_json('hotels')
    rooms = open_mock_json('rooms')
    users = open_mock_json('users')
    bookings = open_mock_json('bookings')

    for booking in bookings:
        booking['date_from'] = datetime.strptime(booking['date_from'], '%Y-%m-%d')
        booking['date_to'] = datetime.strptime(booking['date_to'], '%Y-%m-%d')

    async with async_session_maker() as session:
        for Model, values in [
            (Hotels, hotels),
            (Rooms, rooms),
            (Users, users),
            (Bookings, bookings)
        ]:
            query = insert(Model).values(values)
            await session.execute(query)
        await session.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Replacing the event loop fixture with a custom implementation is deprecated.
# Instead, "asyncio_default_fixture_loop_scope"
# is configured it "pytest.ini"

# New event loop for test running
# @pytest.fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope='function')
async def async_client():
    async with AsyncClient(
            transport=ASGITransport(app=fastapi_app),
            base_url='http://test') as client:
        yield client


@pytest.fixture(scope='session')
async def authed_async_client():
    async with AsyncClient(
            transport=ASGITransport(app=fastapi_app),
            base_url='http://test') as client:
        await client.post('/api/auth/login', json={
            'email': 'test@test.com',
            'password': 'test'
        })
        assert client.cookies['booking_access_token']
        yield client
