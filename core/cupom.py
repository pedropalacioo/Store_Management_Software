from datetime import date, datetime, timedelta
from typing import List, Optional, TYPE_CHECKING, Dict, Any
from pathlib import Path
import json


# Caminho para o settings.json
SETTINGS_PATH = Path(__file__).resolve().parent.parent / "settings" / "settings.json"

# Cache em memória para as configurações
_SETTINGS_CACHE: Dict[str, Any] | None = None


def carregar_settings_cupom() -> Dict[str, Any]:
    """Carrega as configurações de cupom do arquivo settings.json"""
    global _SETTINGS_CACHE
    if _SETTINGS_CACHE is None:
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                _SETTINGS_CACHE = json.load(f)
        except FileNotFoundError:
            # Se settings.json não existir, usar valores padrão
            _SETTINGS_CACHE = {
                "cupons": {
                    "validade_padrao_dias": 30,
                    "uso_maximo_padrao": 100
                }
            }
    return _SETTINGS_CACHE.get("cupons", {})


def obter_validade_padrao() -> date:
    """Obtém a data de validade padrão baseada em settings.json"""
    config_cupom = carregar_settings_cupom()
    dias = config_cupom.get("validade_padrao_dias", 30)
    return date.today() + timedelta(days=dias)


def obter_uso_maximo_padrao() -> int:
    """Obtém o uso máximo padrão baseado em settings.json"""
    config_cupom = carregar_settings_cupom()
    return config_cupom.get("uso_maximo_padrao", 100)


class Cupom:

    TIPO_VALOR = "VALOR"
    TIPO_PERCENTUAL = "PERCENTUAL"
    TIPO_FRETE_GRATIS = "FRETE_GRATIS"

    TIPOS_VALIDOS = {TIPO_VALOR, TIPO_PERCENTUAL, TIPO_FRETE_GRATIS}

    def __init__(
            self,
            codigo: str,
            tipo: str,
            valor: float,
            data_validade: Optional[date] = None,
            uso_maximo: Optional[int] = None,
            usos_realizados: int = 0,
            categorias_elegiveis: Optional[list[str]] | None = None,
    ):
        self.__codigo = None
        self.__tipo = None
        self.__valor = None
        self.__data_validade = None
        self.__uso_maximo = None
        self.__usos_realizados = None
        self.__categorias_elegiveis = None

        self.codigo = codigo
        self.tipo = tipo
        self.valor = valor
        
        # Se data_validade não for fornecida, usa o padrão do settings
        if data_validade is None:
            self.data_validade = obter_validade_padrao()
        else:
            self.data_validade = data_validade
        
        # Se uso_maximo não for fornecido, usa o padrão do settings
        if uso_maximo is None:
            self.uso_maximo = obter_uso_maximo_padrao()
        else:
            self.uso_maximo = uso_maximo
        
        self.usos_realizados = usos_realizados
        self.categorias_elegiveis = categorias_elegiveis

    # CÓDIGO: GETTER E SETTER
    @property
    def codigo(self) -> str:
        return self.__codigo
    
    @codigo.setter
    def codigo(self, novo_codigo: str) -> None:
        if not isinstance(novo_codigo, str):
            raise TypeError("Erro: código do cupom não é uma string.")
        if not novo_codigo.strip():
            raise ValueError("Erro: código do cupom não pode estar vazio.")
        self.__codigo = novo_codigo

    # TIPO: GETTER E SETTER
    @property
    def tipo(self) -> str:
        return self.__tipo
    
    @tipo.setter
    def tipo(self, novo_tipo: str) -> None:
        if not isinstance(novo_tipo, str):
            raise TypeError("Erro: tipo do cupom não é uma string.")
        if novo_tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Erro: tipo do cupom deve ser um dos seguintes: {self.TIPOS_VALIDOS}.")
        self.__tipo = novo_tipo

    # VALOR: GETTER E SETTER
    @property
    def valor(self) -> float:
        return self.__valor
    
    @valor.setter
    def valor(self, novo_valor: float) -> None:
        if not isinstance(novo_valor, (float, int)):
            raise TypeError("Erro: valor do cupom não é um número.")
        
        if novo_valor < 0:
            raise ValueError("Erro: valor do cupom não pode ser negativo.")
        
        # Cupom de frete grátis deve ter valor zero.
        if getattr(self, 'tipo', None) == self.TIPO_FRETE_GRATIS and novo_valor != 0:
            raise ValueError("Erro: cupom de FRETE_GRATIS deve ter valor igual a zero.")
        
        # Cupom percentual não pode ter valor maior que 100.
        if getattr(self, 'tipo', None) == self.TIPO_PERCENTUAL and novo_valor > 100:
            raise ValueError("Erro: cupom percentual não pode ter valor maior que 100.")
        self.__valor = float(novo_valor)
    
    # DATA DE VALIDADE: GETTER E SETTER
    @property
    def data_validade(self) -> Optional[date]:
        return self.__data_validade
    
    @data_validade.setter
    def data_validade(self, nova_data: Optional[date]) -> None:
        if nova_data is None:
            self.__data_validade = None
            return
        
        if isinstance(nova_data, datetime):
            nova_data = nova_data.date()
            return
        
        if isinstance(nova_data, date):
            self.__data_validade = nova_data
            return

        if isinstance(nova_data, str):
            try:
                self.__data_validade = date.fromisoformat(nova_data)
                return
            except ValueError as exc:
                raise ValueError("Erro: data de validade em formato inválido. Use 'YYYY-MM-DD'.") from exc
        
        raise TypeError("Erro: data de validade deve ser do tipo date, datetime, string no formato 'YYYY-MM-DD' ou None.")
    
    # USO MÁXIMO: GETTER E SETTER
    @property
    def uso_maximo(self) -> int:
        return self.__uso_maximo
    
    @uso_maximo.setter
    def uso_maximo(self, novo_uso_maximo: int) -> None:
        if not isinstance(novo_uso_maximo, int):
            raise TypeError("Erro: uso máximo não é um inteiro.")
        if novo_uso_maximo <= 0:
            raise ValueError("Erro: uso máximo deve ser maior que zero.")
        self.__uso_maximo = novo_uso_maximo

    # USOS REALIZADOS: GETTER E SETTER
    @property
    def usos_realizados(self) -> int:
        return self.__usos_realizados
    
    @usos_realizados.setter
    def usos_realizados(self, novos_usos_realizados: int) -> None:
        if not isinstance(novos_usos_realizados, int):
            raise TypeError("Erro: usos realizados não é um inteiro.")
        if novos_usos_realizados < 0:
            raise ValueError("Erro: usos realizados não pode ser negativo.")
        if novos_usos_realizados > self.uso_maximo:
            raise ValueError("Erro: usos realizados não pode ser maior que o uso máximo.")
        self.__usos_realizados = novos_usos_realizados

    # CATEGORIAS ELEGÍVEIS: GETTER E SETTER
    @property
    def categorias_elegiveis(self) -> Optional[list[str]]:
        return self.__categorias_elegiveis
    
    @categorias_elegiveis.setter
    def categorias_elegiveis(self, novas_categorias: List[str]) -> None:
        if not isinstance(novas_categorias, list):
            raise TypeError("Error: categorias_elegiveis must be a list.")
        if not all(isinstance(cat, str) for cat in novas_categorias):
            raise TypeError("Error: every categoria must be a string.")
        # normaliza para maiúsculo e tira espaços
        self.__categorias_elegiveis = [cat.strip().upper() for cat in novas_categorias if cat.strip()]

    # MÉTODOS

    def esta_valido(self, data_validade: Optional[date] = None) -> bool:
        """Verifica se o cupom está válido com base na data de validade."""
        if data_validade is None:
            data_validade = date.today()
        
        if self.data_validade is None:
            return True  # Cupom sem data de validade é sempre válido.
        
        if self.usos_realizados >= self.uso_maximo:
            return False  # Cupom já atingiu o uso máximo.
        
        return True if data_validade <= self.data_validade else False
    
    def aplicavel(self, categoria_produto: Optional[str]) -> bool:
        """Verifica se o cupom é aplicável a uma determinada categoria de produto."""
        if self.categorias_elegiveis is None or not self.categorias_elegiveis:
            return True  # Cupom aplicável a todas as categorias.
        
        return categoria_produto.strip().upper() in self.categorias_elegiveis
    