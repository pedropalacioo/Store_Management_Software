from produto import Produto


class ProdutoFisico(Produto):
    """Subclasse de Produto para itens físicos (consideram peso/medidas)."""

    def __init__(self, nome: str, categoria: str, preco: float, estoque: int, ativo: bool, peso: float, altura: float, largura: float, profundidade: float,):
        super().__init__(nome, categoria, preco, estoque, ativo)
        self.peso = peso
        self.altura = altura
        self.largura = largura
        self.profundidade = profundidade

    # PESO

    @property
    def peso(self) -> float:
        return self.__peso

    @peso.setter
    def peso(self, novo_peso: float) -> None:
        if not isinstance(novo_peso, (int, float)):
            raise TypeError("Error: peso must be a number.")
        if novo_peso <= 0:
            raise ValueError("Error: peso must be greater than zero.")
        self.__peso = float(novo_peso)

    # ALTURA

    @property
    def altura(self) -> float:
        return self.__altura

    @altura.setter
    def altura(self, nova_altura: float) -> None:
        if not isinstance(nova_altura, (int, float)):
            raise TypeError("Error: altura must be a number.")
        if nova_altura <= 0:
            raise ValueError("Error: altura must be greater than zero.")
        self.__altura = float(nova_altura)

    # LARGURA

    @property
    def largura(self) -> float:
        return self.__largura

    @largura.setter
    def largura(self, nova_largura: float) -> None:
        if not isinstance(nova_largura, (int, float)):
            raise TypeError("Error: largura must be a number.")
        if nova_largura <= 0:
            raise ValueError("Error: largura must be greater than zero.")
        self.__largura = float(nova_largura)

    # PROFUNDIDADE

    @property
    def profundidade(self) -> float:
        return self.__profundidade

    @profundidade.setter
    def profundidade(self, nova_profundidade: float) -> None:
        if not isinstance(nova_profundidade, (int, float)):
            raise TypeError("Error: profundidade must be a number.")
        if nova_profundidade <= 0:
            raise ValueError("Error: profundidade must be greater than zero.")
        self.__profundidade = float(nova_profundidade)

    # MÉTODO EXTRA: CUBAGEM

    def calcular_cubagem(self) -> float:
        return self.altura * self.largura * self.profundidade

    def __str__(self) -> str:
        base = super().__str__()
        return (
            f"{base} | Tipo: FISICO | "
            f"Peso: {self.peso} | "
            f"Dimensões (A x L x P): {self.altura} x {self.largura} x {self.profundidade}"
        )

    def __repr__(self) -> str:
        return (
            f"ProdutoFisico(sku={self.sku!r}, nome={self.nome!r}, "
            f"categoria={self.categoria!r}, preco={self.preco!r}, "
            f"estoque={self.estoque!r}, ativo={self.ativo!r}, "
            f"peso={self.peso!r}, altura={self.altura!r}, "
            f"largura={self.largura!r}, profundidade={self.profundidade!r})"
        )

#Métodos:
# __str__() FEITO!
# __repr__() FEITO!
#def calcular_cubagem() FEITO!
