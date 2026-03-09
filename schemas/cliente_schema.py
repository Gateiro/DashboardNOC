from pydantic import BaseModel
from typing import Optional

class ClientesSchema(BaseModel):
    nomeClientes: str
    cnpj: str
    contrato: str

    class Config:
        from_attributes = True