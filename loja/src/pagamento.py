class Pagamento:
    def __init__(self, id: int, pedido: None, data_pagamento: None, forma: str, valor: float):
    #Definir pedido(Pedido) e data_pagamento(datetime)
        self.id = id
        self.pedido = pedido
        self.data_pagamento = data_pagamento
        self.forma = forma
        self.valor = valor

"""
    Métodos planejados:
    - validar_valor()
    - confirmar()
    - estornar()

    Associado ao Pedido
"""