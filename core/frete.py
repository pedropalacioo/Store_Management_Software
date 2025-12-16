from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
import json

# Caminho para o settings.json
SETTINGS_PATH = Path(__file__).resolve().parent.parent / "settings" / "settings.json"

# Cache em memória para as configurações
_SETTINGS_CACHE: Dict[str, Any] | None = None

def carregar_settings() -> Dict[str, Any]:
    """Carrega as configurações do arquivo settings.json"""
    global _SETTINGS_CACHE
    if _SETTINGS_CACHE is None:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            _SETTINGS_CACHE = json.load(f)
    return _SETTINGS_CACHE

@dataclass
class Frete:
    uf: str
    cep: str
    valor: float
    prazo_entrega: int

    @classmethod
    def from_frete(cls, uf: str) -> Frete:
        if not isinstance(uf, str) or len(uf) != 2:
            raise ValueError("Erro: UF deve ser uma string de 2 caracteres.")
        
        uf = uf.strip().upper()
        if len(uf) != 2:
            raise ValueError("Erro: UF deve ter exatamente 2 caracteres.")
        
        settings = carregar_settings()
        config_frete: Dict[str, Any] = settings.get("frete", {})

        uf_origem = config_frete.get("uf_origem", "CE")

        tabela_frete_uf: Dict[str, Any] = config_frete.get("tabela_frete_uf", {})
        configuracao_padrao: Dict[str, Any] = config_frete.get("default", {})

        dados_uf = tabela_frete_uf.get(uf)

        if dados_uf is not None:
            valor_entrega = float(dados_uf.get("valor", configuracao_padrao.get("valor", 0.0)))
            prazo_entrega = int(dados_uf.get("prazo", configuracao_padrao.get("prazo", 0)))
        else:
            #utiliza os valores padrão.
            valor_entrega = float(configuracao_padrao.get("valor", 0.0))
            prazo_entrega = int(configuracao_padrao.get("prazo", 0))
        
        return cls(
            uf=uf,
            cep="",
            valor=valor_entrega,
            prazo_entrega=prazo_entrega,
        )
    
    @classmethod
    def from_cliente(cls, cliente) -> Frete:
        if not hasattr(cliente, "endereco"):
            raise ValueError("Erro: cliente não possui atributo 'endereco'.")
        
        enderecos = cliente.endereco

        if not isinstance(enderecos, list) or  not enderecos:
            raise ValueError("Erro: cliente não possui endereços cadastrados.") 
        
        endereco_principal = enderecos[0]

        if not hasattr(endereco_principal, "uf"):
            raise AttributeError("Erro: endereço do cliente não possui atributo 'uf'.")
        
        uf_cliente = endereco_principal.uf
        return cls.from_frete(uf_cliente)

    def __str__(self) -> str:
        return (
            f"Frete(uf_origem='{self.uf}', uf_destino='{self.uf}', "
            f"valor={self.valor:.2f}, prazo_entrega={self.prazo_entrega} dias)"
        )
    
    def __repr__(self) -> str:
        return (
            f"Frete(uf_origem='{self.uf}', uf_destino='{self.uf}', "
            f"valor={self.valor:.2f}, prazo_entrega={self.prazo_entrega} dias)"
        )
    
    
        
