class Frete:
    def __init__(self, uf: str, cidade: str, faixa_cep: str|None, valor: float, prazo_dias: int):
        self.uf = uf
        self.cidade = cidade
        self.faixa_cep = faixa_cep
        self.valor = valor
        self.prazo_dias = prazo_dias

"""
    Métodos planejados:
    - calcular_frete()

    Utilizado por pedido para compor o valor final e prazo de entrega
"""