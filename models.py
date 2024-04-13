from pydantic import BaseModel, Extra

class LoginUser(BaseModel):
    email: str

    class Config:
        orm_mode = True
        extra = Extra.forbid


class ValidToken(BaseModel):
    username: str

    class Config:
        orm_mode = True