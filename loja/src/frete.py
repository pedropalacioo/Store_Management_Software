from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
import json


# Caminho para o settings.json (ajuste se estiver em outro lugar)
SETTINGS_PATH = Path(__file__).resolve().parent.parent / "settings.json"

# Cache simples em memória
_SETTINGS_CACHE: Dict[str, Any] | None = None


def carregar_settings() -> Dict[str, Any]:
    """
    Carrega as configurações do arquivo settings.json.
    Usa cache para evitar reabrir o arquivo o tempo todo.
    """
    global _SETTINGS_CACHE

    if _SETTINGS_CACHE is None:
        if not SETTINGS_PATH.exists():
            raise FileNotFoundError(f"settings.json not found at: {SETTINGS_PATH}")

        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            _SETTINGS_CACHE = json.load(f)

    return _SETTINGS_CACHE


@dataclass
class Frete:
    """
    Representa as informações de frete de um pedido.

    Atributos:
    - uf_origem: UF do centro de distribuição (ex.: 'CE')
    - uf_destino: UF do cliente
    - valor: valor do frete em R$
    - prazo_dias: prazo estimado em dias úteis
    """
    uf_origem: str
    uf_destino: str
    valor: float
    prazo_dias: int

    @classmethod
    def from_uf_destino(cls, uf_destino: str) -> Frete:
        """
        Cria um objeto Frete apenas com base na UF de destino,
        usando as configurações do settings.json.
        """
        if not isinstance(uf_destino, str):
            raise TypeError("Error: uf_destino must be a string.")

        uf_destino = uf_destino.strip().upper()
        if len(uf_destino) != 2:
            raise ValueError("Error: uf_destino must have 2 characters (e.g., 'CE').")

        settings = carregar_settings()
        cfg_frete: Dict[str, Any] = settings.get("frete", {})

        uf_origem = cfg_frete.get("uf_origem", "CE")

        tabela_por_uf: Dict[str, Any] = cfg_frete.get("tabela_por_uf", {})
        default_cfg: Dict[str, Any] = cfg_frete.get("default", {})

        dados_uf = tabela_por_uf.get(uf_destino)

        if dados_uf is not None:
            valor = float(dados_uf.get("valor", default_cfg.get("valor", 0.0)))
            prazo = int(dados_uf.get("prazo", default_cfg.get("prazo", 0)))
        else:
            # UF não encontrada, usa valores padrão
            valor = float(default_cfg.get("valor", 0.0))
            prazo = int(default_cfg.get("prazo", 0))

        return cls(
            uf_origem=uf_origem,
            uf_destino=uf_destino,
            valor=valor,
            prazo_dias=prazo,
        )

    @classmethod
    def from_cliente(cls, cliente) -> Frete:
        """
        Calcula o frete a partir de um objeto Cliente.

        Suposições:
        - cliente.endereco é uma lista de Endereco
        - Endereco possui atributo/propriedade 'uf'
        """
        if not hasattr(cliente, "endereco"):
            raise AttributeError("Error: cliente has no attribute 'endereco'.")

        enderecos = cliente.endereco

        if not isinstance(enderecos, list) or not enderecos:
            raise ValueError("Error: cliente.endereco must be a non-empty list of Endereco objects.")

        endereco_principal = enderecos[0]

        if not hasattr(endereco_principal, "uf"):
            raise AttributeError("Error: Endereco object must have attribute 'uf'.")

        uf_destino = endereco_principal.uf
        return cls.from_uf_destino(uf_destino)

    def __repr__(self) -> str:
        return (
            f"Frete(uf_origem='{self.uf_origem}', "
            f"uf_destino='{self.uf_destino}', "
            f"valor={self.valor:.2f}, "
            f"prazo_dias={self.prazo_dias})"
        )


"""
    Métodos planejados:
    - calcular_frete()

    Utilizado por pedido para compor o valor final e prazo de entrega
"""