import uuid
from .endereco import Endereco


class Cliente:
    def __init__(self, nome: str, email: str, cpf: str, enderecos=None):
        self.__id = self.gerar__id()

        self.__nome = None
        self.__email = None
        self.__cpf = None

        self.nome = nome
        self.email = email
        self.cpf = cpf

        # Lista de objetos Endereco (composição)
        if enderecos is None:
            self.__enderecos = []
        else:
            if not isinstance(enderecos, list):
                raise TypeError("Error: enderecos must be a list.")
            if not all(isinstance(item, Endereco) for item in enderecos):
                raise TypeError("Error: each item must be an Endereco object.")
            self.__enderecos = enderecos

    # -------------------------------------------------------------------------
    # ID
    # -------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id

    def gerar__id(self) -> int:
        return uuid.uuid4().int % 10000

    # -------------------------------------------------------------------------
    # NOME
    # -------------------------------------------------------------------------

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, novo_nome: str) -> None:
        if not isinstance(novo_nome, str):
            raise TypeError("Error: nome must be a string.")
        if not novo_nome.strip():     # CORREÇÃO AQUI
            raise ValueError("Error: nome cannot be empty.")
        self.__nome = novo_nome

    # -------------------------------------------------------------------------
    # EMAIL
    # -------------------------------------------------------------------------

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, novo_email: str) -> None:
        if not isinstance(novo_email, str):
            raise TypeError("Error: email must be a string.")
        if "@" not in novo_email or "." not in novo_email:
            raise ValueError("Error: invalid email.")
        self.__email = novo_email

    # -------------------------------------------------------------------------
    # CPF
    # -------------------------------------------------------------------------

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, novo_cpf: str) -> None:
        if not isinstance(novo_cpf, str):
            raise TypeError("Error: cpf must be a string.")
        if len(novo_cpf) != 11:
            raise ValueError("Error: cpf must have 11 digits.")
        if not novo_cpf.isdigit():
            raise ValueError("Error: cpf must contain only digits.")
        self.__cpf = novo_cpf

    # -------------------------------------------------------------------------
    # ENDEREÇOS
    # -------------------------------------------------------------------------

    @property
    def enderecos(self) -> list[Endereco]:
        return self.__enderecos

    @enderecos.setter
    def enderecos(self, nova_lista: list[Endereco]):
        if not isinstance(nova_lista, list):
            raise TypeError("Error: enderecos must be a list.")
        if not all(isinstance(item, Endereco) for item in nova_lista):
            raise TypeError("Error: each item must be an Endereco object.")
        self.__enderecos = nova_lista

    # -------------------------------------------------------------------------
    # MANIPULAÇÃO DE ENDEREÇOS
    # -------------------------------------------------------------------------

    def adicionar_endereco(self, endereco: Endereco) -> None:
        if not isinstance(endereco, Endereco):
            raise TypeError("Error: endereco must be an Endereco object.")
        self.__enderecos.append(endereco)     # CORREÇÃO

    def remover_endereco(self, endereco: Endereco) -> None:
        if not isinstance(endereco, Endereco):
            raise TypeError("Error: endereco must be an Endereco object.")
        if endereco not in self.__enderecos:
            raise ValueError("Error: endereco not found in the list.")
        self.__enderecos.remove(endereco)

    def remover_endereco_indice(self, indice: int) -> None:
        if not isinstance(indice, int):
            raise TypeError("Error: indice must be an integer.")
        if indice < 0 or indice >= len(self.__enderecos):
            raise ValueError("Error: indice out of list interval.")
        self.__enderecos.pop(indice)

    # -------------------------------------------------------------------------
    # MÉTODOS ESPECIAIS
    # -------------------------------------------------------------------------

    def __eq__(self, outro) -> bool:
        from .cliente import Cliente        # CORREÇÃO

        if not isinstance(outro, Cliente):
            return NotImplemented
        return self.cpf == outro.cpf or self.email == outro.email

    def __str__(self) -> str:
        return (
            f"Cliente ID: {self.id} | "
            f"Nome: {self.nome} | "
            f"Email: {self.email} | "
            f"CPF: {self.cpf} | "
            f"Endereços cadastrados: {len(self.__enderecos)}"
        )

    def __repr__(self) -> str:
        return (
            f"Cliente(id={self.id}, nome='{self.nome}', "
            f"email='{self.email}', cpf='{self.cpf}', "
            f"enderecos={len(self.__enderecos)})"
        )

    """
    Métodos planejados:
    - adicionar_endereco() FEITO!
    - remover_endereco() FEITO!
    - atualizar_email() FEITO!
    - atualizar_nome() FEITO!
    - __eq__ () --> cpf e email selecionados para verificação de igualdade. FEITO!
    - __str__ () FEITO!
    Extras:
    -__repr__() FEITO!
    """