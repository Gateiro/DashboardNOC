from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

#Criar a conexão com o banco
db = create_engine("sqlite:///database/banco.db")

#Criar a base do banco
Base = declarative_base()

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