from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

#Criar a conexão com o banco
db = create_engine("sqlite:///database/banco.db")

#Criar a base do banco
Base = declarative_base()

#Chamados
class Chamados(Base):
    __tablename__="chamados"

    id = Column("idChamados", Integer, primary_key=True, autoincrement=True)
    ocorrencias = Column("ocorrencias", String(20))
    status = Column("status", String(100))

    def __init__(self, ocorrencias, status):
        self.ocorrencias = ocorrencias
        self.status = status