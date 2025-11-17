class Produto:
    def __init__(self, sku: str, nome: str, categoria: str, _preco: float, _estoque: int, ativo: bool):
        self.sku = sku
        self.nome = nome
        self.categoria = categoria
        self._preco = _preco
        self._estoque = _estoque
        self.ativo = ativo

"""
    Métodos planejados:
    - get_preco() / set_preco()
    - get_estoque() / set_estoque()
    - ajustar_estoque()
    - ativar() / inativar()
    - __str__()
    - __eq__()
    - __lt__()

    Referenciado por ItemCarrinho e ItemPedido
"""