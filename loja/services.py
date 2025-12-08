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

def fechar_pedido_do_carrinho(
        carrinho: Carrinho,
        cupom: Optional[Cupom] = None
) -> Pedido:
    
    # Validação do conteúdo do carrinho
    if not isinstance(carrinho, Carrinho):
        raise TypeError("Error: carrinho must ba a Carrinho Object.")
    
    if not carrinho.itens:
        raise ValueError("Error: carrinho is empty.")
    
    cliente = carrinho.cliente

    # Validação do endereço do cliente
    if not hasattr(cliente, "endereco"):
        raise AttributeError("Error: cliente must have an 'endereco' attribute.")
    
    enderecos = cliente.endereco
    if not isinstance(enderecos, list) or not enderecos:
        raise ValueError("Error: cliente.endereco must be a non-empty list.")

    endereco_entrega = enderecos[0]

    # Validação do estoque
    for item in carrinho.itens:
            produto = item.produto
            quantidade = item.quantidade

            if hasattr(produto, "estoque"):
                estoque_disponivel = getattr(produto, "estoque")
                if quantidade > estoque_disponivel:
                    nome_produto = getattr(produto, "nome", "<sem nome>")
                    sku_produto = getattr(produto, "sku", "<sem sku>")
                    raise ValueError(
                        f"Estoque insuficiente para o produto '{nome_produto}' "
                        f"(SKU {sku_produto}). Quantidade solicitada: {quantidade}, "
                        f"estoque disponível: {estoque_disponivel}."
                    )
    
    # Cálculo do Frete
    frete = Frete.from_cliente(cliente)

    # Conversão de item do carrinho para item do pedido
    itens_pedido: List[ItemPedido] = []
    for item_carrinho in carrinho.itens:
         produto = item_carrinho.produto

         itens_pedido.append(
              ItemPedido(
                   sku = produto.sku,
                   nome = produto.nome,
                   quantidade = item_carrinho.quantidade,
                   preco_unitario = produto.preco
              )
         )

    # Validação e preparação cupom
    cupom_utilizado: Optional[Cupom] = None
    if cupom is not None:
        if not isinstance(cupom, Cupom):
            raise TypeError("Error: cupom must be a Cupom object or None.")
        # só usa se estiver válido
        if cupom.esta_valido():
            cupom_utilizado = cupom
        else:
            cupom_utilizado = None

    # Criação de pedido com os dados
    pedido = Pedido(
        cliente=cliente,
        itens=itens_pedido,
        frete=frete,
        cupom=cupom_utilizado,
        endereco_entrega=endereco_entrega,
    )

    # Se o cupom foi efetivamente usado, registra mais um uso
    if cupom_utilizado is not None:
        cupom_utilizado.registrar_uso()

    # Limpar o carrinho após criar o pedido
    carrinho.limpar()

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
