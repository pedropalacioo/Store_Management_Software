"""
Regras de negócio / Persistência de dados da aplicação.
"""
from __future__ import annotations
from typing import Optional, List
from collections import Dict, Any
from datetime import datetime
from collections import Counter

from persistence.db import listar_pedidos

from src.carrinho import Carrinho
from src.cupom import Cupom
from src.frete import Frete
from src.pedido import Pedido
from src.produto import Produto
from src.item_pedido import ItemPedido

def fechar_pedido(carrinho, cliente, cupom: Cupom | None = None) -> Pedido:
    # 1) Subtotal dos itens
    subtotal = carrinho.calcular_subtotal()

    # 2) Calcular frete a partir do cliente (regras isoladas em frete.py)
    frete = Frete.from_cliente(cliente)  # Frete(uf_origem, uf_destino, valor, prazo_dias)

    # 3) Criar pedido (sem desconto ainda, se você quiser)
    pedido = Pedido(
        cliente=cliente,
        itens=carrinho.itens,
        frete=frete,
        cupom=cupom,
        subtotal=subtotal,
        desconto=0.0,
        valor_frete=frete.valor,
        total=0.0,
        # ... resto dos campos
    )

    # 4) Calcular desconto (cupom usa subtotal + frete do próprio pedido)
    desconto = 0.0
    if cupom is not None:
        desconto = cupom.calcular_desconto_para_pedido(pedido)

    # 5) Calcular total final
    total = subtotal + frete.valor - desconto
    if total < 0:
        total = 0.0

    pedido.desconto = desconto
    pedido.total = total

    # 6) Registrar uso do cupom, se aplicável
    if cupom is not None and desconto > 0:
        cupom.registrar_uso()

    return pedido

def relatorio_ocupacao_periodo(inicio: datetime, fim: datetime) -> Dict[str, Any]:
    """
    Relatório inicial: ocupação por período.

    Ocupação = quantidade de pedidos criados no intervalo [inicio, fim],
    agrupados por status.

    Retorna um dicionário com:
      - inicio, fim
      - total_pedidos
      - quantidade_por_status
      - percentual_por_status
    """
    if inicio > fim:
        raise ValueError("Error: inicial datetime must be smaller than final datetime.")
    
    #carrega os pedidos do banco de dados
    pedidos = listar_pedidos()

    pedidos_filtrados = []

    for pedido in pedidos:
        criado_em = pedido.criado_em #já é datetime

        if criado_em is None :
            continue
        
        #aplicação do filtro de intervalo
        if inicio <= criado_em <= fim:
            pedidos_filtrados.append(pedido)

    contador_status = Counter(p.status for p in pedidos_filtrados)
    total = len(pedidos_filtrados)

    #calculando percentuais
    percentual_por_status: Dict[str, float] = {}
    if total > 0:
        for status, qtd in contador_status.items():
            percentual_por_status[status] = round((qtd/ total) * 100, 2)

    #estrutura do relatório
    return {
        "inicio": inicio,
        "fim": fim,
        "total_pedidos": total,
        "quantidade_por_status": dict(contador_status),
        "percentual_por_status": percentual_por_status
    }

def imprimir_relatorio_ocupacao(relatorio: Dict[str, Any]) -> None:
    """
    Impressão formatada para CLI.
    """

    inicio = relatorio["inicio"].strftime("%d/%m/%Y %H:%M")
    fim = relatorio["fim"].strftime("%d/%m/%Y %H:%M")

    print("\n=== RELATÓRIO DE OCUPAÇÃO POR PERÍODO ===")
    print(f"Período analisado: {inicio}  →  {fim}")
    print(f"Total de pedidos no período: {relatorio['total_pedidos']}\n")

    if relatorio["total_pedidos"] == 0:
        print("Nenhum pedido foi encontrado no intervalo informado.")
        print("==============================================\n")
        return

    print("Distribuição por status:")
    for status, qtd in relatorio["quantidade_por_status"].items():
        perc = relatorio["percentual_por_status"].get(status, 0)
        print(f" - {status}: {qtd} pedido(s) ({perc}%)")

    print("==============================================\n")
