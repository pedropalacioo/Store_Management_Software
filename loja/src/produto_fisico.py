from produto import Produto

"Subclasse de Produto!"

class produto_fisico(Produto):
    def __init__(self, nome: str, categoria: str, preco: float, estoque: int, ativo: bool, peso: float, altura: float, largura: float, profundidade: float):
        super().__init__(nome, categoria, preco, estoque, ativo, peso, altura, largura, profundidade)

        self.__peso = peso
        self.__altura = altura
        self.__largura = largura
        self.__profundidade = profundidade

# getters e setters:

    @property
    def peso(self):
        return self.__peso
    
    @peso.setter
    def peso(self, novo_peso):
        if not isinstance(novo_peso, float):
            raise TypeError("Error: peso msut be a float value.")
        self.__peso = novo_peso

    @property
    def altura(self):
        return self.__altura
    
    @altura.setter
    def altura(self, nova_altura):
        if not isinstance(nova_altura, float):
            raise TypeError("Error: altura must be a float value.")
        self.__altura = nova_altura

    @property
    def largura(self):
        return self.__largura
    
    @largura.setter
    def largura(self, nova_largura):
        if not isinstance(nova_largura, float):
            raise TypeError("Error: largura must be a float value.")
        self.__largura = nova_largura

    @property
    def profundidade(self):
        return self.__profundidade
    
    @profundidade.setter
    def profundidade(self, nova_profundidade):
        if not isinstance(nova_profundidade, float):
            raise TypeError("Error: profundidade must be a float value.")
        self.__profundidade = nova_profundidade

#Métodos:
#reescrever __str__() e __repr__()
#def calcular_cubagem()
