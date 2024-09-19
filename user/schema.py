from pydantic import BaseModel

class UserLoginSchema(BaseModel):
    email:str
    password:str

class UserSignupSchema(BaseModel):
    first_name:str
    last_name:str
    email:str
    password:str


class ForgetPasswordSchema(BaseModel):
    email:str

class ResetPasswordSchema(BaseModel):
    token:str
    new_password:str

class GetVerificationLinkSchema(BaseModel):
    email:str