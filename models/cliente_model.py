from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

#Criar a conexão com o banco
db = create_engine("sqlite:///database/banco.db")

#Criar a base do banco
Base = declarative_base()

#Clientes
class Clientes(Base):
    __tablename__="clientes"

    idClientes = Column("idClientes", Integer, primary_key=True, autoincrement=True)
    nomeClientes = Column("nomeClientes", String(150))
    cnpj = Column("cnpnj", String(14))
    contrato = Column("contrato", String(50))

    def __init(self, nomeClientes, cnpj, contrato):
        self.nomeClientes = nomeClientes
        self.cnpj = cnpj
        self.contrato = contrato