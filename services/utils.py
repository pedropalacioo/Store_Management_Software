"""
Funções utilitárias para formatação e limpeza de dados
"""

def limpar_cpf(cpf: str) -> str:
    """
    Remove formatação do CPF, deixando apenas dígitos.
    Aceita CPFs formatados (ex: "123.456.789-10") ou não formatados (ex: "12345678910")
    
    Args:
        cpf (str): CPF formatado ou não
        
    Returns:
        str: CPF com apenas 11 dígitos
        
    Raises:
        ValueError: Se o CPF não contiver exatamente 11 dígitos após limpeza
    """
    if not isinstance(cpf, str):
        raise TypeError("CPF deve ser uma string")
    
    # Remove caracteres de formatação
    cpf_limpo = cpf.replace(".", "").replace("-", "").strip()
    
    # Valida se tem 11 dígitos
    if len(cpf_limpo) != 11:
        raise ValueError(f"CPF deve conter exatamente 11 dígitos, recebido: {cpf}")
    
    if not cpf_limpo.isdigit():
        raise ValueError(f"CPF deve conter apenas dígitos, recebido: {cpf}")
    
    return cpf_limpo


def limpar_cep(cep: str) -> str:
    """
    Remove formatação do CEP, deixando apenas dígitos.
    Aceita CEPs formatados (ex: "01310-100") ou não formatados (ex: "01310100")
    
    Args:
        cep (str): CEP formatado ou não
        
    Returns:
        str: CEP com apenas 8 dígitos
        
    Raises:
        ValueError: Se o CEP não contiver exatamente 8 dígitos após limpeza
    """
    if not isinstance(cep, str):
        raise TypeError("CEP deve ser uma string")
    
    # Remove caracteres de formatação
    cep_limpo = cep.replace("-", "").replace(" ", "").strip()
    
    # Valida se tem 8 dígitos
    if len(cep_limpo) != 8:
        raise ValueError(f"CEP deve conter exatamente 8 dígitos, recebido: {cep}")
    
    if not cep_limpo.isdigit():
        raise ValueError(f"CEP deve conter apenas dígitos, recebido: {cep}")
    
    return cep_limpo
