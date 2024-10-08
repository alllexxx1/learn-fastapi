from datetime import date, datetime, timezone, timedelta

from pydantic import BaseModel

from fastapi import Query


class SchemaHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int

    class Config:
        from_attributes = True


class SchemaHotelInfo(SchemaHotel):
    rooms_left: int

    class Config:
        from_attribute = True


class HotelSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date = Query(...,
                                    description=f'e.g. {datetime.now(timezone.utc).date()}'),
            date_to: date = Query(...,
                                  description=f'e.g. {(datetime.now(timezone.utc) + timedelta(days=14)).date()}')
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
