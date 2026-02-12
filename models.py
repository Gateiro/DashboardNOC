# --- ARQUIVO DE CONFIGURAÇÃO DO BANCO DE DADOS ---
# Instruções enviadas ao SqlAchemy para versionamento do banco

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

#Alertas
class Alertas(Base):
    __tablename__ = "alertas"

    idAlertas = Column("idAlertas", Integer, primary_key=True, autoincrement=True)
    cliente = Column("cliente", ForeignKey("clientes.idClientes"))
    nomeAlerta = Column("nomeAlerta", String(300))
    plataforma = Column("plataforma", String(150))
    warning = Column("warning", Text)
    critical = Column("critical", Text)
    unknown = Column("unknown", Text)
    observacoes = Column("observacoes", Text)

    def __init__(self, cliente, nomeAlerta, plataforma, warning, critical, unknown, observacoes):
        self.cliente=cliente
        self.nomeAlerta=nomeAlerta
        self.plataforma=plataforma
        self.warning=warning
        self.critical=critical
        self.unknown=unknown
        self.observacoes=observacoes

#Chamados
class Chamados(Base):
    __tablename__="chamados"

    id = Column("idChamados", Integer, primary_key=True, autoincrement=True)
    ocorrencias = Column("ocorrencias", String(20))
    status = Column("status", String(100))

    def __init__(self, ocorrencias, status):
        self.ocorrencias = ocorrencias
        self.status = status

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

#Executar a criação dos metadados do banco (Criar de fato o banco)
