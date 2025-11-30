from produto import Produto


"Subclasse de Produto!"



class produto_digital(Produto):
    def __init__(self, nome: str, categoria: str, preco: float, estoque: int, ativo: bool, url_download: str, chave_licenca: str | None):
        super().__init__(nome, categoria, preco, estoque, ativo, url_download, chave_licenca)

        self.__url_download = url_download
        self.__chave_licenca = chave_licenca

#getters e setters

    @property
    def url_download(self):
        return self.__url_download
    
    @url_download.setter
    def url_download(self, novo_url):
        if not isinstance(novo_url, str):
            raise TypeError("Error: url must be a string.")
        self.__url_download = novo_url

    @property
    def chave_licenca(self):
        return self.__chave_licenca
    
    @chave_licenca.setter
    def chave_licenca(self, nova_licenca):
        if not isinstance(nova_licenca, str):
            raise TypeError("Error: licensa must be a string.")
        self.__chave_licenca = nova_licenca
    
#Métodos planejados:
#reescrever __str__() e __repr__()
#def gerar_licenca()
