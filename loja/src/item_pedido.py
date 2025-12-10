from loja.src.produto import Produto

class ItemPedido:
    def __init__(self, sku: str, nome: str, quantidade: int, preco_unitario: float):
        self.__sku = sku
        self.__nome = nome
        self.__quantidade = quantidade
        self.__preco_unitario = preco_unitario

    # SKU
    @property
    def sku(self):
        return self.__sku

    @sku.setter
    def sku(self, novo_sku):
        if not isinstance(novo_sku, str):
            raise TypeError("Error: sku must be a string.")
        if not novo_sku.strip():
            raise ValueError("Error: sku cannot be empty.")
        self.__sku = novo_sku.strip()

    # Nome
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, novo_nome):
        if not isinstance(novo_nome, str):
            raise TypeError("Error: nome must be a string.")
        if not novo_nome.strip():
            raise ValueError("Error: nome cannot be empty.")
        self.__nome = novo_nome.strip()

    # Quantidade
    @property
    def quantidade(self):
        return self.__quantidade

    # Preço unitário
    def preco_unitario(self):
        return self.__preco_unitario
    
    def calcular_total_item(self) -> float:
        return self.__quantidade * self.__preco_unitario

"""
    Método planejado:
    - Total_item()

    Pertence ao pedido
"""