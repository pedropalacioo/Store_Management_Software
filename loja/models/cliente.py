class Cliente:
    def __init__(self, id: int, nome: str, email: str, cpf: str):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.enderecos = []
        
    """
    Métodos planejados:
    - adicionar_endereco()
    - remover_endereco()
    - atualizar_email()
    - atualizar_nome()
    - __eq__ ()
    - __str__ ()
    """