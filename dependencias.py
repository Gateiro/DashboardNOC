# --- ARQUIVO DE DEPENDENCIAS DO PROGRAMA ---

from models import db
from sqlalchemy.orm import sessionmaker

# Gerenciamento de sessões
def pegarSessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()