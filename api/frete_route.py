"""
Router para operações de frete e expedição.
Endpoints para registrar envios, rastrear e marcar como entregue.
"""

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from core.frete import Frete

router = APIRouter(
    prefix="/frete",
    tags=["Frete & Expedição"],
)


# Modelos Pydantic
class FreteCalculoRequest(BaseModel):
    cep_origem: str
    cep_destino: str
    peso_kg: float
    largura_cm: float
    altura_cm: float
    comprimento_cm: float


class FreteCalculoResponse(BaseModel):
    tipo_frete: str  # SEDEX, PAC, TRANSPORTADORA, RETIRADA
    valor: float
    prazo_dias: int
    empresa: str


class EnvioCreateRequest(BaseModel):
    pedido_numero: str
    cliente_cpf: str
    endereco_entrega_id: int
    tipo_frete: str
    valor_frete: float
    peso_kg: float
    transportadora: str


class EnvioResponse(BaseModel):
    codigo_rastreio: str
    pedido_numero: str
    cliente_cpf: str
    tipo_frete: str
    valor_frete: float
    transportadora: str
    status: str  # PENDENTE, EM_TRANSITO, ENTREGUE, FALHA_ENTREGA
    data_envio: Optional[datetime] = None
    data_entrega: Optional[datetime] = None
    peso_kg: float


class RastreamentoResponse(BaseModel):
    codigo_rastreio: str
    status: str
    data_atualizacao: datetime
    localizacao: str
    proxima_acao: Optional[str] = None


class EntregaConfirmarRequest(BaseModel):
    data_entrega: datetime
    recebedor_nome: str
    documento_recebedor: Optional[str] = None


@router.post("/calcular", response_model=FreteCalculoResponse)
def calcular_frete(frete_request: FreteCalculoRequest):
    """
    Calcula o valor e prazo de frete para um determinado trajeto.
    
    - **cep_origem**: CEP de origem
    - **cep_destino**: CEP de destino
    - **peso_kg**: Peso do pacote em kg
    - **largura_cm**: Largura em cm
    - **altura_cm**: Altura em cm
    - **comprimento_cm**: Comprimento em cm
    """
    try:
        return {
            "tipo_frete": "SEDEX",
            "valor": 50.0,
            "prazo_dias": 2,
            "empresa": "Correios"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/envios", response_model=EnvioResponse, status_code=status.HTTP_201_CREATED)
def registrar_envio(envio: EnvioCreateRequest):
    """
    Registra um novo envio para um pedido.
    
    - **pedido_numero**: Número do pedido
    - **cliente_cpf**: CPF do cliente
    - **endereco_entrega_id**: ID do endereço de entrega
    - **tipo_frete**: Tipo de frete (SEDEX, PAC, TRANSPORTADORA, RETIRADA)
    - **valor_frete**: Valor do frete
    - **peso_kg**: Peso do pedido em kg
    - **transportadora**: Nome da transportadora
    """
    try:
        return {
            "codigo_rastreio": "RASTR-001",
            "pedido_numero": envio.pedido_numero,
            "cliente_cpf": envio.cliente_cpf,
            "tipo_frete": envio.tipo_frete,
            "valor_frete": envio.valor_frete,
            "transportadora": envio.transportadora,
            "status": "PENDENTE",
            "data_envio": None,
            "data_entrega": None,
            "peso_kg": envio.peso_kg
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/envios/{codigo_rastreio}", response_model=EnvioResponse)
def obter_envio(codigo_rastreio: str):
    """
    Obtém informações de um envio específico.
    
    - **codigo_rastreio**: Código de rastreamento
    """
    try:
        return {
            "codigo_rastreio": codigo_rastreio,
            "pedido_numero": "PED-001",
            "cliente_cpf": "123.456.789-00",
            "tipo_frete": "SEDEX",
            "valor_frete": 50.0,
            "transportadora": "Correios",
            "status": "PENDENTE",
            "data_envio": None,
            "data_entrega": None,
            "peso_kg": 2.5
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Envio {codigo_rastreio} não encontrado"
        )


@router.get("/envios/pedido/{pedido_numero}")
def listar_envios_pedido(pedido_numero: str):
    """
    Lista todos os envios relacionados a um pedido.
    
    - **pedido_numero**: Número do pedido
    """
    try:
        return {
            "pedido_numero": pedido_numero,
            "total_envios": 0,
            "envios": []
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/rastreamento/{codigo_rastreio}", response_model=RastreamentoResponse)
def rastrear_envio(codigo_rastreio: str):
    """
    Rastreia um envio e retorna seu status atual e localização.
    
    - **codigo_rastreio**: Código de rastreamento
    """
    try:
        return {
            "codigo_rastreio": codigo_rastreio,
            "status": "EM_TRANSITO",
            "data_atualizacao": datetime.now(),
            "localizacao": "São Paulo - SP",
            "proxima_acao": "Entrega programada para amanhã"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rastreamento para {codigo_rastreio} não encontrado"
        )


@router.get("/")
def listar_envios(
    status_envio: Optional[str] = None,
    transportadora: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Lista envios com filtros opcionais.
    
    - **status_envio**: Filtrar por status (PENDENTE, EM_TRANSITO, ENTREGUE, FALHA_ENTREGA)
    - **transportadora**: Filtrar por transportadora
    - **skip**: Número de registros a pular
    - **limit**: Máximo de registros a retornar
    """
    try:
        return {
            "total": 0,
            "envios": []
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/envios/{codigo_rastreio}/marcar-enviado")
def marcar_como_enviado(codigo_rastreio: str):
    """
    Marca um envio como enviado (saiu para entrega).
    
    - **codigo_rastreio**: Código de rastreamento
    """
    try:
        return {
            "codigo_rastreio": codigo_rastreio,
            "status_anterior": "PENDENTE",
            "status_novo": "EM_TRANSITO",
            "data_atualizacao": datetime.now()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/envios/{codigo_rastreio}/entregar", response_model=EnvioResponse)
def marcar_como_entregue(codigo_rastreio: str, entrega: EntregaConfirmarRequest):
    """
    Marca um envio como entregue e registra detalhes da entrega.
    
    - **codigo_rastreio**: Código de rastreamento
    - **data_entrega**: Data e hora da entrega
    - **recebedor_nome**: Nome de quem recebeu
    - **documento_recebedor**: CPF/RG de quem recebeu (opcional)
    """
    try:
        return {
            "codigo_rastreio": codigo_rastreio,
            "pedido_numero": "PED-001",
            "cliente_cpf": "123.456.789-00",
            "tipo_frete": "SEDEX",
            "valor_frete": 50.0,
            "transportadora": "Correios",
            "status": "ENTREGUE",
            "data_envio": datetime.now(),
            "data_entrega": entrega.data_entrega,
            "peso_kg": 2.5
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/envios/{codigo_rastreio}/falha-entrega")
def registrar_falha_entrega(codigo_rastreio: str, motivo: str):
    """
    Registra uma falha na tentativa de entrega.
    
    - **codigo_rastreio**: Código de rastreamento
    - **motivo**: Motivo da falha
    """
    try:
        return {
            "codigo_rastreio": codigo_rastreio,
            "status": "FALHA_ENTREGA",
            "motivo": motivo,
            "data_atualizacao": datetime.now(),
            "proxima_tentativa": "A ser agendada"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
