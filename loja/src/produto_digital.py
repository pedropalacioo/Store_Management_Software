import uuid

from produto import Produto


class ProdutoDigital(Produto):
    """Subclasse de Produto para itens digitais (não entram no frete)."""

    def __init__(self, nome: str, categoria: str, preco: float, estoque: int, ativo: bool, url_download: str, chave_licenca: str | None = None,):
        super().__init__(nome, categoria, preco, estoque, ativo)
        self.url_download = url_download
        self.chave_licenca = chave_licenca

    @property
    def url_download(self):
        return self.__url_download

    @url_download.setter
    def url_download(self, novo_url: str):
        if not isinstance(novo_url, str):
            raise TypeError("Error: url_download must be a string.")
        if not novo_url.strip():
            raise ValueError("Error: url_download cannot be empty.")
        self.__url_download = novo_url

    @property
    def chave_licenca(self):
        return self.__chave_licenca

    @chave_licenca.setter
    def chave_licenca(self, nova_licenca: str | None):
        if nova_licenca is not None and not isinstance(nova_licenca, str):
            raise TypeError("Error: chave_licenca must be a string or None.")
        self.__chave_licenca = nova_licenca

    def gerar_licenca(self):
        codigo = uuid.uuid4().hex.upper()[:16]  # 16 caracteres
        chave_formatada = "-".join([codigo[i:i+4] for i in range(0, 16, 4)])

        self.__chave_licenca = chave_formatada
        return chave_formatada        

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Tipo: DIGITAL | URL: {self.url_download}"

    def __repr__(self):
        return (
            f"ProdutoDigital(sku={self.sku!r}, nome={self.nome!r}, "
            f"categoria={self.categoria!r}, preco={self.preco!r}, "
            f"estoque={self.estoque!r}, ativo={self.ativo!r}, "
            f"url_download={self.url_download!r}, "
            f"chave_licenca={self.chave_licenca!r})"
        )

    
#Métodos planejados:
#__str__() FEITO
#__repr__() FEITO 
#gerar_licenca() FEITO
