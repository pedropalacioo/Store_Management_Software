import uuid
from cliente import Cliente

class Pedido:
    def __init__(self, cliente: Cliente.cpf, itens: list, frete: None, cupom: None, subtotal: float, desconto: float, valor_frete: float, total: float, status: str, endereco_entrega: None, criado_em: None, pago_em: None, enviado_em: None, entregue_em: None, cancelado_em: None, codigo_rastreio: None):
     #Redefinir atributos
        self.__id = self.gerar__id()

        self.__cliente = None
        self.__itens = None
        self.__frete = None
        self.__cupom = None
        self.__subtotal = None
        self.__descontos = None
        self.__valor_frete = None
        self.__total = None
        self.__status = None
        self.__endereco_entrega = None
        self.__criado_em = None
        self.__pago_em = None
        self.__enviado_em = None
        self.__entregue_em = None
        self.__cancelado_em = None
        self.__codigo_rastreio = None

        self.__cliente = cliente
        self.__itens = itens
        self.__frete = frete
        self.__cupom = cupom
        self.__subtotal = subtotal
        self.__descontos = desconto
        self.__valor_frete = valor_frete
        self.__total = total
        self.__status = status
        self.__endereco_entrega = endereco_entrega
        self.__criado_em = criado_em
        self.__pago_em = pago_em
        self.__enviado_em = enviado_em
        self.__entregue_em = entregue_em
        self.__cancelado_em = cancelado_em
        self.__codigo_rastreio = codigo_rastreio

        @property
        def id(self):
            return self.__id

        def gerar__id(self) -> int:
            return uuid.uuid4().int % 10000
        
        # Cliente

        # Itens

        # Cupom

        # Subtotal

        # Descontos

        # Valor FRETE

        # Valor Frete

        # Total

        # Status

        # Endereço

        # Criação \ Pago\ Enviado\ Entregue\ Cancelado

        # Código de rastreio

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
