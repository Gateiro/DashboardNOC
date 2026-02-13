# --- ARQUIVO DE ROTAS DE CONFIGURAÇÃO DO PROGRAMA ---

from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from sqlalchemy.orm import Session
from dependencias import pegarSessao
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix='/auth', tags=['auth'])

#Criação de Token JWT
def criarToken(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": id_usuario,
                "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticarUsuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.emailUsuario==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.get('/')
async def autenticar():
    """
    Docstring for autenticar
    """
    return HTTPException(status_code=200, detail="Voce acessou a rota padrão de autenticação")

@auth_router.post("/criarUsuario")
async def criarUsuario(usuario_schema: UsuarioSchema, session:Session=Depends(pegarSessao)):
    usuario = session.query(Usuario).filter(Usuario.emailUsuario==usuario_schema.email).first()
    if usuario:
        #Já existe um usuario com esse email
        raise HTTPException(status_code=400, detail="Já existe um usuário com este email")
    else:
        #Criar um usuario com este nome
        senhaCripto = bcrypt_context.hash(usuario_schema.senha)
        novoUsuario = Usuario(usuario_schema.nome, 
                              usuario_schema.email, 
                              senhaCripto, 
                              usuario_schema.ativo, 
                              usuario_schema.admin)
        session.add(novoUsuario)
        session.commit()
        return HTTPException(status_code=200, detail=f"Usuário criado com sucesso {usuario_schema.email}")
    
#Login -> email e senha -> token JWT 
@auth_router.post("/login")
async def login(login_schema:LoginSchema, session:Session=Depends(pegarSessao)):
    usuario = autenticarUsuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválivdas")
    else:
        accessToken = criarToken(usuario.idUsuario)
        refreshToken = criarToken(usuario.idUsuario)
        return {
            "access_token": accessToken,
            "token_type": "Bearer"
        }
