from pydantic import BaseModel, Extra

class LoginUser(BaseModel):
    email: str
    rid: str

    class Config:
        orm_mode = True
        extra = Extra.forbid


class Report(BaseModel):
    text: str
    rep_type: str
    
    class Config:
        orm_mode = True