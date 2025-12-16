class Endereco:
    def __init__(
            self,
            cep: str,
            cidade: str,
            numero: str,
            UF: str,
    ):
        self.__cep = None
        self.__numero = None
        self.cidade = cidade
        self.UF = UF

        self.cep = cep
        self.numero = numero
        self.cidade = cidade
        self.UF = UF

    # CEP: GETTER E SETTER
    @property
    def cep(self) -> str:
        return self.__cep
    
    # CEP validado
    @cep.setter
    def cep(self, novo_cep: str) -> None:
        if not isinstance(novo_cep, str):
            raise TypeError("Erro: CEP não é uma string.")
        if len(novo_cep) != 8:
            raise ValueError("Erro: CEP deve ter 8 caracteres.")
        if not novo_cep.isdigit():
            raise ValueError("Erro: CEP deve conter apenas dígitos.")
        self.__cep = novo_cep

    # NÚMERO: GETTER E SETTER
    @property
    def numero(self) -> str:
        return self.__numero
    @numero.setter
    def numero(self, novo_numero: str) -> None:
        if not isinstance(novo_numero, str):
            raise TypeError("Erro: número não é uma string.")
        if not novo_numero.strip():
            raise ValueError("Erro: número não pode estar vazio.")
        self.__numero = novo_numero

    # Cidade: GETTER E SETTER
    @property
    def cidade(self) -> str:
        return self.__cidade
    
    @cidade.setter
    def cidade(self, nova_cidade: str) -> None:
        if not isinstance(nova_cidade, str):
            raise TypeError("Erro: cidade não é uma string.")
        if not nova_cidade.strip():
            raise ValueError("Erro: cidade não pode estar vazia.")
        self.__cidade = nova_cidade

    # UF: GETTER E SETTER
    @property
    def UF(self) -> str:
        return self.__UF
    
    @UF.setter
    def UF(self, nova_UF: str) -> None:
        if not isinstance(nova_UF, str):
            raise TypeError("Erro: UF não é uma string.")
        if len(nova_UF) != 2:
            raise ValueError("Erro: UF deve ter 2 caracteres.")
        if not nova_UF.isalpha():
            raise ValueError("Erro: UF deve conter apenas letras.")
        self.__UF = nova_UF.upper()

    # Métodos

    def atualizar_endereco(
            self,
            cep: str,
            numero: str,
            cidade: str,
            UF: str,
    ) -> None:
        """Atualiza os dados do endereço"""
        self.cep = cep
        self.numero = numero
        self.cidade = cidade
        self.UF = UF

    def __str__(self) -> str:
        return( f"Endereço(CEP: {self.cep}," 
                f"Número: {self.numero},"
                f" Cidade: {self.cidade}, UF: {self.UF})."
        )
    
     

