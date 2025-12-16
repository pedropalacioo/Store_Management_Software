from core.cliente import Cliente
from core.item_carrinho import ItemCarrinho
from datetime import datetime

class Carrinho:
    def __init__(
            self,
            cliente: Cliente,
            itens: list[ItemCarrinho],
            criado_em: datetime,
            atualizado_em: datetime,
            ativo: bool,
            ):
        self.__cliente = None
        self.__itens = None
        self.__criado_em = None
        self.__atualizado_em = None
        self.__ativo = None

        self.cliente = cliente
        self.itens = itens
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em
        self.ativo = ativo

    # CLIENTE: GETTER E SETTER
    @property
    def cliente(self) -> Cliente:
        return self.__cliente
    
    @cliente.setter
    def cliente(self, novo_cliente: Cliente) -> None:
        if not isinstance(novo_cliente, Cliente):
            raise TypeError("Erro: cliente deve ser uma instância de Cliente.")
        self.__cliente = novo_cliente

    # ITENS: GETTER E SETTER
    @property
    def itens(self) -> list[ItemCarrinho]:
        return self.__itens
    
    @itens.setter
    def itens(self, novos_itens: list[ItemCarrinho]) -> None:
        if not isinstance(novos_itens, list):
            raise TypeError("Erro: itens deve ser uma lista de ItemCarrinho.")
        for item in novos_itens:
            if not isinstance(item, ItemCarrinho):
                raise TypeError("Erro: todos os itens devem ser instâncias de ItemCarrinho.")
        self.__itens = novos_itens

    # CRIADO EM: GETTER E SETTER
    @property
    def criado_em(self) -> datetime:
        return self.__criado_em
    
    @criado_em.setter
    def criado_em(self, nova_data: datetime) -> None:
        if not isinstance(nova_data, datetime):
            raise TypeError("Erro: criado_em deve ser um objeto datetime.")
        self.__criado_em = nova_data
    
    # ATUALIZADO EM: GETTER E SETTER
    @property
    def atualizado_em(self) -> datetime:
        return self.__atualizado_em
    
    @atualizado_em.setter
    def atualizado_em(self, nova_data: datetime) -> None:
        if not isinstance(nova_data, datetime):
            raise TypeError("Erro: atualizado_em deve ser um objeto datetime.")
        self.__atualizado_em = nova_data

    # ATIVO: GETTER E SETTER
    @property
    def ativo(self) -> bool:
        return self.__ativo
    
    @ativo.setter
    def ativo(self, esta_ativo: bool) -> None:
        if not isinstance(esta_ativo, bool):
            raise TypeError("Erro: ativo deve ser um valor booleano.")
        self.__ativo = esta_ativo
    
    # MÉTODOS
    def total(self) -> float:
        """Calcula o total do carrinho somando os subtotais de cada item"""
        total = sum(item.subtotal() for item in self.itens)
        return total
    
    def adicionar_item(self, item: ItemCarrinho, quantidade: int) -> None:
        """Adiciona um item ao carrinho"""
        if not isinstance(item, ItemCarrinho):
            raise TypeError("Erro: item deve ser uma instância de ItemCarrinho.")
        if not isinstance(quantidade, int):
            raise TypeError("Erro: quantidade deve ser um inteiro.")
        if quantidade <= 0:
            raise ValueError("Erro: quantidade deve ser maior que zero.")
        item.quantidade = quantidade

        self.itens.append(item)
        self.atualizado_em = datetime.now()

    def remover_item(self, item: ItemCarrinho) -> None:
        """Remove um item do carrinho"""
        if not isinstance(item, ItemCarrinho):
            raise TypeError("Erro: item deve ser uma instância de ItemCarrinho.")
        if item in self.itens:
            self.itens.remove(item)
            self.atualizado_em = datetime.now()
        else:
            raise ValueError("Erro: item não encontrado no carrinho.")
        
    def alterar_quantidade_item(self, item: ItemCarrinho, nova_quantidade: int) -> None:
        """Altera a quantidade de um item no carrinho"""
        if not isinstance(item, ItemCarrinho):
            raise TypeError("Erro: item deve ser uma instância de ItemCarrinho.")
        if item not in self.itens:
            raise ValueError("Erro: item não encontrado no carrinho.")
        if not isinstance(nova_quantidade, int):
            raise TypeError("Erro: nova_quantidade deve ser um inteiro.")
        if nova_quantidade <= 0:
            raise ValueError("Erro: nova_quantidade deve ser maior que zero.")
        
        item.quantidade = nova_quantidade
        self.atualizado_em = datetime.now()

    def subtotal(self) -> float:
        """Calcula o subtotal do carrinho (total dos itens antes de impostos e descontos)"""
        subtotal = sum(item.subtotal() for item in self.itens)
        return subtotal
    
    # MÉTODOS ESPECIAIS
    def __len__(self) -> int:
        """Retorna a quantidade total de itens no carrinho"""
        return sum(item.quantidade for item in self.itens)
    
