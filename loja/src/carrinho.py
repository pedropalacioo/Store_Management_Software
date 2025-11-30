import uuid
from .item_carrinho import ItemCarrinho

class Carrinho:
    def __init__(self, cliente, criado_em=None, atualizado_em=None, ativo=True):
        self.__id = self.gerar__id()
        self.__cliente = cliente
        self.__itens = []
        self.__criado_em = criado_em
        self.__atualizado_em = atualizado_em
        self.__ativo = ativo

    #getter e setter: ID

    @property
    def id(self):
        return self.__id
    
    def gerar__id(self):
        return uuid.uuid4().int % 10000

    #getter e setter: CLIENTE

    @property
    def cliente(self):
        return self.__cliente
    
    @cliente.setter
    def cliente(self, novo_cliente):
        self.__cliente = novo_cliente

    #getter e setter: ITENS

    @property
    def itens(self):
        return self.__itens

    #getter e setter: CRIAÇÃO / ATUALIZAÇÃO

    @property
    def criado_em(self):
        return self.__criado_em
    
    @criado_em.setter
    def criado_em(self, novo):
        if novo is not None:
            raise TypeError("criado_em deve ser None por enquanto.")
        self.__criado_em = novo

    @property
    def atualizado_em(self):
        return self.__atualizado_em
    
    @atualizado_em.setter
    def atualizado_em(self, novo):
        if novo is not None:
            raise TypeError("atualizado_em deve ser None por enquanto.")
        self.__atualizado_em = novo

    #getter e setter: STATUS

    @property
    def ativo(self):
        return self.__ativo
    
    @ativo.setter
    def ativo(self, novo_ativo):
        if not isinstance(novo_ativo, bool):
            raise TypeError("ativo deve ser booleano.")
        self.__ativo = novo_ativo

    #Métodos:

    def adicionar_item(self, produto, quantidade=1):
        """Adiciona item ao carrinho ou soma quantidade se já existir."""
        if quantidade < 1:
            raise ValueError("Quantidade deve ser ≥ 1.")

        for item in self.__itens:
            if item.produto.sku == produto.sku:
                item.quantidade += quantidade
                return
    
        novo_item = ItemCarrinho(
            produto=produto,
            quantidade=quantidade,
            preco_unitario=produto.preco
        )
        self.__itens.append(novo_item)

    def remover_item(self, sku):
        for item in self.__itens:
            if item.produto.sku == sku:
                self.__itens.remove(item)
                return
        raise ValueError(f"Produto com SKU {sku} não está no carrinho.")
    
    def alterar_quantidade(self, sku, nova_quantidade: int):
        if nova_quantidade < 1:
            raise ValueError("Quantidade deve ser maior ou igual a 1.")

        for item in self.__itens:
            if item.produto.sku == sku:
                item.quantidade = nova_quantidade
                return
        
        raise ValueError(f"Produto com SKU {sku} não encontrado no carrinho.")
    
    def calcular_subtotal(self):
        return sum(item.subtotal() for item in self.__itens)

    def limpar(self):
        self.__itens.clear()

    def __len__(self):
        return sum(item.quantidade for item in self.__itens)

    def __str__(self):
        return (
            f"Carrinho ID [{self.id}],"
            f"Cliente: {self.cliente},"
            f"Data de criação: {self.criado_em}, Data de atualização:{self.atualizado_em},"
            f"Status: {self.ativo}."
        )
    
    def __repr__(self):
        return (
            f"Carrinho (id: {self.id},"
            f"cliente: {self.cliente},"
            f"criado_em: {self.criado_em}, atualizado_em: {self.atualizado_em},"
            f"ativo: {self.ativo})"
        )

"""
    Métodos planejados:
    - adicionar_item() FEITO!
    - remover_item() FEITO!
    - alterar_quantidade() FEITO!
    - calcular_subtotal() FEITO!
    - aplicar_cupom() 
    - limpar() FEITO!
    - __len__() FEITO!
    - __str__() FEITO!

    Extra:
    - __repr__() FEITO!
"""