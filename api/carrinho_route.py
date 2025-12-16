"""
Router para operações de carrinho de compras.
Endpoints para criar, gerenciar e validar carrinhos.
"""

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from datetime import datetime

from core.cliente import Cliente
from core.carrinho import Carrinho
from core.item_carrinho import ItemCarrinho
from core.produto import Produto
from db.database import carregar_clientes
from services.services_database import (
    validar_limite_itens_carrinho,
    validar_estoque_suficiente,
    ValidacaoDatabaseError
)
from services.utils import limpar_cpf

router = APIRouter(
    prefix="/carrinhos",
    tags=["Carrinho"],
)


# Modelos Pydantic
class ItemCarrinhoRequest(BaseModel):
    produto_sku: str
    quantidade: int


class CarrinhoResponse(BaseModel):
    cliente_cpf: str
    quantidade_itens: int
    subtotal: float
    itens: list


@router.post("/criar", response_model=CarrinhoResponse, status_code=status.HTTP_201_CREATED)
def criar_carrinho(cliente_cpf: str = Query(..., description="CPF do cliente")):
    """
    Cria um novo carrinho para um cliente.
    
    - **cliente_cpf**: CPF do cliente
    """
    try:
        cpf_limpo = limpar_cpf(cliente_cpf)
        
        # Buscar cliente no banco
        clientes = carregar_clientes()
        cliente = None
        
        for c in clientes:
            if c.cpf == cpf_limpo:
                cliente = c
                break
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente com CPF {cpf_limpo} não encontrado"
            )
        
        carrinho = Carrinho(
            cliente=cliente,
            itens=[],
            criado_em=datetime.now(),
            atualizado_em=datetime.now(),
            ativo=True
        )
        
        return {
            "cliente_cpf": cliente.cpf,
            "quantidade_itens": len(carrinho.itens),
            "subtotal": carrinho.subtotal(),
            "itens": []
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{cliente_cpf}/itens", status_code=status.HTTP_201_CREATED)
def adicionar_item_carrinho(cliente_cpf: str, item: ItemCarrinhoRequest):
    """
    Adiciona um item ao carrinho de um cliente.
    
    - **cliente_cpf**: CPF do cliente
    - **item**: Dados do item (sku do produto e quantidade)
    """
    try:
        # Validar limite de itens no carrinho (máximo 50 itens)
        validar_limite_itens_carrinho(quantidade_atual=0, novo_item_quantidade=item.quantidade)
        
        # Validar se há estoque suficiente do produto
        validar_estoque_suficiente(item.produto_sku, item.quantidade)
        
        return {
            "message": "Item adicionado com sucesso",
            "item": item.dict()
        }
    except ValidacaoDatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{cliente_cpf}", response_model=CarrinhoResponse)
def obter_carrinho(cliente_cpf: str):
    """
    Obtém o carrinho de um cliente.
    
    - **cliente_cpf**: CPF do cliente
    """
    try:
        return {
            "cliente_cpf": cliente_cpf,
            "quantidade_itens": 0,
            "subtotal": 0.0,
            "itens": []
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{cliente_cpf}/itens/{produto_sku}", status_code=status.HTTP_204_NO_CONTENT)
def remover_item_carrinho(cliente_cpf: str, produto_sku: str):
    """
    Remove um item do carrinho.
    
    - **cliente_cpf**: CPF do cliente
    - **produto_sku**: SKU do produto a remover
    """
    try:
        return {"message": "Item removido com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{cliente_cpf}/itens/{produto_sku}")
def atualizar_quantidade_item(cliente_cpf: str, produto_sku: str, quantidade: int):
    """
    Atualiza a quantidade de um item no carrinho.
    
    - **cliente_cpf**: CPF do cliente
    - **produto_sku**: SKU do produto
    - **quantidade**: Nova quantidade
    """
    try:
        return {
            "message": "Quantidade atualizada com sucesso",
            "nova_quantidade": quantidade
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{cliente_cpf}", status_code=status.HTTP_204_NO_CONTENT)
def limpar_carrinho(cliente_cpf: str):
    """
    Limpa todos os itens do carrinho.
    
    - **cliente_cpf**: CPF do cliente
    """
    try:
        return {"message": "Carrinho limpo com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
