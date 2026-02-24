# --- ARQUIVO DE DEPENDENCIAS DO PROGRAMA ---

from fastapi import Depends, HTTPException
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema

# Gerenciamento de sessões
def pegarSessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

#Verificação de tokens
def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegarSessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")

    #VERIFICAR O TOKEN SE É VALIDO
    #EXTRAR O id DO USUARIO DO TOKEN
    usuario = session.query(Usuario).filter(Usuario.idUsuario==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario