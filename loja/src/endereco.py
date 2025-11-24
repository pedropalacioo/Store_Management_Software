import uuid #geração de ID

class Endereco:
    def __init__(self, cep: str, cidade: str, uf: str, logradouro: str, numero: str, complemento: str|None):
        self.__id = self.gerar_id()
        self.__cep = cep
        self.__cidade = cidade
        self.__uf = uf
        self.__logradouro = logradouro
        self.__numero = numero
        self.__complemento = complemento

##########################ID####################################

    @property
    def id(self):
        return self.__id
    
    def gerar_id(self):
        return uuid.uuid4().int % 10000
    

###########################CEP##################################

    @property
    def cep(self):
        return self.__cep
    
    @cep.setter
    def cep(self, novo_cep):
        if not isinstance(novo_cep, str):
            raise TypeError("Error: cep must be a string.")
        if len(novo_cep) != 8:
            raise ValueError("Error: cep must have 8 digits.")
        self.__cep = novo_cep
        
############################CIDADE##############################
        
    @property
    def cidade(self):
        return self.__cidade
    
    @cidade.setter
    def cidade(self, nova_cidade):
        if not isinstance(nova_cidade, str):
            raise TypeError("Error: cidade must be a string.")
        self.__cidade = nova_cidade

##########################UF####################################

    @property
    def uf(self):
        return self.__uf
    
    @uf.setter
    def uf(self, novo_uf):
        if not isinstance(novo_uf, str):
            raise TypeError("Error: uf must be a string.")
        if len(novo_uf) != 2:
            raise ValueError("Error: uf must have only 2 digits.")
        self.__uf = novo_uf.upper()
    
#####################LOGRADOURO#################################

    @property
    def logradouro(self):
        return self.__logradouro

    @logradouro.setter
    def logradouro(self, novo_logradouro):
        if not isinstance(novo_logradouro, str):
            raise TypeError("Error: logradouro must be a string.")
        
########################NUMERO##################################

    @property
    def numero(self):
        return self.__numero
    
    @numero.setter
    def numero(self, novo_numero):
        if not isinstance(novo_numero, str):
            raise TypeError("Error: numero must be a string.")
        self.__numero = novo_numero

##################COMPLEMENTO###################################

    @property
    def complemento(self):
        return self.__complemento
    
    @complemento.setter
    def complemento(self, novo_complemento):
        if novo_complemento is not None:
            if not isinstance(novo_complemento, str):
                raise TypeError("Error: complemento must be a string.")
        else:
            self.__complemento = None

##########################################
#                 MÉTODOS                #
##########################################

    def formatar(self) -> str:
        complemento_str = f", Complemento: {self.complemento}" if self.__complemento else ""
        return (
            f"CEP: {self.cep},"
            f"Cidade: {self.cidade}, UF: {self.uf},"
            f"Logradouro: {self.logradouro}, Nº: {self.numero}"
            f"{self.complemento}."
        )


    def validar_cep(self, cep) -> str:
        self.cep = cep
        
    def __str__(self):
        return self.formatar()


        
    

"""
    Métodos planejados:
    - formatar() --> retorna o endereço formatado. FEITO!
    - validar_cep() INCOMPLETO
    Adicional: 
    - __str__() FEITO!

    Pertence a um cliente
    Utilizado em pedido como endereco_entrega 
"""