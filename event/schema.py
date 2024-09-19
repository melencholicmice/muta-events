from pydantic import BaseModel


class CreateEventSchema(BaseModel):
    name:str
    description:str
    location:str

class RegisterAttendeeSchema(BaseModel):
    name:str
    email:str
    phone_number:str