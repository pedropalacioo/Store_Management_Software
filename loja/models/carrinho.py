class Carrinho:
    def __init__(self, cliente, id: int | None = None):
        self.id = id
        self.cliente = cliente
        self.itens = []
        self.criado_em = None
        self.atualizado_em = None
        self.ativo = True


"""
    Métodos planejados:
    - adicionar_item()
    - remover_item()
    - alterar_quantidade()
    - calcular_subtotal()
    - aplicar_cupom()
    - limpar()
    - __len__()
    - __str__()
"""