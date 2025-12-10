from __future__ import annotations

from datetime import datetime
from typing import Optional
from loja.src.pedido import Pedido  # ajuste se o nome da file for diferente


class Pagamento:
    def __init__(
        self,
        id: int,
        pedido: Pedido,
        data_pagamento: Optional[datetime],
        forma: str,
        valor: float,
    ):
        # validações iniciais
        if not isinstance(pedido, Pedido):
            raise TypeError("Error: pedido must be a Pedido object.")

        if data_pagamento is not None and not isinstance(data_pagamento, datetime):
            raise TypeError("Error: data_pagamento must be a datetime object or None.")

        if not isinstance(forma, str):
            raise TypeError("Error: forma must be a string.")

        if not isinstance(valor, (float, int)):
            raise TypeError("Error: valor must be a number.")

        if valor <= 0:
            raise ValueError("Error: valor must be greater than 0.")

        self.__id = id
        self.__pedido = pedido
        self.__data_pagamento = data_pagamento
        self.__forma = forma.upper()  # PIX, CREDITO, DEBITO, BOLETO
        self.__valor = float(valor)
        self.__confirmado = False
        self.__estornado = False

    # -----------------------------
    # PROPERTIES
    # -----------------------------
    @property
    def id(self) -> int:
        return self.__id

    @property
    def pedido(self) -> Pedido:
        return self.__pedido

    @property
    def data_pagamento(self) -> Optional[datetime]:
        return self.__data_pagamento

    @property
    def forma(self) -> str:
        return self.__forma

    @property
    def valor(self) -> float:
        return self.__valor

    @property
    def confirmado(self) -> bool:
        return self.__confirmado

    @property
    def estornado(self) -> bool:
        return self.__estornado

    # -----------------------------
    # REGRAS DE NEGÓCIO
    # -----------------------------

    def validar_valor(self) -> None:
        """
        Verifica se o valor do pagamento não ultrapassa
        o valor em aberto do pedido.
        """
        # Pedido precisa expor valor_em_aberto
        valor_em_aberto = getattr(self.__pedido, "valor_em_aberto", None)
        if valor_em_aberto is None:
            raise AttributeError("Pedido must expose 'valor_em_aberto' property.")

        valor_em_aberto = float(valor_em_aberto)

        if valor_em_aberto <= 0:
            raise ValueError("Error: pedido já está totalmente pago.")

        if self.__valor > valor_em_aberto:
            raise ValueError(
                f"Error: payment value ({self.__valor}) cannot be greater than "
                f"open amount ({valor_em_aberto})."
            )

    def confirmar(self) -> None:
        """
        Confirma o pagamento:
        - valida o valor (não pode exceder o valor em aberto)
        - registra data de pagamento
        - notifica o Pedido para registrar o pagamento (parcial ou total)
        """
        if self.__confirmado:
            raise ValueError("Error: payment already confirmed.")

        if self.__estornado:
            raise ValueError("Error: cannot confirm a refunded payment.")

        self.validar_valor()

        # define a data de pagamento (se ainda não tiver)
        if self.__data_pagamento is None:
            self.__data_pagamento = datetime.now()

        # regra de negócio delegada ao Pedido
        self.__pedido.registrar_pagamento(self)

        # marca pagamento como confirmado
        self.__confirmado = True

    def estornar(self) -> None:
        """
        Estorna o pagamento:
        - só pode estornar se já foi confirmado
        - notifica o Pedido para ajustar total_pago e status
        """
        if not self.__confirmado:
            raise ValueError("Error: cannot refund a non-confirmed payment.")

        if self.__estornado:
            raise ValueError("Error: payment already refunded.")

        self.__estornado = True

        # delega ao Pedido a lógica de atualização (inclusive estoque)
        self.__pedido.registrar_estorno(self)

    def __repr__(self) -> str:
        return (
            f"Pagamento(id={self.__id}, valor={self.__valor:.2f}, forma='{self.__forma}', "
            f"confirmado={self.__confirmado}, estornado={self.__estornado}, "
            f"data_pagamento={self.__data_pagamento})"
        )


"""
    Métodos implementados:
    - validar_valor()
    - confirmar()
    - estornar()

    Associado ao Pedido (pagamento parcial + atualização de estado)
"""
