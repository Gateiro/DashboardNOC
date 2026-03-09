from pydantic import BaseModel
from typing import Optional

class ChamadosSchema(BaseModel):
    ocorrencias: str
    status: str

    class Config:
        from_attributes = True