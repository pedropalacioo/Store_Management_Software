import uuid

class Produto:
    def __init__(self, nome: str, categoria: str, preco: float, estoque: int, ativo: bool):
        self.__sku = self.gerar_sku()
        self.__nome = nome
        self.__categoria = categoria
        self.__preco = preco
        self.__estoque = estoque
        self.__ativo = ativo

    #getter e função: SKU

    @property
    def sku(self):
        return self.__sku
    
    def gerar_sku(self):
        return uuid.uuid4().int% 10000
    
    #getter e setter: NOME

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, novo_nome):
        if not isinstance(novo_nome, str):
            raise TypeError("Error: nome must be a string.")
        self.__nome = novo_nome

    #getter e setter: CATEGORIA

    @property
    def categoria(self):
        return self.__categoria
    
    @categoria.setter
    def categoria(self, nova_categoria):
        if not isinstance(nova_categoria, str):
            raise TypeError("Error: categoria must be a string.")
        self.__categoria = nova_categoria

    #getter e setter: PRECO

    @property
    def preco(self):
        return self.__preco 
    
    @preco.setter
    def preco(self, novo_preco):
        if novo_preco == self.__preco:
            ValueError("Valor igual ao atual.")
        elif not isinstance(novo_preco, float):
            raise TypeError("Entrada inválida!")
        elif novo_preco < 0:
            raise ValueError("Entrada inválida.")
        else:
            self.preco = novo_preco

    #getter e setter: ESTOQUE

    @property
    def estoque(self):
        return self.__preco
    
    @estoque.setter
    def estoque(self, novo_estoque):
        if novo_estoque == self.__estoque:
            ValueError("Valor igual ao atual.")
        elif not isinstance(novo_estoque, int):
            ValueError("Entrada inválida.")
        else:
            self.__estoque = novo_estoque
    
    #####################################################

    def ajustar_estoque(self, valor):
        if valor > 0:
            self.estoque += valor
        elif valor < 0:
            if -valor >= self.estoque:
                self.estoque = 0
            else:
                self.estoque -= valor

    #getter e setter: ATIVIDADE

    @property
    def ativo(self):
        return self.__ativo
    
    @ativo.setter
    def ativo(self, novo_ativo):
        if not isinstance(novo_ativo, bool):
            raise TypeError("Error: ativo must be a bool.")
        self.__ativo = novo_ativo

    #####################################################

    def ativar(self, ssku):
        if self.sku == ssku:
            if not self.ativo == True:
                self.ativo = True
                return print(f"Produto com sku {self.sku} com status: ATIVO.")

    def desativar(self, ssku):
        if self.sku == ssku:
            if not self.ativo == False:
                self.ativo = False
                return print(f"Produto com sku {self.sku} com status: INATIVO.")
            
    #####################################################

    #Métodos planejados:

    def __str__(self):
        return (
            f"Produto {self.nome}. SKU: {self.sku}"
            f"Categoria: {self.categoria}"
            f"Preço: {self.preco}, qtd no estoque: {self.estoque}"
            f"status: {self.ativo}"
        )
    
    def __eq__(self, outro):
        if not isinstance(outro, Produto):
            raise TypeError("Error: invalid comparison between objects")
        self.sku = outro.sku
        
    def __lt__(self, outro):
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
    - __eq__() FEITO!
    - __lt__() --> Usado nome para melhor organização. FEITO!

    Extra:
    - __repr__() FEITO!

    Referenciado por ItemCarrinho e ItemPedido
"""