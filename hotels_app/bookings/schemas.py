from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SchemaBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(
        from_attributes=True
    )

    # deprecated structure
    # class Config:
    #     from_attributes = True


class SchemaBookingInfo(SchemaBooking):
    image_id: int
    name: str
    description: Optional[str] = None
    services: list[str]

    model_config = ConfigDict(
        from_attributes=True
    )

    # deprecated structure
    # class Config:
    #     from_attributes = True


class SchemaNewBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date
