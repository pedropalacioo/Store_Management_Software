from core.produto import Produto
from core.produto_fisico import ProdutoFisico
from core.produto_digital import ProdutoDigital

class ItemCarrinho:
    """Item a ser adicionado/removido no carrinho"""
    def __init__(self,
                 produto: Produto,
                 quantidade: int,
                 preco_unitario: float,
    ):
        self.__produto = None
        self.__quantidade = None
        self.__preco_unitario = None

        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
    
    # PRODUTO: GETTER E SETTER
    @property
    def produto(self) -> Produto:
        return self.__produto
    
    @produto.setter
    def produto(self, novo_produto: Produto) -> None:
        if not isinstance(novo_produto, Produto):
            raise TypeError("Erro: produto deve ser uma instância de Produto.")
        self.__produto = novo_produto

    # QUANTIDADE: GETTER E SETTER
    @property
    def quantidade(self) -> int:
        return self.__quantidade
    
    @quantidade.setter
    def quantidade(self, nova_quantidade: int) -> None:
        if not isinstance(nova_quantidade, int):
            raise TypeError("Erro: quantidade deve ser um inteiro.")
        if nova_quantidade <= 0:
            raise ValueError("Erro: quantidade deve ser maior que zero.")
        self.__quantidade = nova_quantidade

    # PREÇO UNITÁRIO: GETTER E SETTER
    @property
    def preco_unitario(self) -> float:
        return self.__preco_unitario
    
    @preco_unitario.setter
    def preco_unitario(self, novo_preco: float) -> None:
        if not isinstance(novo_preco, (int, float)):
            raise TypeError("Erro: preço unitário deve ser um número.")
        if novo_preco < 0:
            raise ValueError("Erro: preço unitário não pode ser negativo.")
        if novo_preco != self.produto.preco:
            raise ValueError(f"Erro: preço não corresponde ao produto ({self.produto.preco})")
        self.__preco_unitario = float(novo_preco)


    # MÉTODOS
    def subtotal(self) -> float:
        """Calcula o subtotal do item (preço unitário x quantidade)"""
        subtotal = self.preco_unitario * self.quantidade
        return subtotal