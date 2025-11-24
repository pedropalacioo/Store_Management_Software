class Cupom:
    def __init__(self, codigo: str, tipo: str, valor: float, data_validade: None, uso_maximo: int, usos_realizados: int, categ_elegiveis: list[str]):
        self.codigo = codigo
        self.tipo = tipo
        self.valor = valor
        self.data_validade = data_validade
        self.uso_maximo = uso_maximo
        self.usos_reslizados = usos_realizados
        self.categ_elegiveis = []

"""
    Métodos planejados:
    - esta_valido()
    - aplicavel()
    - calcular_desconto()
    - registrar_uso()
"""