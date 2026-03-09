from pydantic import BaseModel
from typing import Optional

class LoginSchema(BaseModel):
    email:str
    senha:str

    class Config:
        from_attributes = True
