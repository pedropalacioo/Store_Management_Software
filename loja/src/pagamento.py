from datetime import datetime
from pedido import Pedido  # ajuste se o nome da file for diferente

class Pagamento:
    def __init__(self, id: int, pedido: Pedido, data_pagamento: datetime, forma: str, valor: float):
        # validações iniciais
        if not isinstance(pedido, Pedido):
            raise TypeError("Error: pedido must be a Pedido object.")

        if not isinstance(data_pagamento, datetime):
            raise TypeError("Error: data_pagamento must be a datetime object.")

        if not isinstance(forma, str):
            raise TypeError("Error: forma must be a string.")

        if not isinstance(valor, float) and not isinstance(valor, int):
            raise TypeError("Error: valor must be a number.")

        self.__id = id
        self.__pedido = pedido
        self.__data_pagamento = data_pagamento
        self.__forma = forma.upper()  # PIX, CREDITO, DEBITO, BOLETO
        self.__valor = float(valor)
        self.__confirmado = False

    # -----------------------------
    # PROPERTIES
    # -----------------------------
    @property
    def id(self):
        return self.__id

    @property
    def pedido(self):
        return self.__pedido

    @property
    def data_pagamento(self):
        return self.__data_pagamento

    @property
    def forma(self):
        return self.__forma

    @property
    def valor(self):
        return self.__valor

    @property
    def confirmado(self):
        return self.__confirmado

    # -----------------------------
    # MÉTODOS PRINCIPAIS
    # -----------------------------

    def validar_valor(self):
        """
        Verifica se o valor pago é suficiente para o total devido do pedido.
        total a pagar = total do pedido (produtos + frete - descontos)
        """
        total_devido = self.__pedido.total

        if self.__valor < total_devido:
            raise ValueError(
                f"Error: valor pago ({self.__valor}) é menor que o total do pedido ({total_devido})."
            )

        return True

    def confirmar(self):
        """
        Confirma o pagamento, marca o pedido como PAGO
        e efetua baixa de estoque.
        """
        if self.__confirmado:
            return  # já confirmado

        self.validar_valor()

        # marca pagamento como confirmado
        self.__confirmado = True


"""
    Métodos planejados:
    - validar_valor()
    - confirmar()
    - estornar()

    Associado ao Pedido
"""