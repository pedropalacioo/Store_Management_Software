import random
import string
from datetime import datetime
from core.pedido import Pedido


class Expedicao:
    """Controla o rastreio e entrega dos pedidos"""
    
    def __init__(self, pedido: Pedido):
        if not isinstance(pedido, Pedido):
            raise TypeError("Erro: pedido deve ser uma instância de Pedido.")
        
        self.__pedido = pedido
        self.__codigo_rastreio = None
        self.__data_envio = None
        self.__data_entrega = None
        self.__entregue = False
    
    # GETTERS
    @property
    def pedido(self) -> Pedido:
        return self.__pedido
    
    @property
    def codigo_rastreio(self) -> str | None:
        return self.__codigo_rastreio
    
    @property
    def data_envio(self) -> datetime | None:
        return self.__data_envio
    
    @property
    def data_entrega(self) -> datetime | None:
        return self.__data_entrega
    
    @property
    def entregue(self) -> bool:
        return self.__entregue
    
    # MÉTODOS
    def gerar_codigo_rastreio(self) -> str:
        """Gera um código de rastreio fictício
        
        Returns:
            str: Código de rastreio formatado (Ex: BR123456789012)
        """
        if self.__codigo_rastreio is not None:
            return self.__codigo_rastreio
        
        # Formato: BR + 12 caracteres alfanuméricos
        caracteres = string.ascii_uppercase + string.digits
        numero_aleatorio = ''.join(random.choice(caracteres) for _ in range(12))
        self.__codigo_rastreio = f"BR{numero_aleatorio}"
        
        return self.__codigo_rastreio
    
    def registrar_envio(self) -> None:
        """Registra o envio do pedido e atualiza seu status
        
        Raises:
            ValueError: Se o pedido não estiver PAGO
        """
        if self.__pedido.status != Pedido.STATUS_PAGO:
            raise ValueError(
                f"Erro: Pedido deve estar PAGO para ser enviado. Status atual: {self.__pedido.status}"
            )
        
        # Gerar código de rastreio
        self.gerar_codigo_rastreio()
        
        # Registrar data de envio
        self.__data_envio = datetime.now()
        
        # Atualizar status do pedido
        self.__pedido.atualizar_status(Pedido.STATUS_ENVIADO)
    
    def marcar_como_entregue(self, data_entrega: datetime | None = None) -> None:
        """Marca o pedido como entregue
        
        Args:
            data_entrega: Data da entrega (padrão: hoje)
        
        Raises:
            ValueError: Se o pedido não estiver ENVIADO
        """
        if self.__pedido.status != Pedido.STATUS_ENVIADO:
            raise ValueError(
                f"Erro: Pedido deve estar ENVIADO para ser entregue. Status atual: {self.__pedido.status}"
            )
        
        self.__data_entrega = data_entrega or datetime.now()
        self.__entregue = True
        
        # Atualizar status do pedido
        self.__pedido.atualizar_status(Pedido.STATUS_ENTREGUE)
    
    def gerar_resumo_rastreio(self) -> str:
        """Gera um resumo do rastreio
        
        Returns:
            str: Resumo formatado do rastreio
        """
        resumo = f"""
╔════════════════════════════════════════════════════════════╗
║                   RASTREIO DO PEDIDO                       ║
╚════════════════════════════════════════════════════════════╝

Código de Rastreio: {self.__codigo_rastreio or 'Não gerado'}
Status: {self.__pedido.status}

Histórico:
┌─────────────────────────────────────────────────────────────
│ Criado em: {self.__pedido.criado_em.strftime('%d/%m/%Y %H:%M:%S')}
"""
        
        if self.__data_envio:
            resumo += f"│ Enviado em: {self.__data_envio.strftime('%d/%m/%Y %H:%M:%S')}\n"
        
        if self.__data_entrega:
            resumo += f"│ Entregue em: {self.__data_entrega.strftime('%d/%m/%Y %H:%M:%S')}\n"
        
        resumo += "└─────────────────────────────────────────────────────────────\n"
        
        return resumo
