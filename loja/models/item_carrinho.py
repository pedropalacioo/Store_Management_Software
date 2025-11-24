class ItemCarrinho:
    def __init__(self, produto, quantidade: int, preco_unitario: float):
        if preco_unitario <= 0:
            raise ValueError("Preço deve ser positivo.")
        self.__produto = produto
        self.__quantidade = quantidade
        self.__preco_unitario = preco_unitario

    #getter: PRODUTO

    @property
    def produto(self):
        return self.__produto
    
    #getter e setter: QUANTIDADE

    @property
    def quantidade(self):
        return self.__quantidade
    
    @quantidade.setter
    def quantidade(self, nova_qtd):
        if nova_qtd < 1:
            raise ValueError("Quantidade deve ser ≥ 1.")
        self.__quantidade = nova_qtd

    #getter: PREÇO UNITÁRIO

    @property
    def preco_unitario(self):
        return self.__preco_unitario
    
    #Métodos:

    def subtotal(self):
        return self.__quantidade * self.__preco_unitario
    

"""
Classe criada para organização limpa de processo envolvendo operações no carrinho.py
"""