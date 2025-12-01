import uuid


class Produto:
    def __init__(self, nome: str, categoria: str, preco: float, estoque: int, ativo: bool = True):
        self.__sku = self._gerar_sku()
        self.nome = nome
        self.categoria = categoria
        self.preco = preco            
        self.estoque = estoque        
        self.ativo = ativo           

    # SKU 

    @property
    def sku(self) -> int:
        return self.__sku

    def _gerar_sku(self) -> int:
        return uuid.uuid4().int % 10000

    # NOME

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, novo_nome: str) -> None:
        if not isinstance(novo_nome, str):
            raise TypeError("Error: nome must be a string.")
        if not novo_nome.strip():
            raise ValueError("Error: nome cannot be empty.")
        self.__nome = novo_nome

    # CATEGORIA

    @property
    def categoria(self) -> str:
        return self.__categoria

    @categoria.setter
    def categoria(self, nova_categoria: str) -> None:
        if not isinstance(nova_categoria, str):
            raise TypeError("Error: categoria must be a string.")
        if not nova_categoria.strip():
            raise ValueError("Error: categoria cannot be empty.")
        self.__categoria = nova_categoria

    # PREÇO

    @property
    def preco(self) -> float:
        return self.__preco

    @preco.setter
    def preco(self, novo_preco: float) -> None:
        if not isinstance(novo_preco, (int, float)):
            raise TypeError("Error: preco must be a number.")
        if novo_preco <= 0:
            raise ValueError("Error: preco must be greater than zero.")
        self.__preco = float(novo_preco)

    # ESTOQUE

    @property
    def estoque(self) -> int:
        return self.__estoque

    @estoque.setter
    def estoque(self, novo_estoque: int) -> None:
        if not isinstance(novo_estoque, int):
            raise TypeError("Error: estoque must be an integer.")
        if novo_estoque < 0:
            raise ValueError("Error: estoque must be non-negative.")
        self.__estoque = novo_estoque

    def ajustar_estoque(self, delta: int) -> None:
    #Delta : Responsável por registrar uma entrada ou saída do estoque.
        if not isinstance(delta, int):
            raise TypeError("Error: delta must be an integer.")
        novo_estoque = self.estoque + delta
        if novo_estoque < 0:
            raise ValueError("Error: resulting estoque cannot be negative.")
        self.estoque = novo_estoque

    # ================= ATIVO =================

    @property
    def ativo(self) -> bool:
        return self.__ativo

    @ativo.setter
    def ativo(self, novo_ativo: bool) -> None:
        if not isinstance(novo_ativo, bool):
            raise TypeError("Error: ativo must be a bool.")
        self.__ativo = novo_ativo

    def ativar(self) -> None:
        self.ativo = True

    def desativar(self) -> None:
        self.ativo = False

    # ================= MÉTODOS ESPECIAIS =================

    def __str__(self) -> str:
        status = "ATIVO" if self.ativo else "INATIVO"
        return (
            f"Produto: {self.nome} | SKU: {self.sku} | "
            f"Categoria: {self.categoria} | Preço: {self.preco:.2f} | "
            f"Estoque: {self.estoque} | Status: {status}"
        )

    def __repr__(self) -> str:
        return (
            f"Produto(sku={self.sku!r}, nome={self.nome!r}, "
            f"categoria={self.categoria!r}, preco={self.preco!r}, "
            f"estoque={self.estoque!r}, ativo={self.ativo!r})"
        )

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Produto):
            return NotImplemented
        return self.sku == outro.sku

    def __lt__(self, outro: object) -> bool:
        if not isinstance(outro, Produto):
            return NotImplemented
        return self.nome < outro.nome

    def __repr__(self):    
        return (f"Produto(sku = {self.sku}, nome = {self.nome}, categoria = {self.categoria},"
                f"preco = {self.preco}, estoque = {self.estoque}, status = {self.status})"
        )

"""
    Métodos planejados:
    - get_preco() / set_preco() FEITO!
    - get_estoque() / set_estoque() FEITO!
    - ajustar_estoque() FEITO!
    - ativar() / inativar() FEITO!
    - __str__() FEITO!
    - __eq__() --> feito com SKU. FEITO!
    - __lt__() --> Usado nome para melhor organização. FEITO!

    Extra:
    - __repr__() FEITO!

    Referenciado por ItemCarrinho e ItemPedido
"""