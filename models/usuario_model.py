from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

#Criar a conexão com o banco
db = create_engine("sqlite:///database/banco.db")

#Criar a base do banco
Base = declarative_base()


#Criar as classes/tabelas do banco
class Usuario(Base):
    __tablename__ = "usuarios"

    idUsuario = Column("idUsuario", Integer, primary_key=True, autoincrement=True)
    nomeUsuario = Column("nomeUsuario", String(150))
    emailUsuario = Column("emailUsuario", String(255), nullable=False)
    senha = Column("senha", String(255))
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nomeUsuario, emailUsuario, senha, ativo=True, admin=False):
        self.nomeUsuario = nomeUsuario
        self.emailUsuario = emailUsuario
        self.senha = senha
        self.ativo = ativo
        self.admin = admin