from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from cliente import Cliente
from carrinho import Carrinho
from item_pedido import ItemPedido
from cupom import Cupom
from frete import Frete

# Import só para o type checker (não roda em tempo de execução)
if TYPE_CHECKING:
    from pagamento import Pagamento


class Pedido:
    STATUS_CRIADO = "CRIADO"
    STATUS_PENDENTE_PAGAMENTO = "PENDENTE_PAGAMENTO"
    STATUS_PAGO_PARCIAL = "PAGO_PARCIAL"
    STATUS_PAGO = "PAGO"
    STATUS_ENVIADO = "ENVIADO"
    STATUS_ENTREGUE = "ENTREGUE"
    STATUS_CANCELADO = "CANCELADO"

    def __init__(
        self,
        cliente: Cliente,
        itens: List[ItemPedido],
        frete: Optional[Frete] = None,
        cupom: Optional[Cupom] = None,
        endereco_entrega: Optional[object] = None,
        status: str = STATUS_CRIADO,
        criado_em: Optional[datetime] = None,
    ):
        # ID
        self.__id = self._gerar_id()

        # Atributos principais
        self.__cliente: Cliente = None  # type: ignore
        self.__itens: List[ItemPedido] = []
        self.__frete: Optional[Frete] = None
        self.__cupom: Optional[Cupom] = None

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
        if self.__cupom:
            self.aplicar_cupom(self.__cupom)
        self._atualizar_valor_frete()
        self.calcular_total()

    # ===================== ID =====================

    @property
    def id(self) -> int:
        return self.__id

    def _gerar_id(self) -> int:
        return uuid.uuid4().int % 10000

    # ===================== CLIENTE =====================

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @cliente.setter
    def cliente(self, novo_cliente: Cliente) -> None:
        if not isinstance(novo_cliente, Cliente):
            raise TypeError("Error: cliente must be a Cliente object.")
        self.__cliente = novo_cliente

    # ===================== ITENS =====================

    @property
    def itens(self) -> List[ItemPedido]:
        return self.__itens

    @itens.setter
    def itens(self, novos_itens: List[ItemPedido]) -> None:
        if not isinstance(novos_itens, list):
            raise TypeError("Error: itens must be a list.")
        if len(novos_itens) == 0:
            raise ValueError("Error: pedido must have at least one item.")
        if not all(isinstance(i, ItemPedido) for i in novos_itens):
            raise TypeError("Error: itens must contain only ItemPedido objects.")
        self.__itens = novos_itens

    # ===================== FRETE =====================

    @property
    def frete(self) -> Optional[Frete]:
        return self.__frete

    @frete.setter
    def frete(self, novo_frete: Optional[Frete]) -> None:
        if novo_frete is not None and not isinstance(novo_frete, Frete):
            raise TypeError("Error: frete must be a Frete object or None.")
        self.__frete = novo_frete
        self._atualizar_valor_frete()

    def _atualizar_valor_frete(self) -> None:
        if self.__frete is None:
            self.__valor_frete = 0.0
        else:
            self.__valor_frete = float(getattr(self.__frete, "valor", 0.0))

    # ===================== CUPOM =====================

    @property
    def cupom(self) -> Optional[Cupom]:
        return self.__cupom

    @cupom.setter
    def cupom(self, novo_cupom: Optional[Cupom]) -> None:
        if novo_cupom is not None and not isinstance(novo_cupom, Cupom):
            raise TypeError("Error: cupom must be a Cupom object or None.")
        self.__cupom = novo_cupom

    # ===================== SUBTOTAL =====================

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    @subtotal.setter
    def subtotal(self, novo_subtotal: float) -> None:
        if not isinstance(novo_subtotal, (int, float)):
            raise TypeError("Error: subtotal must be a number.")
        if novo_subtotal < 0:
            raise ValueError("Error: subtotal must be >= 0.")
        self.__subtotal = float(novo_subtotal)

    # ===================== DESCONTOS =====================

    @property
    def descontos(self) -> float:
        return self.__descontos

    @descontos.setter
    def descontos(self, novo_desconto: float) -> None:
        if not isinstance(novo_desconto, (int, float)):
            raise TypeError("Error: descontos must be a number.")
        if novo_desconto < 0:
            raise ValueError("Error: descontos must be >= 0.")
        self.__descontos = float(novo_desconto)

    # ===================== VALOR FRETE =====================

    @property
    def valor_frete(self) -> float:
        return self.__valor_frete

    @valor_frete.setter
    def valor_frete(self, valor: float) -> None:
        if not isinstance(valor, (int, float)):
            raise TypeError("Error: valor_frete must be a number.")
        if valor < 0:
            raise ValueError("Error: valor_frete must be >= 0.")
        self.__valor_frete = float(valor)

    # ===================== TOTAL =====================

    @property
    def total(self) -> float:
        return self.__total

    @total.setter
    def total(self, novo_total: float) -> None:
        if not isinstance(novo_total, (int, float)):
            raise TypeError("Error: total must be a number.")
        if novo_total < 0:
            raise ValueError("Error: total must be >= 0.")
        self.__total = float(novo_total)

    # ===================== STATUS =====================

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, novo_status: str) -> None:
        estados_validos = {
            self.STATUS_CRIADO,
            self.STATUS_PENDENTE_PAGAMENTO,
            self.STATUS_PAGO_PARCIAL,
            self.STATUS_PAGO,
            self.STATUS_ENVIADO,
            self.STATUS_ENTREGUE,
            self.STATUS_CANCELADO,
        }
        if novo_status not in estados_validos:
            raise ValueError(f"Error: status must be one of {estados_validos}.")
        self.__status = novo_status

    # ===================== ENDEREÇO ENTREGA =====================

    @property
    def endereco_entrega(self):
        return self.__endereco_entrega

    @endereco_entrega.setter
    def endereco_entrega(self, endereco) -> None:
        self.__endereco_entrega = endereco

    # ===================== DATAS =====================

    @property
    def criado_em(self) -> datetime:
        return self.__criado_em

    @property
    def pago_em(self) -> Optional[datetime]:
        return self.__pago_em

    @pago_em.setter
    def pago_em(self, data: Optional[datetime]) -> None:
        if data is not None and not isinstance(data, datetime):
            raise TypeError("Error: pago_em must be a datetime or None.")
        self.__pago_em = data

    @property
    def enviado_em(self) -> Optional[datetime]:
        return self.__enviado_em

    @enviado_em.setter
    def enviado_em(self, data: Optional[datetime]) -> None:
        if data is not None and not isinstance(data, datetime):
            raise TypeError("Error: enviado_em must be a datetime or None.")
        self.__enviado_em = data

    @property
    def entregue_em(self) -> Optional[datetime]:
        return self.__entregue_em

    @entregue_em.setter
    def entregue_em(self, data: Optional[datetime]) -> None:
        if data is not None and not isinstance(data, datetime):
            raise TypeError("Error: entregue_em must be a datetime or None.")
        self.__entregue_em = data

    @property
    def cancelado_em(self) -> Optional[datetime]:
        return self.__cancelado_em

    @cancelado_em.setter
    def cancelado_em(self, data: Optional[datetime]) -> None:
        if data is not None and not isinstance(data, datetime):
            raise TypeError("Error: cancelado_em must be a datetime or None.")
        self.__cancelado_em = data

    # ===================== CÓDIGO RASTREIO =====================

    @property
    def codigo_rastreio(self) -> Optional[str]:
        return self.__codigo_rastreio

    @codigo_rastreio.setter
    def codigo_rastreio(self, codigo: Optional[str]) -> None:
        if codigo is not None and not isinstance(codigo, str):
            raise TypeError("Error: codigo_rastreio must be a string or None.")
        self.__codigo_rastreio = codigo

    def _gerar_codigo_rastreio(self) -> str:
        return uuid.uuid4().hex[:12].upper()

    # ===================== PAGAMENTOS =====================

    @property
    def pagamentos(self) -> List[Pagamento]:
        return list(self.__pagamentos)

    @property
    def total_pago(self) -> float:
        return float(self.__total_pago)

    @property
    def valor_em_aberto(self) -> float:
        aberto = self.__total - self.__total_pago
        return aberto if aberto > 0 else 0.0

    # ===================== MÉTODOS PRINCIPAIS =====================

    @classmethod
    def criar_de_carrinho(
        cls,
        carrinho: Carrinho,
        frete: Optional[Frete] = None,
        cupom: Optional[Cupom] = None,
        endereco_entrega: Optional[object] = None,
    ) -> "Pedido":
        if not carrinho.itens:
            raise ValueError("Error: carrinho vazio não pode virar pedido.")

        itens_pedido: List[ItemPedido] = []
        for item_carrinho in carrinho.itens:
            produto = item_carrinho.produto
            quantidade = item_carrinho.quantidade
            preco_unitario = produto.preco

            itens_pedido.append(
                ItemPedido(
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario,
                )
            )

        pedido = cls(
            cliente=carrinho.cliente,
            itens=itens_pedido,
            frete=frete,
            cupom=cupom,
            endereco_entrega=endereco_entrega,
        )
        return pedido

    def calcular_subtotal(self) -> float:
        subtotal = 0.0
        for item in self.__itens:
            if hasattr(item, "subtotal"):
                subtotal += float(item.subtotal)
            else:
                preco = float(getattr(item, "preco_unitario", 0.0))
                qtd = int(getattr(item, "quantidade", 0))
                subtotal += preco * qtd

        self.__subtotal = round(subtotal, 2)
        return self.__subtotal

    def aplicar_cupom(self, cupom: Cupom) -> float:
        self.__cupom = cupom
        desconto = cupom.calcular_desconto_para_pedido(self)
        self.__descontos = round(desconto, 2)

        self.calcular_total()

        if self.__descontos > 0:
            cupom.registrar_uso()

        return self.__descontos

    def calcular_total(self) -> float:
        total = self.__subtotal - self.__descontos + self.__valor_frete
        if total < 0:
            total = 0.0
        self.__total = round(total, 2)
        return self.__total

    def aplicar_teste(self) -> bool:
        self.calcular_subtotal()
        if self.__cupom is not None:
            self.aplicar_cupom(self.__cupom)
        self._atualizar_valor_frete()
        self.calcular_total()
        return True

    # ===================== PAGAMENTOS: REGISTRO / ESTORNO =====================

    def registrar_pagamento(self, pagamento: Pagamento) -> None:
        from pagamento import Pagamento as PagamentoCls
        if not isinstance(pagamento, PagamentoCls):
            raise TypeError("Error: pagamento must be a Pagamento object.")

        if getattr(pagamento, "estornado", False):
            raise ValueError("Error: cannot register a refunded payment.")

        if pagamento in self.__pagamentos:
            return

        self.__pagamentos.append(pagamento)
        self.__total_pago += float(pagamento.valor)

        self.__atualizar_status_pos_pagamento(pagamento.data_pagamento)

    def registrar_estorno(self, pagamento: Pagamento) -> None:
        from pagamento import Pagamento as PagamentoCls
        if not isinstance(pagamento, PagamentoCls):
            raise TypeError("Error: pagamento must be a Pagamento object.")

        if pagamento not in self.__pagamentos:
            return

        self.__total_pago -= float(pagamento.valor)
        if self.__total_pago < 0:
            self.__total_pago = 0.0

        self.__atualizar_status_pos_pagamento()

    def __atualizar_status_pos_pagamento(
        self,
        data_pagamento: Optional[datetime] = None,
    ) -> None:
        if self.__status == self.STATUS_CANCELADO:
            return

        old_status = self.__status

        if self.__total_pago <= 0:
            new_status = self.STATUS_PENDENTE_PAGAMENTO
            novo_pago_em = None
        elif self.__total_pago < self.__total:
            new_status = self.STATUS_PAGO_PARCIAL
            novo_pago_em = None
        else:
            new_status = self.STATUS_PAGO
            novo_pago_em = data_pagamento or datetime.now()

        if old_status != self.STATUS_PAGO and new_status == self.STATUS_PAGO:
            self._baixar_estoque()
        elif old_status == self.STATUS_PAGO and new_status != self.STATUS_PAGO:
            self._estornar_estoque()

        self.status = new_status
        self.__pago_em = novo_pago_em

    # ===================== CANCELAR / ENVIAR / ENTREGAR =====================

    def cancelar(self) -> None:
        if self.__status not in (
            self.STATUS_CRIADO,
            self.STATUS_PENDENTE_PAGAMENTO,
            self.STATUS_PAGO_PARCIAL,
            self.STATUS_PAGO,
        ):
            raise ValueError(
                "Error: pedido só pode ser cancelado se estiver "
                "CRIADO, PENDENTE_PAGAMENTO, PAGO_PARCIAL ou PAGO."
            )

        if self.__status == self.STATUS_PAGO:
            self._estornar_estoque()

        self.status = self.STATUS_CANCELADO
        self.__cancelado_em = datetime.now()

    def marcar_enviado(self, codigo_rastreio: Optional[str] = None) -> None:
        if self.__status != self.STATUS_PAGO:
            raise ValueError("Error: só é possível enviar pedidos pagos.")

        self.status = self.STATUS_ENVIADO
        self.__enviado_em = datetime.now()
        self.__codigo_rastreio = codigo_rastreio or self._gerar_codigo_rastreio()

    def marcar_entregue(self, data_entrega: Optional[datetime] = None) -> None:
        if self.__status != self.STATUS_ENVIADO:
            raise ValueError("Error: só é possível marcar como entregue se estiver ENVIADO.")

        self.status = self.STATUS_ENTREGUE
        self.__entregue_em = data_entrega or datetime.now()

    # ===================== RESUMO / STR / REPR =====================

    def gerar_resumo_textual(self) -> str:
        linhas = []
        linhas.append(f"Pedido #{self.__id} - Status: {self.__status}")
        linhas.append(f"Cliente: {self.__cliente.nome} (CPF: {self.__cliente.cpf})")

        if self.__endereco_entrega is not None:
            linhas.append(f"Endereço de entrega: {self.__endereco_entrega}")

        linhas.append("Itens:")
        for item in self.__itens:
            produto = getattr(item, "produto", None)
            nome_produto = getattr(produto, "nome", "Produto")
            qtd = getattr(item, "quantidade", 0)
            preco_unit = getattr(item, "preco_unitario", 0.0)
            subtotal_item = preco_unit * qtd
            linhas.append(
                f" - {nome_produto} x{qtd} = R$ {subtotal_item:.2f}"
            )

        linhas.append(f"Subtotal: R$ {self.__subtotal:.2f}")
        linhas.append(f"Descontos: -R$ {self.__descontos:.2f}")
        linhas.append(f"Frete: R$ {self.__valor_frete:.2f}")
        linhas.append(f"Total: R$ {self.__total:.2f}")
        linhas.append(f"Total pago: R$ {self.__total_pago:.2f}")
        linhas.append(f"Valor em aberto: R$ {self.valor_em_aberto:.2f}")

        if self.__codigo_rastreio:
            linhas.append(f"Código de rastreio: {self.__codigo_rastreio}")

        return "\n".join(linhas)

    def __str__(self) -> str:
        return (
            f"Pedido #{self.__id} - Cliente: {self.__cliente.nome} - "
            f"Total: R$ {self.__total:.2f} - Status: {self.__status}"
        )

    def __repr__(self) -> str:
        return (
            f"Pedido(id={self.__id}, cliente={self.__cliente!r}, "
            f"total={self.__total:.2f}, status='{self.__status}')"
        )

    # ===================== ESTOQUE =====================

    def _baixar_estoque(self) -> None:
        for item in self.__itens:
            produto = item.produto
            quantidade = item.quantidade

            estoque_atual = getattr(produto, "estoque", None)
            if estoque_atual is None:
                raise AttributeError("'Produto' doesn't have 'estoque' attribute.")

            if quantidade > estoque_atual:
                raise ValueError(
                    f"Estoque insuficiente para o produto {produto.nome}: "
                    f"solicitado {quantidade}, disponível {estoque_atual}."
                )

        for item in self.__itens:
            produto = item.produto
            produto.estoque = produto.estoque - item.quantidade

    def _estornar_estoque(self) -> None:
        for item in self.__itens:
            produto = item.produto
            estoque_atual = getattr(produto, "estoque", None)
            if estoque_atual is None:
                raise AttributeError("'Produto' doesn't have 'estoque' attribute.")
            produto.estoque = estoque_atual + item.quantidade
