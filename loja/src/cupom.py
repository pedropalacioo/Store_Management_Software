from __future__ import annotations
from datetime import date, datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pedido import Pedido

class Cupom:

    TIPO_VALOR = "VALOR"
    TIPO_PERCENTUAL = "PERCENTUAL"
    TIPO_FRETE_GRATIS = "FRETE_GRATIS"

    TIPOS_VALIDOS = {TIPO_VALOR, TIPO_PERCENTUAL, TIPO_FRETE_GRATIS}

    def __init__(
        self, codigo: str, tipo: str, valor: float, data_validade: Optional[date], 
        uso_maximo: int = 1, usos_realizados: int = 0, categ_elegiveis: Optional[List[str]] = None):
        self.codigo = codigo
        self.tipo = tipo
        self.valor = valor
        self.data_validade = data_validade
        self.uso_maximo = uso_maximo
        self.usos_realizados = usos_realizados
        self.categorias_elegiveis = categ_elegiveis if categ_elegiveis is not None else []

    # ============== PROPRIEDADES ==============

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, novo_codigo: str) -> None:
        if not isinstance(novo_codigo, str):
            raise TypeError("Error: codigo must be a string.")
        if not novo_codigo.strip():
            raise ValueError("Error: codigo cannot be empty.")
        self.__codigo = novo_codigo.strip().upper()

    @property
    def tipo(self) -> str:
        return self.__tipo

    @tipo.setter
    def tipo(self, novo_tipo: str) -> None:
        if not isinstance(novo_tipo, str):
            raise TypeError("Error: tipo must be a string.")
        novo_tipo = novo_tipo.upper()
        if novo_tipo not in self.TIPOS_VALIDOS:
            raise ValueError("Error: tipo must be 'VALOR' or 'PERCENTUAL' or 'FRETE_GRATIS'.")
        self.__tipo = novo_tipo

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, novo_valor: float) -> None:
        if not isinstance(novo_valor, (int, float)):
            raise TypeError("Error: valor must be a number.")
        
        if getattr(self, "_Cupom__tipo", None) == self.TIPO_FRETE_GRATIS:
            if novo_valor < 0:
                raise ValueError("Error: valor must be greater or equal to 0 for FRETE_GRATIS.")
            self.__valor = float(novo_valor)
            return

        if novo_valor <= 0:
            raise ValueError("Error: valor must be greater than 0.")
        
        #limitador de percentual
        if getattr(self, "_Cupom__tipo", None) == self.TIPO_PERCENTUAL and novo_valor > 100:
            raise ValueError("Error: percentual must be above or equal to 100%.")
        self.__valor = float(novo_valor)

    @property
    def data_validade(self) -> Optional[date]:
        return self.__data_validade

    @data_validade.setter
    def data_validade(self, nova_data) -> None:
        """
        Aceita:
        - date
        - datetime (usa apenas a parte de data)
        - str no formato ISO 'YYYY-MM-DD'
        - None (sem validade)
        """
        if nova_data is None:
            self.__data_validade = None
            return

        if isinstance(nova_data, datetime):
            self.__data_validade = nova_data.date()
            return

        if isinstance(nova_data, date):
            self.__data_validade = nova_data
            return

        if isinstance(nova_data, str):
            try:
                self.__data_validade = date.fromisoformat(nova_data)
                return
            except ValueError as exc:
                raise ValueError("Error: data_validade string must be in 'YYYY-MM-DD' format.") from exc

        raise TypeError("Error: data_validade must be a date, datetime, ISO string or None.")

    @property
    def uso_maximo(self) -> int:
        return self.__uso_maximo

    @uso_maximo.setter
    def uso_maximo(self, novo_uso_maximo: int) -> None:
        if not isinstance(novo_uso_maximo, int):
            raise TypeError("Error: uso_maximo must be an integer.")
        if novo_uso_maximo <= 0:
            raise ValueError("Error: uso_maximo must be at least 1.")
        self.__uso_maximo = novo_uso_maximo

    @property
    def usos_realizados(self) -> int:
        return self.__usos_realizados

    @usos_realizados.setter
    def usos_realizados(self, novo_uso: int) -> None:
        if not isinstance(novo_uso, int):
            raise TypeError("Error: usos_realizados must be an integer.")
        if novo_uso < 0:
            raise ValueError("Error: usos_realizados cannot be negative.")
        if hasattr(self, "_Cupom__uso_maximo") and novo_uso > self.__uso_maximo:
            raise ValueError("Error: usos_realizados cannot be greater than uso_maximo.")
        self.__usos_realizados = novo_uso

    @property
    def categorias_elegiveis(self) -> List[str]:
        return self.__categ_elegiveis

    @categorias_elegiveis.setter
    def categorias_elegiveis(self, novas_categorias: List[str]) -> None:
        if not isinstance(novas_categorias, list):
            raise TypeError("Error: categorias_elegiveis must be a list.")
        if not all(isinstance(cat, str) for cat in novas_categorias):
            raise TypeError("Error: every categoria must be a string.")
        # normaliza para maiúsculo e tira espaços
        self.__categ_elegiveis = [cat.strip().upper() for cat in novas_categorias if cat.strip()]

    # ============== MÉTODOS PRINCIPAIS ==============

    def esta_valido(self, data_referencia: Optional[date] = None) -> bool:
        """
        Verifica se o cupom ainda é válido considerando:
        - data de validade (se existir)
        - limite de uso_maximo
        """
        if data_referencia is None:
            data_referencia = date.today()

        # Verifica validade por data
        if self.data_validade is not None and data_referencia > self.data_validade:
            return False

        # Verifica limite de uso
        if self.usos_realizados >= self.uso_maximo:
            return False

        return True

    def aplicavel(self, categoria: Optional[str]) -> bool:
        """
        Verifica se o cupom pode ser aplicado a uma categoria específica.
        - Se categorias_elegiveis estiver vazia -> aplicável a qualquer categoria.
        """
        if not self.categorias_elegiveis:
            return True  # sem restrição de categoria

        if categoria is None:
            # se há restrição de categorias e nenhuma categoria foi informada, considera não aplicável
            return False

        return categoria.strip().lower() in self.categorias_elegiveis

    def calcular_desconto(
        self,
        subtotal: float,
        categoria: Optional[str] = None,
        data_referencia: Optional[date] = None,
        valor_frete: float = 0.0
    ) -> float:
        """
        Calcula o valor de desconto a partir do subtotal.

        Regras:
        - Se o cupom não estiver válido (data/uso) -> 0
        - Se a categoria não for elegível -> 0
        - TIPO_VALOR: desconto fixo sobre o subtotal
        - TIPO_PERCENTUAL: percentual sobre o subtotal
        - TIPO_FRETE_GRATIS: desconto em cima do valor do frete
        - Desconto nunca pode tornar o total (subtotal + frete) negativo.
        """
        if not isinstance(subtotal, (int, float)):
            raise TypeError("Error: subtotal must be a number.")
        if not isinstance(valor_frete, (int, float)):
            raise TypeError("Error: valor_frete must be a number.")
        
        subtotal = float(subtotal)
        valor_frete = float(valor_frete)

        if subtotal <= 0 and valor_frete <= 0:
            return 0.0

        if not self.esta_valido(data_referencia=data_referencia):
            return 0.0

        if not self.aplicavel(categoria):
            return 0.0

        if self.tipo == self.TIPO_VALOR:
            desconto = self.valor
            
        elif self.tipo == self.TIPO_PERCENTUAL:
            desconto = subtotal * (self.valor / 100.0)

        elif self.tipo == self.TIPO_FRETE_GRATIS:
            # Se valor == 0 -> frete totalmente grátis
            if self.valor <= 0:
                desconto = valor_frete
            else:
                desconto = min(self.valor, valor_frete)

        else:
            desconto = 0.0

        # Impede desconto maior que subtotal + frete
        desconto_maximo = max(0.0, subtotal + valor_frete)
        desconto = max(0.0, min(desconto, desconto_maximo))

        return desconto
    
    # INTERAÇÃO COM PEDIDO

    def esta_valido_para_pedido(
            self,
            pedido: "Pedido",
            data_referencia: Optional[date] = None,
    ) -> bool:
        """
        Validação completa levando em conta o Pedido:

        - Cupom válido por data/uso (esta_valido)
        - Se houver categorias_elegiveis, exige que pelo menos
          UM item do pedido tenha categoria permitida.
        """
        if not self.esta_valido(data_referencia=data_referencia):
            return False
        
        if not self.categorias_elegiveis:
            return True
        
        categorias_itens = set()

        for item in getattr(pedido, "itens", []):
            produto = getattr(item, "produto", None)
            categoria = getattr(produto, "categoria", None)
            if isinstance(categoria, str):
                categorias_itens.add(categoria.strip().upper())

        if not categorias_itens:
            return False
        
        return any(cat in self.categorias_elegiveis for cat in categorias_itens)
    
    def calcular_desconto_para_pedido(
            self,
            pedido: "Pedido",
            data_referencia: Optional[date] = None,
    ) -> float:
        """
        Calcula o desconto considerando o Pedido inteiro.

        Regras:
        - Exige cupom válido por data/uso + categorias (esta_valido_para_pedido).
        - Desconto é calculado com base no SUBTOTAL total.
        - Para TIPO_FRETE_GRATIS, também considera o valor do frete do pedido
          (se existir em pedido.frete).
        """
        # 1) Obter subtotal
        subtotal = getattr(pedido, "subtotal", None)
        if subtotal is None:
            calcular = getattr(pedido, "calcular_subtotal", None)
            if callable(calcular):
                subtotal = calcular()
            else:
                raise AttributeError(
                    "Pedido must have 'subtotal' attribute or 'calcular_subtotal()' method."
                )

        # Obter valor_frete (suporta float ou objeto Frete com atributo 'valor')
        valor_frete = 0.0
        frete = getattr(pedido, "frete", None)
        if isinstance(frete, (int, float)):
            valor_frete = float(frete)
        elif frete is not None and hasattr(frete, "valor"):
            valor_frete = float(frete.valor)

        # Validação completa para o pedido (data/uso + categorias)
        if not self.esta_valido_para_pedido(pedido, data_referencia=data_referencia):
            return 0.0

        # Calcular desconto sem categoria específica (já validada)
        desconto = self.calcular_desconto(
            subtotal=subtotal,
            categoria=None,
            data_referencia=data_referencia,
            valor_frete=valor_frete,
        )

        return desconto


    def registrar_uso(self) -> None:
        """
        Incrementa o número de usos do cupom.
        Lança erro se o cupom já atingiu o limite.
        """
        if self.usos_realizados >= self.uso_maximo:
            raise ValueError("Error: coupon usage limit reached.")
        self.usos_realizados = self.usos_realizados + 1

    # ============== REPRESENTAÇÃO ==============

    def __repr__(self) -> str:
        return (
            f"Cupom(codigo='{self.codigo}', tipo='{self.tipo}', valor={self.valor}, "
            f"data_validade={self.data_validade}, uso_maximo={self.uso_maximo}, "
            f"usos_realizados={self.usos_realizados}, categorias_elegiveis={self.categorias_elegiveis})"
        )
