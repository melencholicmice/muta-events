from pydantic import BaseModel


class CreateEventSchema(BaseModel):
    name:str
    description:str
    location:str