# --- GARANTIR INTEGRIDADE DOS DADOS COM PADRONIZAÇÃO DOS DADOS A SEREM ENVIADOS AO BANCO! ---

from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True

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


class ClientesSchema(BaseModel):
    nomeClientes: str
    cnpj: str
    contrato: str

    class Config:
        from_attributes = True

class ChamadosSchema(BaseModel):
    ocorrencias: str
    status: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email:str
    senha:str

    class Config:
        from_attributes = True