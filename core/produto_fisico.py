from core.produto import Produto


class ProdutoFisico(Produto):
    """Produto físico com atributos de dimensões e peso"""
    
    def __init__(
            self,
            nome: str,
            descricao: str,
            preco: float,
            peso: float,
            altura: float,
            largura: float,
            profundidade: float,
            estoque: int = 0,
            sku: str | None = None,
    ):
        super().__init__(nome, descricao, preco, "fisico", estoque, sku)
        self.__peso = None
        self.__altura = None
        self.__largura = None
        self.__profundidade = None

        self.peso = peso
        self.altura = altura
        self.largura = largura
        self.profundidade = profundidade

    # PESO: GETTERS E SETTERS
    @property
    def peso(self) -> float:
        return self.__peso
    
    @peso.setter
    def peso(self, novo_peso: float) -> None:
        if not isinstance(novo_peso, (float, int)):
            raise TypeError("Erro: peso não é um número.")
        if novo_peso <= 0:
            raise ValueError("Erro: peso deve ser maior que zero.")
        self.__peso = float(novo_peso)

    # ALTURA: GETTERS E SETTERS
    @property
    def altura(self) -> float:
        return self.__altura
    
    @altura.setter
    def altura(self, nova_altura: float) -> None:
        if not isinstance(nova_altura, (float, int)):
            raise TypeError("Erro: altura não é um número.")
        if nova_altura <= 0:
            raise ValueError("Erro: altura deve ser maior que zero.")
        self.__altura = float(nova_altura)

    # LARGURA: GETTERS E SETTERS
    @property
    def largura(self) -> float:
        return self.__largura
    
    @largura.setter
    def largura(self, nova_largura: float) -> None:
        if not isinstance(nova_largura, (float, int)):
            raise TypeError("Erro: largura não é um número.")
        if nova_largura <= 0:
            raise ValueError("Erro: largura deve ser maior que zero.")
        self.__largura = float(nova_largura)

    # PROFUNDIDADE: GETTERS E SETTERS
    @property
    def profundidade(self) -> float:
        return self.__profundidade
    
    @profundidade.setter
    def profundidade(self, nova_profundidade: float) -> None:
        if not isinstance(nova_profundidade, (float, int)):
            raise TypeError("Erro: profundidade não é um número.")
        if nova_profundidade <= 0:
            raise ValueError("Erro: profundidade deve ser maior que zero.")
        self.__profundidade = float(nova_profundidade)

    # MÉTODOS
    def calcular_cubagem(self) -> float:
        """Calcula a cubagem do produto (altura x largura x profundidade)"""
        cubagem = self.altura * self.largura * self.profundidade
        return cubagem
    
    def __str__(self) -> str:
        return (
            f"Produto Físico: {self.nome} | "
            f"Preço: R$ {self.preco:.2f} | "
            f"Peso: {self.peso}kg | "
            f"Dimensões: {self.altura}x{self.largura}x{self.profundidade}cm"
        )
