from abc import ABC, abstractmethod


class Produto(ABC):
    """Classe base para produtos usando Single Table Inheritance"""
    
    def __init__(
            self,
            nome: str,
            descricao: str,
            preco: float,
            tipo: str,
            estoque: int = 0,
            sku: str | None = None,
            categoria: str = "Geral",
            ativo: bool = True,
    ):
        self.__nome = None
        self.__descricao = None
        self.__preco = None
        self.__tipo = tipo
        self.__estoque = None
        self.__sku = None
        self.__categoria = None
        self.__ativo = None
        
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.sku = sku
        self.categoria = categoria
        self.ativo = ativo

    # NOME: GETTER E SETTER
    @property
    def nome(self) -> str:
        return self.__nome
    
    @nome.setter
    def nome(self, novo_nome: str) -> None:
        if not isinstance(novo_nome, str):
            raise TypeError("Erro: nome não é uma string.")
        if not novo_nome.strip():
            raise ValueError("Erro: nome não pode estar vazio.")
        self.__nome = novo_nome

    # DESCRICAO: GETTER E SETTER
    @property
    def descricao(self) -> str:
        return self.__descricao
    
    @descricao.setter
    def descricao(self, nova_descricao: str) -> None:
        if not isinstance(nova_descricao, str):
            raise TypeError("Erro: descrição não é uma string.")
        if not nova_descricao.strip():
            raise ValueError("Erro: descrição não pode estar vazia.")
        self.__descricao = nova_descricao

    # PRECO: GETTER E SETTER
    @property
    def preco(self) -> float:
        return self.__preco
    
    @preco.setter
    def preco(self, novo_preco: float) -> None:
        if not isinstance(novo_preco, (int, float)):
            raise TypeError("Erro: preço deve ser um número.")
        if novo_preco < 0:
            raise ValueError("Erro: preço não pode ser negativo.")
        self.__preco = float(novo_preco)

    # TIPO: GETTER (somente leitura)
    @property
    def tipo(self) -> str:
        return self.__tipo

    # ESTOQUE: GETTER E SETTER
    @property
    def estoque(self) -> int:
        return self.__estoque
    
    @estoque.setter
    def estoque(self, novo_estoque: int) -> None:
        if not isinstance(novo_estoque, int):
            raise TypeError("Erro: estoque deve ser um número inteiro.")
        if novo_estoque < 0:
            raise ValueError("Erro: estoque não pode ser negativo.")
        self.__estoque = novo_estoque

    # SKU: GETTER E SETTER
    @property
    def sku(self) -> str | None:
        return self.__sku
    
    @sku.setter
    def sku(self, novo_sku: str | None) -> None:
        if novo_sku is not None:
            if not isinstance(novo_sku, str):
                raise TypeError("Erro: SKU deve ser uma string.")
            if not novo_sku.strip():
                raise ValueError("Erro: SKU não pode estar vazio.")
        self.__sku = novo_sku

    # CATEGORIA: GETTER E SETTER
    @property
    def categoria(self) -> str:
        return self.__categoria
    
    @categoria.setter
    def categoria(self, nova_categoria: str) -> None:
        if not isinstance(nova_categoria, str):
            raise TypeError("Erro: categoria deve ser uma string.")
        if not nova_categoria.strip():
            raise ValueError("Erro: categoria não pode estar vazia.")
        self.__categoria = nova_categoria

    # ATIVO: GETTER E SETTER
    @property
    def ativo(self) -> bool:
        return self.__ativo
    
    @ativo.setter
    def ativo(self, novo_ativo: bool) -> None:
        if not isinstance(novo_ativo, bool):
            raise TypeError("Erro: ativo deve ser um booleano.")
        self.__ativo = novo_ativo

    # MÉTODOS
    def ajustar_estoque(self, quantidade: int, tipo: str = "baixa") -> None:
        """Ajusta o estoque do produto
        
        Args:
            quantidade: Quantidade a ser adicionada (entrada) ou removida (baixa)
            tipo: 'entrada' para compra/fornecedor ou 'baixa' para pedido faturado
        
        Raises:
            ValueError: Se quantidade > estoque em uma baixa
        """
        if tipo == "entrada":
            self.estoque += quantidade
        elif tipo == "baixa":
            if quantidade > self.estoque:
                raise ValueError(f"Erro: Estoque insuficiente. Disponível: {self.estoque}, Solicitado: {quantidade}")
            self.estoque -= quantidade
        else:
            raise ValueError("Tipo deve ser 'entrada' ou 'baixa'")
    
    def ativar(self) -> None:
        """Ativa o produto"""
        self.ativo = True
    
    def desativar(self) -> None:
        """Desativa o produto"""
        self.ativo = False
    

    # MÉTODOS ESPECIAIS
    def __str__(self) -> str:
        """Representação textual do produto"""
        return f"{self.nome} (SKU: {self.sku}) - R$ {self.preco:.2f}"
    
    def __repr__(self) -> str:
        """Representação técnica do produto"""
        return f"Produto(nome='{self.nome}', sku='{self.sku}', preco={self.preco}, estoque={self.estoque}, tipo='{self.tipo}')"
    
    def __eq__(self, outro: 'Produto') -> bool:
        """Compara produtos por SKU"""
        if not isinstance(outro, Produto):
            return False
        return self.sku == outro.sku
    
    def __lt__(self, outro: 'Produto') -> bool:
        """Compara produtos por nome para ordenação"""
        if not isinstance(outro, Produto):
            raise TypeError(f"Não é possível comparar Produto com {type(outro)}")
        return self.nome < outro.nome
