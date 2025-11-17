class Pedido:
    def __init__(self, id: int, cliente: None, itens: list, frete: None, cupom: None, subtotal: float, desconto: float, valor_frete: float, total: float, status: str, endereco_entrega: None, criado_em: None, pago_em: None, enviado_em: None, entregue_em: None, cancelado_em: None, codigo_rastreio: None):
     #Redefinir atributos
        self.id = id
        self.cliente = cliente
        self.itens = itens
        self.frete = frete
        self.cupom = cupom
        self.subtotal = subtotal
        self.descontos = desconto
        self.valor_frete = valor_frete
        self.total = total
        self.status = status
        self.endereco_entrega = endereco_entrega
        self.criado_em = criado_em
        self.pago_em = pago_em
        self.enviado_em = enviado_em
        self.entregue_em = entregue_em
        self.cancelado_em = cancelado_em
        self.codigo_rastreio = codigo_rastreio

"""
    Métodos planejados:
    - criar_de_carrinho()
    - calcular_subtotal()
    - aplicar_cupom()
    - calcular_total()
    - aplicar_teste()
    - registrar_pagamento()
    - cancelar()
    - gerar_resumo_textual()
    - marcar_enviado()
    - marcar_entregue()
"""

class ItemPedido:
    def __init__(self, produto:  None, quantidade: int, preco_unitario: float):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

"""
    Método planejado:
    - Total_item()

    Pertence ao pedido
"""