class Endereco:
    def __init__(self,id: int, cep: str, cidade: str, uf: str, logradouro: str, numero: str, complemento: str|None):
        self.id = id
        self.cep = cep
        self.cidade = cidade
        self.uf = uf
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento

"""
    Métodos planejados:
    - formatar()
    - validar_cep()

    Pertence a um cliente
    Utilizado em pedido como endereco_entrega 
"""