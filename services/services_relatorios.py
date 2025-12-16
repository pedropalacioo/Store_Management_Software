"""
Lógica para geração de relatórios:
- relatório de ocupação
- top N produtos
- faturamento de pedido
"""

from core.pedido import Pedido
from core.produto import Produto
from core.item_pedido import ItemPedido

from typing import List, Dict, Tuple, Any
from datetime import datetime, date
from collections import Counter
from pathlib import Path
import json


# Caminho para o settings.json
SETTINGS_PATH = Path(__file__).resolve().parent.parent / "settings" / "settings.json"

# Cache em memória para as configurações
_SETTINGS_CACHE: Dict[str, Any] | None = None


def carregar_settings_relatorios() -> Dict[str, Any]:
    """Carrega as configurações de relatórios do arquivo settings.json"""
    global _SETTINGS_CACHE
    if _SETTINGS_CACHE is None:
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                _SETTINGS_CACHE = json.load(f)
        except FileNotFoundError:
            # Se settings.json não existir, usar valores padrão
            _SETTINGS_CACHE = {
                "relatorios": {
                    "top_n_produtos": 5
                }
            }
    return _SETTINGS_CACHE.get("relatorios", {})


def obter_top_n_produtos() -> int:
    """Obtém o número de produtos para top N baseado em settings.json"""
    config = carregar_settings_relatorios()
    return config.get("top_n_produtos", 5)


class ServicosRelatorios:
    """Serviço de negócio para operações complexas com relatórios."""

    @staticmethod
    def gerar_relatorio_ocupacao(pedidos: List[Pedido]) -> Dict[str, Any]:
        """
        Gera relatório de ocupação dos pedidos por status.
        
        Args:
            pedidos: Lista de pedidos para analisar
            
        Returns:
            Dicionário com distribuição de status
        """
        if not pedidos:
            return {
                "total_pedidos": 0,
                "distribuicao_status": {},
                "percentual_status": {},
                "pedidos_ativos": 0,
                "pedidos_finalizados": 0
            }
        
        # Contar pedidos por status
        distribuicao = Counter(p.status for p in pedidos)
        
        # Calcular percentuais
        total = len(pedidos)
        percentual = {
            status: round((count / total) * 100, 2)
            for status, count in distribuicao.items()
        }
        
        # Contar pedidos ativos e finalizados
        pedidos_ativos = sum(
            1 for p in pedidos 
            if p.status not in [Pedido.STATUS_ENTREGUE, Pedido.STATUS_CANCELADO]
        )
        pedidos_finalizados = sum(
            1 for p in pedidos 
            if p.status in [Pedido.STATUS_ENTREGUE, Pedido.STATUS_CANCELADO]
        )
        
        return {
            "total_pedidos": total,
            "distribuicao_status": dict(distribuicao),
            "percentual_status": percentual,
            "pedidos_ativos": pedidos_ativos,
            "pedidos_finalizados": pedidos_finalizados,
            "taxa_entrega": round((sum(1 for p in pedidos if p.status == Pedido.STATUS_ENTREGUE) / total) * 100, 2) if total > 0 else 0,
            "taxa_cancelamento": round((sum(1 for p in pedidos if p.status == Pedido.STATUS_CANCELADO) / total) * 100, 2) if total > 0 else 0
        }

    @staticmethod
    def gerar_relatorio_top_produtos(pedidos: List[Pedido]) -> List[Dict[str, Any]]:
        """
        Gera relatório dos top N produtos mais vendidos.
        N é definido em settings.json (padrão: 5)
        
        Args:
            pedidos: Lista de pedidos para analisar
            
        Returns:
            Lista com top N produtos ordenados por quantidade vendida
        """
        if not pedidos:
            return []
        
        # Contar quantidade vendida por produto
        contador_produtos = Counter()
        faturamento_produto = {}
        
        for pedido in pedidos:
            # Apenas considerar pedidos entregues ou pagos
            if pedido.status in [Pedido.STATUS_ENTREGUE, Pedido.STATUS_PAGO, Pedido.STATUS_ENVIADO]:
                for item in pedido.itens:
                    sku = item.produto.sku
                    contador_produtos[sku] += item.quantidade
                    
                    if sku not in faturamento_produto:
                        faturamento_produto[sku] = {
                            "nome": item.produto.nome,
                            "total": 0.0,
                            "quantidade": 0
                        }
                    
                    faturamento_produto[sku]["total"] += item.preco_unitario * item.quantidade
                    faturamento_produto[sku]["quantidade"] += item.quantidade
        
        # Obter top N do settings
        top_n = obter_top_n_produtos()
        
        # Criar lista de top produtos
        top_produtos = []
        for sku, quantidade in contador_produtos.most_common(top_n):
            if sku in faturamento_produto:
                info = faturamento_produto[sku]
                top_produtos.append({
                    "sku": sku,
                    "nome": info["nome"],
                    "quantidade_vendida": quantidade,
                    "faturamento": info["total"],
                    "preco_medio": round(info["total"] / quantidade, 2) if quantidade > 0 else 0.0
                })
        
        return top_produtos

    @staticmethod
    def gerar_relatorio_faturamento_pedido(pedido: Pedido) -> Dict[str, Any]:
        """
        Gera relatório detalhado de faturamento de um pedido.
        
        Args:
            pedido: Pedido para gerar faturamento
            
        Returns:
            Dicionário com detalhes de faturamento
        """
        # Calcular valores
        subtotal = pedido.calcular_subtotal()
        total = pedido.calcular_total()
        
        # Desconto (cupom)
        desconto = 0.0
        desconto_cupom = ""
        if pedido.cupom:
            desconto = pedido.cupom.calcular_desconto(subtotal) if hasattr(pedido.cupom, 'calcular_desconto') else 0.0
            desconto_cupom = f"({pedido.cupom.codigo})"
        
        # Frete
        frete = 0.0
        if pedido.frete:
            frete = pedido.frete.valor
        
        # Detalhes de itens
        itens_detalhes = []
        for item in pedido.itens:
            itens_detalhes.append({
                "sku": item.produto.sku,
                "nome": item.produto.nome,
                "categoria": item.produto.categoria,
                "quantidade": item.quantidade,
                "preco_unitario": item.preco_unitario,
                "subtotal": item.quantidade * item.preco_unitario
            })
        
        return {
            "pedido_id": id(pedido),
            "cliente": pedido.cliente.nome if pedido.cliente else "Desconhecido",
            "status": pedido.status,
            "criado_em": pedido.criado_em.strftime("%d/%m/%Y %H:%M:%S"),
            "itens": itens_detalhes,
            "quantidade_itens": len(pedido.itens),
            "subtotal": round(subtotal, 2),
            "desconto": round(desconto, 2),
            "cupom": desconto_cupom if desconto > 0 else "Nenhum",
            "frete": round(frete, 2),
            "total": round(total, 2),
            "detalhamento": {
                "subtotal_itens": round(subtotal, 2),
                "menos_desconto": f"-R$ {desconto:.2f}" if desconto > 0 else "R$ 0.00",
                "mais_frete": f"+R$ {frete:.2f}" if frete > 0 else "R$ 0.00",
                "total_final": round(total, 2)
            }
        }

    @staticmethod
    def gerar_relatorio_faturamento_periodo(
        pedidos: List[Pedido],
        data_inicio: date | None = None,
        data_fim: date | None = None
    ) -> Dict[str, Any]:
        """
        Gera relatório de faturamento em um período.
        
        Args:
            pedidos: Lista de pedidos
            data_inicio: Data inicial (inclusive)
            data_fim: Data final (inclusive)
            
        Returns:
            Dicionário com faturamento do período
        """
        if not pedidos:
            return {
                "periodo": f"{data_inicio} a {data_fim}" if data_inicio and data_fim else "Sem período",
                "total_pedidos": 0,
                "faturamento_bruto": 0.0,
                "total_descontos": 0.0,
                "total_frete": 0.0,
                "faturamento_liquido": 0.0,
                "ticket_medio": 0.0
            }
        
        # Filtrar por período se fornecido
        pedidos_filtrados = pedidos
        if data_inicio or data_fim:
            pedidos_filtrados = [
                p for p in pedidos
                if (not data_inicio or p.criado_em.date() >= data_inicio) and
                   (not data_fim or p.criado_em.date() <= data_fim)
            ]
        
        # Apenas pedidos pagos/entregues
        pedidos_processados = [
            p for p in pedidos_filtrados
            if p.status in [Pedido.STATUS_PAGO, Pedido.STATUS_ENVIADO, Pedido.STATUS_ENTREGUE]
        ]
        
        if not pedidos_processados:
            return {
                "periodo": f"{data_inicio} a {data_fim}" if data_inicio and data_fim else "Sem período",
                "total_pedidos": 0,
                "faturamento_bruto": 0.0,
                "total_descontos": 0.0,
                "total_frete": 0.0,
                "faturamento_liquido": 0.0,
                "ticket_medio": 0.0
            }
        
        # Calcular totais
        faturamento_bruto = 0.0
        total_descontos = 0.0
        total_frete = 0.0
        
        for pedido in pedidos_processados:
            subtotal = pedido.calcular_subtotal()
            faturamento_bruto += subtotal
            
            if pedido.cupom and hasattr(pedido.cupom, 'calcular_desconto'):
                total_descontos += pedido.cupom.calcular_desconto(subtotal)
            
            if pedido.frete:
                total_frete += pedido.frete.valor
        
        faturamento_liquido = faturamento_bruto - total_descontos + total_frete
        ticket_medio = faturamento_liquido / len(pedidos_processados) if pedidos_processados else 0.0
        
        return {
            "periodo": f"{data_inicio} a {data_fim}" if data_inicio and data_fim else "Sem período definido",
            "total_pedidos": len(pedidos_processados),
            "faturamento_bruto": round(faturamento_bruto, 2),
            "total_descontos": round(total_descontos, 2),
            "total_frete": round(total_frete, 2),
            "faturamento_liquido": round(faturamento_liquido, 2),
            "ticket_medio": round(ticket_medio, 2)
        }

    @staticmethod
    def gerar_relatorio_resumo_vendas(pedidos: List[Pedido]) -> str:
        """
        Gera um resumo textual completo de vendas.
        
        Args:
            pedidos: Lista de pedidos
            
        Returns:
            String com relatório formatado
        """
        relatorio_ocupacao = ServicosRelatorios.gerar_relatorio_ocupacao(pedidos)
        relatorio_faturamento = ServicosRelatorios.gerar_relatorio_faturamento_periodo(pedidos)
        top_produtos = ServicosRelatorios.gerar_relatorio_top_produtos(pedidos)
        
        linhas = [
            "=" * 70,
            "RELATÓRIO GERAL DE VENDAS",
            "=" * 70,
            "",
            "📊 OCUPAÇÃO DOS PEDIDOS",
            "─" * 70,
            f"Total de pedidos: {relatorio_ocupacao['total_pedidos']}",
            f"Pedidos ativos: {relatorio_ocupacao['pedidos_ativos']}",
            f"Pedidos finalizados: {relatorio_ocupacao['pedidos_finalizados']}",
            f"Taxa de entrega: {relatorio_ocupacao['taxa_entrega']}%",
            f"Taxa de cancelamento: {relatorio_ocupacao['taxa_cancelamento']}%",
            "",
            "Distribuição por status:",
        ]
        
        for status, count in relatorio_ocupacao['distribuicao_status'].items():
            percentual = relatorio_ocupacao['percentual_status'].get(status, 0)
            linhas.append(f"  • {status}: {count} ({percentual}%)")
        
        linhas.extend([
            "",
            "💰 FATURAMENTO",
            "─" * 70,
            f"Faturamento bruto: R$ {relatorio_faturamento['faturamento_bruto']:.2f}",
            f"Total de descontos: -R$ {relatorio_faturamento['total_descontos']:.2f}",
            f"Total de frete: +R$ {relatorio_faturamento['total_frete']:.2f}",
            f"Faturamento líquido: R$ {relatorio_faturamento['faturamento_liquido']:.2f}",
            f"Ticket médio: R$ {relatorio_faturamento['ticket_medio']:.2f}",
            "",
            f"🏆 TOP {obter_top_n_produtos()} PRODUTOS MAIS VENDIDOS",
            "─" * 70,
        ])
        
        if top_produtos:
            for i, produto in enumerate(top_produtos, 1):
                linhas.append(
                    f"{i}. {produto['nome']} (SKU: {produto['sku']})"
                )
                linhas.append(
                    f"   Quantidade: {produto['quantidade_vendida']} | "
                    f"Faturamento: R$ {produto['faturamento']:.2f}"
                )
        else:
            linhas.append("Nenhum produto vendido")
        
        linhas.extend([
            "",
            "=" * 70,
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            "=" * 70
        ])
        
        return "\n".join(linhas)
