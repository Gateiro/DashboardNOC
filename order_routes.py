# --- ARQUIVO DE ROTAS PARA PEDIDOS AO SISTEMA ---

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from dependencias import pegarSessao
from schemas import AlertasSchema, ClientesSchema, ChamadosSchema
from models import Alertas, Clientes, Chamados

order_router = APIRouter(prefix='/funcionalidades', tags=['funcionalidadesSystem'])

@order_router.get("/")
async def pedidos():
    return {"mensagem":"Você acessou a rota pedidos"}

@order_router.post("/alertas")
async def criarAlerta(alertas_schema: AlertasSchema, session: Session = Depends(pegarSessao)):
    alerta = session.query(Alertas).filter(Alertas.nomeAlerta==alertas_schema.nomeAlerta).first()
    if alerta:
        raise HTTPException(status_code=400, detail=f"Já existe um alerta com o nome {alertas_schema.nomeAlerta}")
    else:
        novoAlerta = Alertas(cliente=alertas_schema.cliente, 
                            nomeAlerta=alertas_schema.nomeAlerta, 
                            plataforma=alertas_schema.plataforma, 
                            warning=alertas_schema.warning,
                            critical=alertas_schema.critical,
                            unknown=alertas_schema.unknown,
                            observacoes=alertas_schema.observacoes)
        session.add(novoAlerta)
        session.commit()
    return HTTPException(status_code=200, detail=f"Alerta {novoAlerta.nomeAlerta} cadastrado com sucesso!")

@order_router.post("/clientes")
async def cadastroCliente(cliente_schema: ClientesSchema, session: Session = Depends(pegarSessao)):
    cliente = session.query(Clientes).filter(or_(Clientes.cnpj==cliente_schema.cnpj,
                                             Clientes.contrato==cliente_schema.contrato,
                                             Clientes.nomeClientes==cliente_schema.nomeClientes)).first()
    if cliente:
        raise HTTPException(status_code=400, detail="Já existe um cliente com este CNPJ/Nome/Contrato")
    else:
        novoCliente = Clientes(nomeClientes=cliente_schema.nomeClientes,
                            cnpj=cliente_schema.cnpj,
                            contrato=cliente_schema.contrato)
        session.add(novoCliente)
        session.commit()
        return HTTPException(status_code=200, detail=f"Cliente {cliente_schema.nomeClientes} cadastrado com sucesso!")
    
@order_router.post("/chamados")
async def cadastroChamado(chamado_schema: ChamadosSchema, session: Session = Depends(pegarSessao)):
    chamado = session.query(Chamados).filter(Chamados.ocorrencias==chamado_schema.ocorrencias).first()
    if chamado:
        raise HTTPException(status_code=400, detail=f"O chamado {chamado_schema.ocorrencias} já consta no sistema.")
    else:
        novoChamado = Chamados(ocorrencias=chamado_schema.ocorrencias,
                               status=chamado_schema.status)
        session.add(novoChamado)
        session.commit()
        return HTTPException(status_code=200, detail=f"Chamado {chamado_schema.ocorrencias} cadastrado com sucesso!")
