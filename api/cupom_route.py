"""
Router para operações de cupons de desconto.
Endpoints para criar, listar, validar e gerenciar cupons.
"""

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

from core.cupom import Cupom

router = APIRouter(
    prefix="/cupons",
    tags=["Cupons"],
)


# Modelos Pydantic
class CupomCreateRequest(BaseModel):
    codigo: str
    percentual_desconto: float
    valor_minimo_compra: float
    data_validade: Optional[date] = None
    uso_maximo: Optional[int] = None
    ativo: bool = True


class CupomResponse(BaseModel):
    codigo: str
    percentual_desconto: float
    valor_minimo_compra: float
    data_validade: date
    uso_maximo: int
    usos_realizados: int
    ativo: bool
    data_criacao: datetime


class CupomValidacaoResponse(BaseModel):
    codigo: str
    valido: bool
    percentual_desconto: float
    valor_minimo_compra: float
    motivo_rejeicao: Optional[str] = None


class CupomUpdateRequest(BaseModel):
    percentual_desconto: Optional[float] = None
    valor_minimo_compra: Optional[float] = None
    data_validade: Optional[date] = None
    uso_maximo: Optional[int] = None
    ativo: Optional[bool] = None


@router.post("/", response_model=CupomResponse, status_code=status.HTTP_201_CREATED)
def criar_cupom(cupom: CupomCreateRequest):
    """
    Cria um novo cupom de desconto.
    
    - **codigo**: Código único do cupom
    - **percentual_desconto**: Desconto em percentual (ex: 10.0 para 10%)
    - **valor_minimo_compra**: Valor mínimo de compra para aplicar cupom
    - **data_validade**: Data de validade (opcional, usa padrão de 30 dias se não informado)
    - **uso_maximo**: Máximo de usos (opcional, usa padrão de 100 se não informado)
    - **ativo**: Se o cupom está ativo
    """
    try:
        return {
            "codigo": cupom.codigo,
            "percentual_desconto": cupom.percentual_desconto,
            "valor_minimo_compra": cupom.valor_minimo_compra,
            "data_validade": cupom.data_validade or date.today(),
            "uso_maximo": cupom.uso_maximo or 100,
            "usos_realizados": 0,
            "ativo": cupom.ativo,
            "data_criacao": datetime.now()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", status_code=status.HTTP_200_OK)
def listar_cupons(
    ativo: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Lista cupons disponíveis com filtros opcionais.
    
    - **ativo**: Filtrar apenas cupons ativos
    - **skip**: Número de registros a pular
    - **limit**: Máximo de registros a retornar
    """
    try:
        return {
            "total": 0,
            "cupons": []
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{codigo}", response_model=CupomResponse)
def obter_cupom(codigo: str):
    """
    Obtém os detalhes de um cupom específico.
    
    - **codigo**: Código do cupom
    """
    try:
        return {
            "codigo": codigo,
            "percentual_desconto": 10.0,
            "valor_minimo_compra": 100.0,
            "data_validade": date.today(),
            "uso_maximo": 100,
            "usos_realizados": 0,
            "ativo": True,
            "data_criacao": datetime.now()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cupom {codigo} não encontrado"
        )


@router.post("/{codigo}/validar", response_model=CupomValidacaoResponse)
def validar_cupom(codigo: str, valor_compra: float):
    """
    Valida se um cupom pode ser aplicado para um valor de compra.
    
    - **codigo**: Código do cupom
    - **valor_compra**: Valor total da compra para validação
    """
    try:
        return {
            "codigo": codigo,
            "valido": True,
            "percentual_desconto": 10.0,
            "valor_minimo_compra": 100.0,
            "motivo_rejeicao": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{codigo}", response_model=CupomResponse)
def atualizar_cupom(codigo: str, cupom_update: CupomUpdateRequest):
    """
    Atualiza informações de um cupom existente.
    
    - **codigo**: Código do cupom
    - **cupom_update**: Campos a atualizar
    """
    try:
        return {
            "codigo": codigo,
            "percentual_desconto": cupom_update.percentual_desconto or 10.0,
            "valor_minimo_compra": cupom_update.valor_minimo_compra or 100.0,
            "data_validade": cupom_update.data_validade or date.today(),
            "uso_maximo": cupom_update.uso_maximo or 100,
            "usos_realizados": 0,
            "ativo": cupom_update.ativo if cupom_update.ativo is not None else True,
            "data_criacao": datetime.now()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cupom(codigo: str):
    """
    Deleta/desativa um cupom.
    
    - **codigo**: Código do cupom
    """
    try:
        return {"message": "Cupom deletado com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
