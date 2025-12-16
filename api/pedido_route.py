"""
Router para operações de pedidos.
Endpoints para criar, consultar, cancelar e gerenciar pedidos.
"""

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from core.pedido import Pedido
from core.carrinho import Carrinho

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"],
)


# Modelos Pydantic
class PedidoCreateRequest(BaseModel):
    cliente_cpf: str
    endereco_entrega_id: int


class ItemPedidoResponse(BaseModel):
    produto_sku: str
    quantidade: int
    preco_unitario: float
    preco_total: float


class PedidoResponse(BaseModel):
    numero: str
    status: str
    cliente_cpf: str
    data_criacao: datetime
    subtotal: float
    taxa_frete: float
    desconto_cupom: float
    total: float
    itens: list


class PedidoResumoResponse(BaseModel):
    numero: str
    status: str
    cliente_cpf: str
    data_criacao: datetime
    resumo: str


class AplicarCupomRequest(BaseModel):
    codigo_cupom: str


class CancelarPedidoResponse(BaseModel):
    numero: str
    status_anterior: str
    status_novo: str
    mensagem: str


@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido_do_carrinho(pedido: PedidoCreateRequest):
    """
    Cria um pedido a partir do carrinho de um cliente.
    
    - **cliente_cpf**: CPF do cliente
    - **endereco_entrega_id**: ID do endereço de entrega
    """
    try:
        return {
            "numero": "PED-001",
            "status": "CRIADO",
            "cliente_cpf": pedido.cliente_cpf,
            "data_criacao": datetime.now(),
            "subtotal": 0.0,
            "taxa_frete": 0.0,
            "desconto_cupom": 0.0,
            "total": 0.0,
            "itens": []
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{pedido_numero}", response_model=PedidoResponse)
def obter_pedido(pedido_numero: str):
    """
    Obtém os detalhes de um pedido específico.
    
    - **pedido_numero**: Número do pedido (ex: PED-001)
    """
    try:
        return {
            "numero": pedido_numero,
            "status": "CRIADO",
            "cliente_cpf": "123.456.789-00",
            "data_criacao": datetime.now(),
            "subtotal": 0.0,
            "taxa_frete": 0.0,
            "desconto_cupom": 0.0,
            "total": 0.0,
            "itens": []
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {pedido_numero} não encontrado"
        )


@router.get("/")
def listar_pedidos(
    cliente_cpf: Optional[str] = None,
    status_pedido: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Lista pedidos com filtros opcionais.
    
    - **cliente_cpf**: Filtrar por CPF do cliente
    - **status_pedido**: Filtrar por status (CRIADO, PENDENTE_PAGAMENTO, PAGO, ENVIADO, ENTREGUE, CANCELADO)
    - **skip**: Número de registros a pular
    - **limit**: Máximo de registros a retornar
    """
    try:
        return {
            "total": 0,
            "pedidos": []
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{pedido_numero}/cupom")
def aplicar_cupom(pedido_numero: str, cupom: AplicarCupomRequest):
    """
    Aplica um cupom de desconto a um pedido.
    
    - **pedido_numero**: Número do pedido
    - **codigo_cupom**: Código do cupom
    """
    try:
        return {
            "numero": pedido_numero,
            "cupom_aplicado": cupom.codigo_cupom,
            "desconto": 0.0,
            "novo_total": 0.0
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{pedido_numero}/cancelar", response_model=CancelarPedidoResponse)
def cancelar_pedido(pedido_numero: str):
    """
    Cancela um pedido existente.
    Nota: Deve estar dentro da janela de cancelamento (148 horas por padrão).
    
    - **pedido_numero**: Número do pedido a cancelar
    """
    try:
        return {
            "numero": pedido_numero,
            "status_anterior": "CRIADO",
            "status_novo": "CANCELADO",
            "mensagem": "Pedido cancelado com sucesso"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{pedido_numero}/resumo", response_model=PedidoResumoResponse)
def gerar_resumo_pedido(pedido_numero: str):
    """
    Gera um resumo formatado do pedido com informações de status e valores.
    
    - **pedido_numero**: Número do pedido
    """
    try:
        return {
            "numero": pedido_numero,
            "status": "CRIADO",
            "cliente_cpf": "123.456.789-00",
            "data_criacao": datetime.now(),
            "resumo": "Resumo do pedido em texto formatado"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{pedido_numero}/status")
def obter_status_pedido(pedido_numero: str):
    """
    Obtém apenas o status atual de um pedido.
    
    - **pedido_numero**: Número do pedido
    """
    try:
        return {
            "numero": pedido_numero,
            "status": "CRIADO",
            "data_atualizacao": datetime.now()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
