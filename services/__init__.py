"""
Módulo de serviços da aplicação.

Contém regras de negócio e operações complexas que não pertencem ao domínio (core).
"""

from services.services_frete import ServicoFrete
from services.services_relatorios import ServicosRelatorios

__all__ = ['ServicoFrete', 'ServicosRelatorios']
