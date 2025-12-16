from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from core.pedido import Pedido

class Pagamento:
    
    FORMA_PIX = "PIX"
    FORMA_CREDITO = "CREDITO"
    FORMA_DEBITO = "DEBITO"
    FORMA_BOLETO = "BOLETO"
    
    FORMAS_VALIDAS = {FORMA_PIX, FORMA_CREDITO, FORMA_DEBITO, FORMA_BOLETO}

    def __init__(
        self,
        pedido: "Pedido",
        data_pagamento: Optional[datetime],
        forma: str,
        valor: float,
    ):
        # validações iniciais:
        if not hasattr(pedido, '__class__') or pedido.__class__.__name__ != 'Pedido':
            raise TypeError("Erro: pedido deve ser um objeto de pedido.")
        if data_pagamento is not None and not isinstance(data_pagamento, datetime):
            raise TypeError("Erro: 'data_pagamento' não está em datetime.")
        if not isinstance(forma, str):
            raise TypeError("Erro: forma não é uma string.")
        if forma.upper() not in self.FORMAS_VALIDAS:
            raise ValueError(f"Erro: forma '{forma}' inválida. Válidas: {self.FORMAS_VALIDAS}")
        if not isinstance(valor, (float,int)):
            raise TypeError("Erro: valor deve ser um número.")
        if valor <= 0:
            raise ValueError("Error: valor deve ser maior que 0.")

        self.__pedido = pedido
        self.__data_pagamento = data_pagamento
        self.__forma = forma.upper()
        self.__valor = float(valor)
        self.__confirmado = False
        self.__estornado = False

    # PROPERTIES

    @property
    def pedido(self) -> "Pedido":
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
    
    # Regras de negócio

    def validar_valor(self) -> None:
        """
        Função responsável por verificar se o valor não ultrapassa o valor do pedido.
        """
        valor_pagamento = getattr(self.__pedido, "subtotal", None)
        if valor_pagamento is None:
            raise AttributeError("Pedido deve possuir propriedade 'subtotal'.")
        
        valor_pagamento = float(valor_pagamento)

        if valor_pagamento <= 0:
            raise ValueError("Erro: pedido está totalmente pago.")
        
        if self.__valor > valor_pagamento:
            raise ValueError(f"Erro: valor do pagamento {valor_pagamento}"
                             f"não pode ser maior que o valor do pedido{self.valor}")
        
    def confirmar_pagamento(self) -> None:
        """
        Confirma o pagamento:
        - valida o valor,
        - registra a data de pagamento,
        - notifica o pedido para registrar pagamento inicial ou parcial
        """
        if self.__confirmado:
            raise ValueError("Erro: pedido já confirmado.")
        
        if self.__estornado:
            raise ValueError("Erro: não é possível estornar o pedido.")
        
        self.validar_valor()

        # define a data de pagamento
        if self.__data_pagamento is None:
            self.__data_pagamento = datetime.now()

        # regra de negócio delegada ao pedido
        self.__pedido.registrar_pagamento(self)

        self.__confirmado = True