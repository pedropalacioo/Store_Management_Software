import random
import string

from core.produto import Produto


class ProdutoDigital(Produto):
    """Produto digital com URL de download e chave de licença"""
    
    def __init__(
            self,
            nome: str,
            descricao: str,
            preco: float,
            url_download: str,
            chave_licenca: str | None = None,
            estoque: int = 0,
            sku: str | None = None,
    ):
        super().__init__(nome, descricao, preco, "digital", estoque, sku)
        self.__url_download = None
        self.__chave_licenca = None

        self.url_download = url_download
        self.chave_licenca = chave_licenca

    # URL DE DOWNLOAD: GETTER E SETTER
    @property
    def url_download(self) -> str:
        return self.__url_download
    
    @url_download.setter
    def url_download(self, nova_url: str) -> None:
        if not isinstance(nova_url, str):
            raise TypeError("Erro: URL de download não é uma string.")
        if not nova_url.strip():
            raise ValueError("Erro: URL de download não pode estar vazia.")
        self.__url_download = nova_url

    # CHAVE DE LICENÇA: GETTER E SETTER
    @property
    def chave_licenca(self) -> str | None:
        return self.__chave_licenca
    
    @chave_licenca.setter
    def chave_licenca(self, nova_chave: str | None) -> None:
        if nova_chave is not None:
            if not isinstance(nova_chave, str):
                raise TypeError("Erro: chave de licença não é uma string.")
            if not nova_chave.strip():
                raise ValueError("Erro: chave de licença não pode estar vazia.")
        self.__chave_licenca = nova_chave

    # MÉTODOS
    def gerar_chave_licenca(self) -> str:
        """Gera uma chave de licença aleatória de 16 caracteres"""
        caracteres = string.ascii_uppercase + string.digits
        chave = ''.join(random.choice(caracteres) for _ in range(16))
        self.chave_licenca = chave
        return chave
    
    def __str__(self) -> str:
        licenca_info = f"com licença" if self.chave_licenca else "sem licença"
        return (
            f"Produto Digital: {self.nome} | "
            f"Preço: R$ {self.preco:.2f} | "
            f"{licenca_info}"
        )
