from core.endereco import Endereco

class Cliente:
    def __init__(
            self,
            nome: str,
            email: str,
            cpf: str,
            endereco: list[Endereco] = None
    ):
        self.__nome = None
        self.__email = None
        self.__cpf = None
        self.__endereco = endereco if endereco is not None else []

        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.endereco = endereco if endereco is not None else []

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

    # EMAIL: GETTER E SETTER
    @property
    def email(self) -> str:
        return self.__email
    
    @email.setter
    def email(self, novo_email: str) -> None:
        if not isinstance(novo_email, str):
            raise TypeError("Erro: email não é uma string.")
        if "@" not in novo_email and "." not in novo_email:
            raise ValueError("Erro: email não possui @ e ponto final.")
        self.__email = novo_email
        
    # CPF: GETTER E SETTER
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

    # ENDEREÇO: GETTER E SETTER
    @property
    def endereco(self) -> list[Endereco]:
        return self.__endereco
    
    @endereco.setter
    def endereco(self, novos_enderecos: list[Endereco]) -> None:
        if not isinstance(novos_enderecos, list):
            raise TypeError("Erro: endereços devem ser uma lista.")
        for endereco in novos_enderecos:
            if not isinstance(endereco, Endereco):
                raise TypeError("Erro: todos os itens da lista devem ser do tipo Endereco.")
        self.__endereco = novos_enderecos

    # MÉTODOS ESPECIAIS

    def __eq__(self, outro) -> bool:
        from .cliente import Cliente

        if not isinstance(outro, Cliente):
            return NotImplemented
        return self.cpf == outro.cpf or self.email == outro.email
    
    def __str__(self) -> str:
        return (
            f"Cliente: {self.nome} |"
            f"email: {self.email} |"
            f"CPF: {self.cpf} |"
            f"Endereços: {[str(endereco) for endereco in self.endereco]}"
        )