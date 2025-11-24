import uuid

class Cliente:
    def __init__(self, nome: str, email: str, cpf: str, endereco = None):
        self.__id = self.gerar__id()
        self.__nome = nome
        self.__email = email
        self.__cpf = cpf

        if endereco is None:
            self.__endereco = []
        else:
            if not isinstance(endereco, list):
                raise TypeError("Error: endereco must be a list.")
            if not all(isinstance(item, str) for item in endereco):
                raise TypeError("Error: Every endereco must be a string.")
        self.__endereco = endereco

    
    
    #getter e função: ID

    @property
    def id(self):
        return self.__id
    
    def gerar__id(self):
        return uuid.uuid4().int % 10000
    
    #getter e setter: NOME

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, novo_nome):
        if not isinstance(novo_nome, str):
            raise TypeError("Error: nome must be a string.")
        self.__nome = novo_nome

    #getter e setter: EMAIL

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def endereco(self, novo_email):
        if not isinstance(novo_email, str):
            raise TypeError("Error: email must be a string.")
        self.__email = novo_email

    #getter e setter: CPF
    
    @property
    def cpf(self):
        return self.__cpf
    
    @cpf.setter
    def cpf(self, novo_cpf):
        if not isinstance(novo_cpf, str):
            raise TypeError("Error: cpf must be a string.")
        self.__cpf = novo_cpf

    ###########################################################

    def atualizar_nome(self, novo_nome):
        if not isinstance(novo_nome, str):
            raise TypeError("Error: nome must be a string.")
        self.nome = novo_nome

    ###########################################################

    def atualizar_email(self, novo_email):
        if not isinstance(novo_email, str):
            raise TypeError("Error: email must be a string.")
        if "@" not in novo_email or "." not in novo_email:
            raise ValueError("Error: invalid email.")
        self.email = novo_email
    
    #getter e setter: ENDERECO
    @property
    def endereco(self):
        return self.__endereco
    
    @endereco.setter
    def endereco(self, novo_endereco):
        if not isinstance(novo_endereco, list):
            raise TypeError("Error: endereco must be a list.")
        if not all(isinstance(item, str) for item in novo_endereco):
            raise TypeError("Error: every endereco must be a string.")
        self.__endereco = novo_endereco

    ###########################################################

    def adicionar_endereco(self, endereco):
        if not isinstance(endereco, str):
            raise TypeError("Error: endereco must be a string.")
        self.endereco.append(endereco)

    def remover_endereco(self, endereco):
        if not isinstance(endereco, str):
            raise TypeError("Error: endereco must be a string.")
        if endereco not in self.endereco:
            raise ValueError("Error: endereco not found in the list.")
        
        self.endereco.remove(endereco)

    
    ###########################################################
    # Remover endereço por índice (pode ser usado no futuro!) 
    ###########################################################

    def remover_endereco_indice(self, indice):
        if not isinstance(indice, int):
            raise TypeError("Error: indice must be an intenger.")
        if indice < 0 or indice >= len(self.endereco):
            raise ValueError("Error: indice out of list interval.")
        
        self.endereco.pop(indice)

    # Métodos Especiais:

    def __eq__(self, outro):
        if not isinstance(outro, Cliente):
            raise TypeError("Error: Invalid comparison between other objects.")
        self.cpf = outro.cpf

    def __str__(self):
        return (
            f"Cliente ID: {self.id}"
            f"Nome: {self.nome}"
            f"Email: {self.email}"
            f"CPF: {self.cpf}"
            f"Endereços: {len(self.endereco)}"
        )
    
    def __repr__(self):
        return (
            f"Cliente(id = {self.id}, nome = {self.nome}, "
            f"email: {self.email}, cpf = {self.cpf}"
            f"endereco = {len(self.endereco)})"
        )

    """
    Métodos planejados:
    - adicionar_endereco() FEITO!
    - remover_endereco() FEITO!
    - atualizar_email() FEITO!
    - atualizar_nome() FEITO!
    - __eq__ () --> cpf selecionado para verificação de igualdade. FEITO!
    - __str__ () FEITO!
    Extras:
    -__repr__() FEITO!
    """