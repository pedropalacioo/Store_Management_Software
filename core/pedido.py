from core.item_pedido import ItemPedido
from core.cliente import Cliente
from core.cupom import Cupom
from core.frete import Frete
from core.endereco import Endereco
from core.carrinho import Carrinho
from core.item_carrinho import ItemCarrinho
from core.pagamento import Pagamento

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pathlib import Path
import json

# Caminho para o settings.json
SETTINGS_PATH = Path(__file__).resolve().parent.parent / "settings" / "settings.json"

# Cache em memória para as configurações
_SETTINGS_CACHE: Dict[str, Any] | None = None


def carregar_settings_cancelamento() -> Dict[str, Any]:
    """Carrega as configurações de cancelamento do arquivo settings.json"""
    global _SETTINGS_CACHE
    if _SETTINGS_CACHE is None:
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                _SETTINGS_CACHE = json.load(f)
        except FileNotFoundError:
            # Se settings.json não existir, usar valores padrão
            _SETTINGS_CACHE = {
                "regra de cancelamento": {
                    "tempo de cancelamento": 148
                }
            }
    return _SETTINGS_CACHE.get("regra de cancelamento", {})


def obter_janela_cancelamento_horas() -> int:
    """Obtém a janela de cancelamento em horas baseada em settings.json"""
    config = carregar_settings_cancelamento()
    return config.get("tempo de cancelamento", 148)

class Pedido:
    STATUS_CRIADO = "CRIADO"
    STATUS_PENDENTE_PAGAMENTO = "PENDENTE_PAGAMENTO"
    STATUS_PAGO_PARCIAL = "PAGO_PARCIAL"
    STATUS_PAGO = "PAGO"
    STATUS_ENVIADO = "ENVIADO"
    STATUS_ENTREGUE = "ENTREGUE"
    STATUS_CANCELADO = "CANCELADO"

    STATUS_VALIDOS = {STATUS_CRIADO, STATUS_PENDENTE_PAGAMENTO, STATUS_PAGO_PARCIAL,
                      STATUS_PAGO, STATUS_ENVIADO, STATUS_ENTREGUE, STATUS_CANCELADO}

    def __init__(
            self,
            cliente: Cliente,
            itens: list[ItemPedido],
            frete: Frete | None = None,
            cupom: Cupom | None = None,
            endereco_entrega: Endereco | None = None,
            status: str = STATUS_CRIADO,
            criado_em: Optional[datetime] = None
    ):
        # Atributos principais
        self.__cliente: Cliente = None
        self.__itens: List[ItemPedido] = []
        self.__frete: Optional[Frete] = None
        self.__cupom: Optional[Cupom] = None
        self.__status: str = self.STATUS_CRIADO
        self.__criado_em = datetime.now()
        self.__endereco_entrega = None

        self.__subtotal: float = 0.0
        self.__descontos: float = 0.0
        self.__valor_frete: float = 0.0
        self.__total: float = 0.0

        # Pagamentos
        self.__pagamentos: List[Pagamento] = []  # reconhecido pelo Pylance via TYPE_CHECKING
        self.__total_pago: float = 0.0

        self.__status: str = self.STATUS_CRIADO
        self.__endereco_entrega = None

        self.__criado_em: datetime = criado_em or datetime.now()
        self.__pago_em: Optional[datetime] = None
        self.__enviado_em: Optional[datetime] = None
        self.__entregue_em: Optional[datetime] = None
        self.__cancelado_em: Optional[datetime] = None
        self.__codigo_rastreio: Optional[str] = None

        # Usa os setters para validar
        self.cliente = cliente
        self.itens = itens
        self.frete = frete
        self.cupom = cupom
        self.endereco_entrega = endereco_entrega
        self.status = status

        # Calcula valores iniciais
        self.calcular_subtotal()

        self.cliente = cliente
        self.itens = itens
        self.frete = frete
        self.cupom = cupom
        self.status = status
        self.endereco_entrega = endereco_entrega

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
    def itens(self) -> list[ItemPedido]:
        return self.__itens
    
    @itens.setter
    def itens(self, novos_itens: list[ItemPedido]) -> None:
        if not isinstance(novos_itens, list):
            raise TypeError("Erro: itens deve ser uma lista de ItemPedido.")
        for item in novos_itens:
            if not isinstance(item, ItemPedido):
                raise TypeError("Erro: todos os itens devem ser instâncias de ItemPedido.")
        self.__itens = novos_itens

    # FRETE: GETTER E SETTER
    @property
    def frete(self) -> Frete | None:
        return self.__frete
    
    @frete.setter
    def frete(self, novo_frete: Frete | None) -> None:
        if novo_frete is not None and not isinstance(novo_frete, Frete):
            raise TypeError("Erro: frete deve ser uma instância de Frete ou None.")
        self.__frete = novo_frete

    def atualizar_frete(self, novo_frete: Frete | None) -> None:
        """Atualiza o frete do pedido"""
        self.frete = novo_frete if novo_frete is not None else None

    # CUPOM: GETTER E SETTER
    @property
    def cupom(self) -> Cupom | None:
        return self.__cupom
    
    @cupom.setter
    def cupom(self, novo_cupom: Cupom | None) -> None:
        if novo_cupom is not None and not isinstance(novo_cupom, Cupom):
            raise TypeError("Erro: cupom deve ser uma instância de Cupom ou None.")
        self.__cupom = novo_cupom

    # STATUS: GETTER E SETTER
    @property
    def status(self) -> str:
        return self.__status
    
    @status.setter
    def status(self, novo_status: str) -> None:
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError(f"Erro: status '{novo_status}' inválido. Válidos: {self.STATUS_VALIDOS}")
        self.__status = novo_status

    # ENDEREÇO DE ENTREGA: GETTER E SETTER
    @property
    def endereco_entrega(self) -> Endereco | None:
        return self.__endereco_entrega
    
    @endereco_entrega.setter
    def endereco_entrega(self, novo_endereco: Endereco | None) -> None:
        if novo_endereco is not None and not isinstance(novo_endereco, Endereco):
            raise TypeError("Erro: endereço de entrega deve ser uma instância de Endereco ou None.")
        self.__endereco_entrega = novo_endereco

    # DATA DE CRIAÇÃO: GETTER
    @property
    def criado_em(self) -> datetime:
        return self.__criado_em

    # MÉTODOS
    @classmethod
    def criar_de_carrinho(
            cls,
            carrinho: Carrinho,
            endereco_entrega: Endereco | None = None,
            cupom: Cupom | None = None,
            frete: Frete | None = None,
    ) -> 'Pedido':
        """Cria um pedido a partir de um carrinho de compras
        
        Converte a lista de ItemCarrinho em ItemPedido e define o status como CRIADO.
        Valida se a quantidade solicitada é menor ou igual ao estoque disponível.
        
        Args:
            carrinho: Instância de Carrinho com os itens
            endereco_entrega: Endereço para entrega (opcional)
            cupom: Cupom de desconto (opcional)
            frete: Informações de frete (opcional)
        
        Returns:
            Pedido: Nova instância de Pedido com status CRIADO
        
        Raises:
            TypeError: Se carrinho não for uma instância de Carrinho
            ValueError: Se algum item não tiver estoque suficiente
        """
        if not isinstance(carrinho, Carrinho):
            raise TypeError("Erro: carrinho deve ser uma instância de Carrinho.")
        
        # Validar estoque de cada item antes de criar o pedido
        itens_indisponiveis = []
        for item in carrinho.itens:
            if item.quantidade > item.produto.estoque:
                itens_indisponiveis.append(
                    f"'{item.produto.nome}': solicitado {item.quantidade}, "
                    f"disponível {item.produto.estoque}"
                )
        
        if itens_indisponiveis:
            erro_msg = "Erro: Estoque insuficiente para os seguintes produtos:\n" + "\n".join(itens_indisponiveis)
            raise ValueError(erro_msg)
        
        # Converter ItemCarrinho em ItemPedido
        itens_pedido = [
            ItemPedido(
                produto=item.produto,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario
            )
            for item in carrinho.itens
        ]
        
        # Criar instância do pedido com status CRIADO
        pedido = cls(
            cliente=carrinho.cliente,
            itens=itens_pedido,
            frete=frete,
            cupom=cupom,
            endereco_entrega=endereco_entrega,
            status=cls.STATUS_CRIADO
        )
        
        return pedido
    
    def atualizar_status(self, novo_status: str) -> None:
        """Atualiza o status do pedido"""
        self.status = novo_status

    def calcular_subtotal(self) -> float:
        """Calcula o subtotal do pedido (soma de todos os itens) e muda status para PENDENTE_PAGAMENTO
        
        O subtotal inclui apenas o valor dos produtos sem considerar frete ou desconto.
        Após o cálculo, o status é automaticamente atualizado para PENDENTE_PAGAMENTO.
        
        Returns:
            float: Subtotal do pedido (valor total dos itens)
        """
        # Calcular subtotal somando todos os itens
        subtotal = sum(
            item.preco_unitario * item.quantidade 
            for item in self.__itens
        )
        
        # Atualizar status para PENDENTE_PAGAMENTO
        self.status = self.STATUS_PENDENTE_PAGAMENTO
        
        return subtotal
    
    def registrar_pagamento(self, pagamento: Pagamento) -> None:
        from pagamento import Pagamento as PagamentoCls
        if not isinstance(pagamento, PagamentoCls):
            raise TypeError("Erro: pagamento deve ser um objeto da classe Pagamento.")
        
        if getattr(pagamento, "estornado", False):
            raise ValueError("Erro: Impossível registrar um estorno de pagamento.")
        
        if pagamento in self.__pagamentos:
            return
    def cancelar(self) -> None:
        """Cancela o pedido se estiver em CRIADO ou PAGO e dentro da janela de cancelamento
        
        A janela de cancelamento é definida em settings.json (em horas).
        
        Raises:
            ValueError: Se o pedido não estiver em estado cancelável ou fora da janela
        """
        if self.status not in [self.STATUS_CRIADO, self.STATUS_PAGO]:
            raise ValueError(
                f"Erro: Pedido não pode ser cancelado no status '{self.status}'. "
                f"Apenas CRIADO ou PAGO podem ser cancelados."
            )
        
        # Valida se está dentro da janela de cancelamento
        janela_horas = obter_janela_cancelamento_horas()
        tempo_decorrido = datetime.now() - self.__criado_em
        horas_decorridas = tempo_decorrido.total_seconds() / 3600
        
        if horas_decorridas > janela_horas:
            raise ValueError(
                f"Erro: Janela de cancelamento expirada. "
                f"Pedido criado há {horas_decorridas:.1f} horas. "
                f"Janela permitida: {janela_horas} horas."
            )
        
        # Estornar estoque dos itens
        for item in self.__itens:
            item.produto.ajustar_estoque(item.quantidade, tipo="entrada")
        
        self.status = self.STATUS_CANCELADO
        self.__cancelado_em = datetime.now()
    
    def gerar_resumo(self) -> str:
        """Gera um resumo textual do pedido
        
        Returns:
            str: Resumo formatado do pedido
        """
        resumo = f"""
╔════════════════════════════════════════════════════════════╗
║                    RESUMO DO PEDIDO                        ║
╚════════════════════════════════════════════════════════════╝

DADOS DO CLIENTE
┌─────────────────────────────────────────────────────────────
│ Nome: {self.__cliente.nome}
│ Email: {self.__cliente.email}
│ CPF: {self.__cliente.cpf}
└─────────────────────────────────────────────────────────────

ITENS DO PEDIDO
┌─────────────────────────────────────────────────────────────
"""
        
        for idx, item in enumerate(self.__itens, 1):
            resumo += f"│ {idx}. {item.produto.nome}\n"
            resumo += f"│    Quantidade: {item.quantidade} | Preço unitário: R$ {item.preco_unitario:.2f}\n"
            resumo += f"│    Subtotal: R$ {item.quantidade * item.preco_unitario:.2f}\n"
        
        resumo += "└─────────────────────────────────────────────────────────────\n\n"
        
        subtotal = sum(item.preco_unitario * item.quantidade for item in self.__itens)
        
        resumo += "VALORES\n"
        resumo += "┌─────────────────────────────────────────────────────────────\n"
        resumo += f"│ Subtotal: R$ {subtotal:.2f}\n"
        
        if self.__frete:
            resumo += f"│ Frete: R$ {self.__frete.valor:.2f} ({self.__frete.prazo_entrega} dias úteis)\n"
        
        if self.__cupom:
            desconto = self.__cupom.calcular_desconto(subtotal) if hasattr(self.__cupom, 'calcular_desconto') else 0.0
            resumo += f"│ Desconto ({self.__cupom.codigo}): -R$ {desconto:.2f}\n"
        
        total = self.calcular_total()
        resumo += f"│ TOTAL: R$ {total:.2f}\n"
        resumo += "└─────────────────────────────────────────────────────────────\n\n"
        
        if self.__endereco_entrega:
            resumo += "ENDEREÇO DE ENTREGA\n"
            resumo += "┌─────────────────────────────────────────────────────────────\n"
            resumo += f"│ {self.__endereco_entrega}\n"
            resumo += "└─────────────────────────────────────────────────────────────\n\n"
        
        resumo += f"Status: {self.status}\n"
        resumo += f"Criado em: {self.__criado_em.strftime('%d/%m/%Y %H:%M:%S')}\n"
        
        return resumo

    # MÉTODOS ESPECIAIS
    def __str__(self) -> str:
        """Representação textual do pedido"""
        total = self.calcular_total()
        return f"Pedido #{id(self)} - Status: {self.status} - Total: R$ {total:.2f} - {len(self.__itens)} itens"
    
    def __repr__(self) -> str:
        """Representação técnica do pedido"""
        return f"Pedido(cliente='{self.__cliente.nome}', itens={len(self.__itens)}, status='{self.status}', total=R${self.calcular_total():.2f})"