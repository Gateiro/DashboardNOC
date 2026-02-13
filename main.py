# --- ARQUIVO DE CONFIGURAÇÃO DO PROGRAMA ---

import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

# 1. Carrega variáveis de ambiente
load_dotenv() 

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI(
    title="NOC Cockpit API",
    description="API de Automação de Chamados (Ticket Master)",
    version="1.0.0"
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# 2. Definição do Modelo de Dados (O que o Front/Copilot deve enviar)
class TicketInput(BaseModel):
    cliente: str       
    assunto: str        
    descricao: str      
    prioridade: str = "P4-Nenhuma das anteriores" 

# 3. Lógica Auxiliar (Separada para organização)
def obter_dados_cliente(nome_cliente: str):
    """Busca CNPJ e Contrato baseado no nome (Case Insensitive)"""
    nome = nome_cliente.lower().strip()
    
    # Dicionário de Clientes
    clientes_db = {
        "bw": (os.getenv("BW"), os.getenv("CONTRATO_BW")),
        "pagbem": (os.getenv("PAGBEM"), os.getenv("CONTRATO_PAGBEM")),
        "stix": (os.getenv("STIX"), os.getenv("CONTRATO_STIX")),
    }
    
    return clientes_db.get(nome, (None, None))

# 4. Rota Principal de Criação de Chamado
@app.post("/api/abrir-chamado")
async def abrir_chamado(ticket: TicketInput):
    
    # A. Validação do Cliente
    cnpj, contrato = obter_dados_cliente(ticket.cliente)
    if not cnpj:
        raise HTTPException(status_code=400, detail=f"Cliente '{ticket.cliente}' não configurado ou não encontrado.")

    # B. Montagem do Payload (Exatamente como no seu script)
    payload = {
        "cnpjcpfcliente": cnpj,
        "numerocontrato": contrato,
        "codigoproduto": "WT-MON",
        "assunto": ticket.assunto,
        "descricao": ticket.descricao,
        "categoria": "CC-Registro",
        "criticidade": ticket.prioridade,
        "usuariocliente": "email@email.com.br", 
        "anexos": [] 
    }

    # C. Envio para o Portal (Com tratamento de erro)
    url_portal = os.getenv("URL")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': os.getenv("AUTHORIZATION")
    }

    # --- MODO DE SEGURANÇA (Mock) ---
    # Enquanto estamos testando, não vamos bombardear o portal real.
    # Quando quiser ativar de verdade, mude MOCK_MODE para False.
    MOCK_MODE = True 

    if MOCK_MODE:
        print(f"Simulando envio para {ticket.cliente}...")
        return {
            "status": "sucesso",
            "modo": "simulacao",
            "mensagem": "Chamado simulado com sucesso",
            "dados_enviados": payload
        }
    
    # --- ENVIO REAL ---
    try:
        response = requests.post(url_portal, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 201:
            dados_resp = response.json()
            return {
                "status": "sucesso",
                "id_chamado": dados_resp.get("ocorrencia"),
                "mensagem": "Chamado criado no portal"
            }
        else:
            # Repassa o erro do portal para quem chamou a API
            raise HTTPException(status_code=502, detail=f"Erro no Portal: {response.text}")
            
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Portal indisponível: {str(e)}")

# Rota de Saúde (Health Check)
@app.get("/")
def home():
    return {"status": "online", "system": "NOC Cockpit v1"}