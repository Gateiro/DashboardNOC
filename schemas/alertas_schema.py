from pydantic import BaseModel
from typing import Optional

class AlertasSchema(BaseModel):
    cliente: int
    nomeAlerta: str
    plataforma: str
    warning: str
    critical: str
    unknown: str
    observacoes: str

    class Config:
        from_attributes = True