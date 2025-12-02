"""
Regras de negócio / Persistência de dados da aplicação.
"""
from __future__ import annotations
from typing import Optional, List

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