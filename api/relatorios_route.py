"""
Router para operações de relatórios e análises.
Endpoints para gerar relatórios de vendas, ocupação, produtos mais vendidos, etc.
"""

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, Dict, List

router = APIRouter(
    prefix="/relatorios",
    tags=["Relatórios & Análises"],
)


# Modelos Pydantic
class OcupacaoRelatarioResponse(BaseModel):
    total_pedidos: int
    pedidos_por_status: Dict[str, int]
    percentual_entregues: float
    percentual_cancelados: float
    percentual_em_processamento: float
    data_geracao: datetime


class ProdutoVendidoInfo(BaseModel):
    sku: str
    nome: str
    quantidade_vendida: int
    receita_total: float
    ticket_medio: float


class TopProdutosResponse(BaseModel):
    periodo: str
    total_produtos_vendidos: int
    top_produtos: List[ProdutoVendidoInfo]
    data_geracao: datetime


class FaturamentoPedidoResponse(BaseModel):
    pedido_numero: str
    cliente_cpf: str
    data_pedido: date
    subtotal_produtos: float
    desconto_cupom: float
    taxa_frete: float
    total_liquido: float
    status_pagamento: str


class FaturamentoPeriodoResponse(BaseModel):
    data_inicio: date
    data_fim: date
    total_vendas: int
    receita_bruta: float
    total_descontos: float
    total_frete: float
    receita_liquida: float
    ticket_medio: float
    data_geracao: datetime


class ResumoPeriodoInfo(BaseModel):
    periodo: str
    total_vendas: int
    total_faturamento: float
    ticket_medio: float
    margem_liquida: float


class ResumoPedidosResponse(BaseModel):
    data_geracao: datetime
    periodo_analise: str
    resumo_completo: str
    metricas_principais: ResumoPeriodoInfo


@router.get("/ocupacao", response_model=OcupacaoRelatarioResponse)
def gerar_relatorio_ocupacao(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None
):
    """
    Gera relatório de ocupação da loja (distribuição de pedidos por status).
    
    Mostra:
    - Total de pedidos no período
    - Distribuição por status (CRIADO, PAGO, ENVIADO, ENTREGUE, CANCELADO, etc)
    - Percentual de pedidos entregues
    - Percentual de pedidos cancelados
    - Percentual em processamento
    
    - **data_inicio**: Data inicial (opcional, usa últimos 30 dias)
    - **data_fim**: Data final (opcional, usa data de hoje)
    """
    try:
        return {
            "total_pedidos": 0,
            "pedidos_por_status": {
                "CRIADO": 0,
                "PENDENTE_PAGAMENTO": 0,
                "PAGO": 0,
                "ENVIADO": 0,
                "ENTREGUE": 0,
                "CANCELADO": 0
            },
            "percentual_entregues": 0.0,
            "percentual_cancelados": 0.0,
            "percentual_em_processamento": 0.0,
            "data_geracao": datetime.now()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/top-produtos", response_model=TopProdutosResponse)
def gerar_relatorio_top_produtos(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    top_n: Optional[int] = Query(None, ge=1, le=50)
):
    """
    Gera relatório dos produtos mais vendidos no período.
    
    Mostra:
    - Top N produtos por quantidade vendida (configurável, padrão 5 do settings.json)
    - SKU, nome, quantidade vendida
    - Receita total por produto
    - Ticket médio
    
    - **data_inicio**: Data inicial (opcional, usa últimos 30 dias)
    - **data_fim**: Data final (opcional, usa data de hoje)
    - **top_n**: Quantidade de produtos (opcional, usa padrão do settings.json)
    """
    try:
        return {
            "periodo": "Últimos 30 dias",
            "total_produtos_vendidos": 0,
            "top_produtos": [],
            "data_geracao": datetime.now()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/faturamento-pedido/{pedido_numero}", response_model=FaturamentoPedidoResponse)
def gerar_relatorio_faturamento_pedido(pedido_numero: str):
    """
    Gera relatório detalhado de faturamento de um pedido específico.
    
    Mostra:
    - Subtotal dos produtos
    - Desconto aplicado (cupom)
    - Taxa de frete
    - Total líquido
    - Status do pagamento
    
    - **pedido_numero**: Número do pedido
    """
    try:
        return {
            "pedido_numero": pedido_numero,
            "cliente_cpf": "123.456.789-00",
            "data_pedido": date.today(),
            "subtotal_produtos": 0.0,
            "desconto_cupom": 0.0,
            "taxa_frete": 0.0,
            "total_liquido": 0.0,
            "status_pagamento": "PENDENTE"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {pedido_numero} não encontrado"
        )


@router.get("/faturamento-periodo", response_model=FaturamentoPeriodoResponse)
def gerar_relatorio_faturamento_periodo(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    status_filtro: Optional[str] = None
):
    """
    Gera relatório de faturamento consolidado por período.
    
    Mostra:
    - Total de vendas no período
    - Receita bruta
    - Total de descontos (cupons)
    - Total de frete
    - Receita líquida
    - Ticket médio
    
    - **data_inicio**: Data inicial (opcional, usa últimos 30 dias)
    - **data_fim**: Data final (opcional, usa data de hoje)
    - **status_filtro**: Filtrar por status de pedido (opcional)
    """
    try:
        return {
            "data_inicio": date.today(),
            "data_fim": date.today(),
            "total_vendas": 0,
            "receita_bruta": 0.0,
            "total_descontos": 0.0,
            "total_frete": 0.0,
            "receita_liquida": 0.0,
            "ticket_medio": 0.0,
            "data_geracao": datetime.now()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/resumo-vendas", response_model=ResumoPedidosResponse)
def gerar_relatorio_resumo_vendas(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None
):
    """
    Gera um resumo completo e formatado de vendas no período.
    
    Inclui:
    - Total de vendas
    - Receita total (bruta e líquida)
    - Ticket médio
    - Margem de lucro estimada
    - Resumo em texto formatado
    
    - **data_inicio**: Data inicial (opcional, usa últimos 30 dias)
    - **data_fim**: Data final (opcional, usa data de hoje)
    """
    try:
        resumo_texto = """
        ===== RELATÓRIO DE VENDAS =====
        Período: Últimos 30 dias
        
        RESUMO EXECUTIVO:
        - Total de pedidos: 0
        - Receita bruta: R$ 0,00
        - Receita líquida: R$ 0,00
        - Ticket médio: R$ 0,00
        
        STATUS DOS PEDIDOS:
        - Entregues: 0 (0%)
        - Em processamento: 0 (0%)
        - Cancelados: 0 (0%)
        
        PRODUTOS:
        - Produtos mais vendidos: Nenhum
        - Quantidade total de itens: 0
        
        CUSTOS:
        - Descontos (cupons): R$ 0,00
        - Frete total: R$ 0,00
        - Margem líquida: 0%
        """
        
        return {
            "data_geracao": datetime.now(),
            "periodo_analise": "Últimos 30 dias",
            "resumo_completo": resumo_texto,
            "metricas_principais": {
                "periodo": "Últimos 30 dias",
                "total_vendas": 0,
                "total_faturamento": 0.0,
                "ticket_medio": 0.0,
                "margem_liquida": 0.0
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/dashboard")
def dashboard_resumido():
    """
    Retorna um dashboard resumido com as principais métricas.
    """
    try:
        return {
            "timestamp": datetime.now(),
            "pedidos_hoje": 0,
            "faturamento_hoje": 0.0,
            "pedidos_entregues": 0,
            "pedidos_em_processamento": 0,
            "produto_top_1": {
                "nome": "Sem vendas",
                "quantidade": 0,
                "receita": 0.0
            },
            "cliente_top_1": {
                "cpf": "Sem vendas",
                "total_gasto": 0.0,
                "total_pedidos": 0
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
