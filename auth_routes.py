# --- ARQUIVO DE ROTAS DE CONFIGURAÇÃO DO PROGRAMA ---

from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from sqlalchemy.orm import Session
from dependencias import pegarSessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema

auth_router = APIRouter(prefix='/auth', tags=['auth'])

def criarToken(email):
    token = f"audhauhduad{email}"
    return token

def autenticarUsuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.emailUsuario==login_schema.email).first()
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
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    else:
        accessToken = criarToken(usuario.idUsuario)
        return {
            "access_token": accessToken,
            "token_type": "Bearer"
        }
        #JWT Bearer
        #headers = {"Access-Token":"Bearer token"}