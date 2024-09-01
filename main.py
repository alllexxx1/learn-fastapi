from datetime import date
from typing import Optional

from fastapi import FastAPI, Query

from pydantic import BaseModel

import uvicorn


app = FastAPI()


@app.get('/hotels')
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        stars: Optional[int] = Query(None, ge=1, le=5),
        has_spa: Optional[bool] = None

):
    return location, date_from, date_to, stars, has_spa


class SchemaBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post('/bookings')
def add_booking(booking: SchemaBooking):
    pass


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
