from pydantic import BaseModel, ConfigDict, EmailStr


class SchemaUser(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str


class SchemaUserAuth(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        from_attributes=True
    )

    # deprecated structure
    # class Config:
    #     from_attributes = True
