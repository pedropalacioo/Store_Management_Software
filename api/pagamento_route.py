"""
Router para operações de pagamentos.
Endpoints para registrar, confirmar, consultar e estornar pagamentos.
"""

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from core.pagamento import Pagamento

router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"],
)


# Modelos Pydantic
class PagamentoCreateRequest(BaseModel):
    pedido_numero: str
    cliente_cpf: str
    valor: float
    metodo: str  # CREDITO, DEBITO, BOLETO, PIX, DINHEIRO
    parcelas: Optional[int] = 1


class PagamentoResponse(BaseModel):
    id: str
    pedido_numero: str
    cliente_cpf: str
    valor: float
    metodo: str
    parcelas: int
    status: str  # PENDENTE, CONFIRMADO, RECUSADO, ESTORNADO
    data_criacao: datetime
    data_confirmacao: Optional[datetime] = None
    id_transacao_gateway: Optional[str] = None


class PagamentoConfirmarRequest(BaseModel):
    id_transacao: str
    codigo_autorizacao: Optional[str] = None


class PagamentoEstornarRequest(BaseModel):
    motivo: str


class PagamentoListaResponse(BaseModel):
    total: int
    pagamentos: list


@router.post("/", response_model=PagamentoResponse, status_code=status.HTTP_201_CREATED)
def registrar_pagamento(pagamento: PagamentoCreateRequest):
    """
    Registra um novo pagamento para um pedido.
    
    - **pedido_numero**: Número do pedido
    - **cliente_cpf**: CPF do cliente
    - **valor**: Valor do pagamento
    - **metodo**: Método de pagamento (CREDITO, DEBITO, BOLETO, PIX, DINHEIRO)
    - **parcelas**: Número de parcelas (padrão: 1)
    """
    try:
        return {
            "id": "PAG-001",
            "pedido_numero": pagamento.pedido_numero,
            "cliente_cpf": pagamento.cliente_cpf,
            "valor": pagamento.valor,
            "metodo": pagamento.metodo,
            "parcelas": pagamento.parcelas or 1,
            "status": "PENDENTE",
            "data_criacao": datetime.now(),
            "data_confirmacao": None,
            "id_transacao_gateway": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{pagamento_id}", response_model=PagamentoResponse)
def obter_pagamento(pagamento_id: str):
    """
    Obtém os detalhes de um pagamento específico.
    
    - **pagamento_id**: ID do pagamento
    """
    try:
        return {
            "id": pagamento_id,
            "pedido_numero": "PED-001",
            "cliente_cpf": "123.456.789-00",
            "valor": 100.0,
            "metodo": "CREDITO",
            "parcelas": 1,
            "status": "PENDENTE",
            "data_criacao": datetime.now(),
            "data_confirmacao": None,
            "id_transacao_gateway": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pagamento {pagamento_id} não encontrado"
        )


@router.get("/pedido/{pedido_numero}")
def listar_pagamentos_pedido(pedido_numero: str):
    """
    Lista todos os pagamentos relacionados a um pedido.
    
    - **pedido_numero**: Número do pedido
    """
    try:
        return {
            "pedido_numero": pedido_numero,
            "total_pagamentos": 0,
            "pagamentos": []
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/")
def listar_pagamentos(
    cliente_cpf: Optional[str] = None,
    status_pagamento: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Lista pagamentos com filtros opcionais.
    
    - **cliente_cpf**: Filtrar por CPF do cliente
    - **status_pagamento**: Filtrar por status (PENDENTE, CONFIRMADO, RECUSADO, ESTORNADO)
    - **skip**: Número de registros a pular
    - **limit**: Máximo de registros a retornar
    """
    try:
        return {
            "total": 0,
            "pagamentos": []
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{pagamento_id}/confirmar", response_model=PagamentoResponse)
def confirmar_pagamento(pagamento_id: str, dados: PagamentoConfirmarRequest):
    """
    Confirma um pagamento após processamento no gateway.
    
    - **pagamento_id**: ID do pagamento
    - **id_transacao**: ID da transação no gateway de pagamento
    - **codigo_autorizacao**: Código de autorização (opcional)
    """
    try:
        return {
            "id": pagamento_id,
            "pedido_numero": "PED-001",
            "cliente_cpf": "123.456.789-00",
            "valor": 100.0,
            "metodo": "CREDITO",
            "parcelas": 1,
            "status": "CONFIRMADO",
            "data_criacao": datetime.now(),
            "data_confirmacao": datetime.now(),
            "id_transacao_gateway": dados.id_transacao
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{pagamento_id}/recusar")
def recusar_pagamento(pagamento_id: str, motivo: str):
    """
    Marca um pagamento como recusado.
    
    - **pagamento_id**: ID do pagamento
    - **motivo**: Motivo da recusa
    """
    try:
        return {
            "id": pagamento_id,
            "status": "RECUSADO",
            "motivo": motivo,
            "data_atualizacao": datetime.now()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{pagamento_id}/estornar", response_model=PagamentoResponse)
def estornar_pagamento(pagamento_id: str, dados: PagamentoEstornarRequest):
    """
    Realiza o estorno de um pagamento confirmado.
    
    - **pagamento_id**: ID do pagamento a estornar
    - **motivo**: Motivo do estorno
    """
    try:
        return {
            "id": pagamento_id,
            "pedido_numero": "PED-001",
            "cliente_cpf": "123.456.789-00",
            "valor": 100.0,
            "metodo": "CREDITO",
            "parcelas": 1,
            "status": "ESTORNADO",
            "data_criacao": datetime.now(),
            "data_confirmacao": datetime.now(),
            "id_transacao_gateway": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
