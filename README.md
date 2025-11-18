# Store Management Software
*Projeto da cadeira de Programação Orientada à Objetos do curso de Engenharia de Software*

**Aluno: Pedro Yan Alcantara Palacio**
*Engenharia de Software - Universidade Federal do Cariri*

----

## 1. Objetivo do projeto: 
Desenvolver um **sistema simplificado de gerenciamento de loja virtual**, aplicando conceitos essenciais de **Programação Orientada a Objetos**:

----

## 2. UML Textual com estrutra das Classes:
| **Classe** | **Atributos Principais** | **Métodos Principais** |
|-----------|---------------------------|-------------------------|
| **Produto** | `sku`, `nome`, `categoria`, `_preco`, `_estoque`, `ativo` ou `inativo` | `preco/get/set`, `estoque/get/set`, `ajustar_estoque()`, `ativar()`, `inativar()`, `__str__()`, `__eq__()`, `__lt__()` |
| **ProdutoFisico** *Subclasse de produto* | herda `Produto` + `peso`, `altura`, `largura`, `profundidade` | herda de Produto + `calcular_cubagem()` |
| **ProdutoDigital** *Subclasse de Produto* | herda `Produto` + `url_download`, `chave_licenca` | herda de Produto + `gerar_licenca()` |
| **Cliente** | `id`, `nome`, `_email`, `_cpf`, `enderecos` | `email/get/set`, `cpf/get/set`, `adicionar_endereco()`, `remover_endereco()`, `__eq__()` |
| **Endereco** | `id`, `cep`, `cidade`, `uf`, `logradouro`, `numero`, `complemento` | `formatar()`, `validar_cep()` |
| **Carrinho** | `id`, `cliente`, `itens`, `cupom`, `criado_em` | `adicionar_item()`, `remover_item()`, `alterar_quantidade()`, `subtotal()`, `aplicar_cupom()`, `__len__()` |
| **ItemCarrinho** | `produto`, `_quantidade`, `preco_unitario` | `quantidade/get/set`, `subtotal()` |
| **Pedido** | `id`, `cliente`, `itens`, `frete`, `cupom`, `subtotal`, `desconto`, `valor_frete`, `total`, `status`, `endereco_entrega`, `criado_em`, `pago_em`, `enviado_em`, `entregue_em`, `cancelado_em`, `codigo_rastreio` | `criar_de_carrinho()`, `calcular_subtotal()`, `aplicar_cupom()`, `calcular_total()`, `aplicar_frete()`, `registrar_pagamento()`, `cancelar()`, `gerar_resumo_textual()`, `marcar_enviado()`, `marcar_entregue()` |
| **ItemPedido** | `produto` (ou `sku`, `nome` do produto), `quantidade`, `preco_unitario` | `total_item()` |
| **Pagamento** | `id`, `pedido`, `data_pagamento`, `forma`, `valor` | `validar_valor()`, `confirmar()`, `estornar()` |
| **Cupom** | `codigo`, `tipo`, `valor`, `data_validade`, `uso_maximo`, `usos_realizados`, `categorias_elegiveis` | `esta_valido()`, `aplicavel()`, `calcular_desconto()`, `registrar_uso()` |
| **Frete** | `uf`, `cidade`, `faixa_cep`, `valor`, `prazo_dias` | `calcular_frete()` |

----
# 2.1. Diagrama de Classes (UML):

*Representação visual da interação entre classes (simplificada)*

![UML](media/UML%20-%20Pedro%20Yan%20Alcantara%20Palacio.png)

----

## 3. Estrutura Planejada de Classes:
Abaixo estão as principais classes do domínio da loja virtual, com seus atributos, métodos e relacionamentos planejados.

---

### Classe `Produto`

- **Responsabilidade**: representar um produto vendável no sistema (base para produtos físicos e digitais).
- **Atributos principais**
  - `sku: str` — identificador único do produto.
  - `nome: str`
  - `categoria: str`
  - `_preco: float` — preço unitário (> 0), acessado via `@property`.
  - `_estoque: int` — quantidade em estoque (≥ 0), acessado via `@property`.
  - `ativo: bool` — indica se o produto está disponível para venda.
- **Métodos principais**
  - `preco` (getter/setter) — controla validação de preço.
  - `estoque` (getter/setter) — controla validação de estoque.
  - `ajustar_estoque(qtd: int)` — incrementa/decrementa estoque (com validações).
  - `ativar()` / `inativar()` — altera estado de disponibilidade.
  - `__str__()` — representação amigável do produto.
  - `__eq__(other)` — compara produtos por `sku`.
  - `__lt__(other)` — ordenação por preço ou nome.
- **Relacionamentos**
  - Referenciado por `ItemCarrinho` e `ItemPedido`.

---

### Classe `ProdutoFisico` (subclasse de `Produto`)

- **Responsabilidade**: especializar `Produto` para itens físicos, que exigem frete.
- **Atributos principais**
  - Herda todos de `Produto`.
  - `peso: float`
  - `altura: float`
  - `largura: float`
  - `profundidade: float`
- **Métodos principais**
  - Herda métodos de `Produto`.
  - `calcular_cubagem() -> float` — calcula volume/cubagem para cálculo de frete.
- **Relacionamentos**
  - Considerado no cálculo de frete em `Frete`.

---

### Classe `ProdutoDigital` (subclasse de `Produto`)

- **Responsabilidade**: representar produtos digitais que não possuem frete.
- **Atributos principais**
  - Herda todos de `Produto`.
  - `url_download: str`
  - `chave_licenca: str | None` — chave gerada no momento da compra.
- **Métodos principais**
  - Herda métodos de `Produto`.
  - `gerar_licenca()` — gera e associa uma chave de licença ao produto digital.
- **Relacionamentos**
  - Não impacta frete (produtos digitais não somam frete no pedido).

---

### Classe `Cliente`

- **Responsabilidade**: representar o cliente da loja, com dados de identificação e contato.
- **Atributos principais**
  - `id: int`
  - `nome: str`
  - `_email: str` — validado via `@property`.
  - `_cpf: str` — validado via `@property`.
  - `enderecos: list[Endereco]` — lista de endereços cadastrados.
- **Métodos principais**
  - `email` (getter/setter) — valida formato e unicidade de email.
  - `cpf` (getter/setter) — valida formato e unicidade de CPF.
  - `adicionar_endereco(endereco: Endereco)`
  - `remover_endereco(endereco: Endereco)`
  - `__eq__(other)` — compara clientes por CPF e/ou email.
- **Relacionamentos**
  - Possui vários `Endereco`.
  - Associado a `Carrinho` e `Pedido`.

---

### Classe `Endereco`

- **Responsabilidade**: representar um endereço de cliente para cadastro e entrega.
- **Atributos principais**
  - `id: int`
  - `cep: str`
  - `cidade: str`
  - `uf: str`
  - `logradouro: str`
  - `numero: str`
  - `complemento: str | None`
- **Métodos principais**
  - `formatar() -> str` — retorna endereço formatado.
  - `validar_cep() -> bool` — valida formato básico do CEP.
- **Relacionamentos**
  - Pertence a um `Cliente`.
  - Utilizado em `Pedido` como `endereco_entrega`.

---

### Classe `Carrinho`

- **Responsabilidade**: representar o carrinho de compras de um cliente antes de virar pedido.
- **Atributos principais**
  - `id: int`
  - `cliente: Cliente`
  - `itens: list[ItemCarrinho]`
  - `cupom: Cupom | None`
  - `criado_em: datetime`
- **Métodos principais**
  - `adicionar_item(produto: Produto, quantidade: int)`
  - `remover_item(produto: Produto)`
  - `alterar_quantidade(produto: Produto, nova_quantidade: int)`
  - `subtotal() -> float` — soma dos subtotais dos itens.
  - `aplicar_cupom(cupom: Cupom)` — tenta aplicar cupom ao carrinho.
  - `__len__()` — retorna quantidade total de itens (soma das quantidades).
- **Relacionamentos**
  - Possui vários `ItemCarrinho`.
  - Associado a um `Cliente`.
  - Serve de base para criar um `Pedido`.

---

### Classe `ItemCarrinho`

- **Responsabilidade**: representar um item dentro do carrinho (produto + quantidade).
- **Atributos principais**
  - `produto: Produto`
  - `_quantidade: int` — (≥ 1), acessada via `@property`.
  - `preco_unitario: float` — preço do produto no momento da adição.
- **Métodos principais**
  - `quantidade` (getter/setter) — controla validação de quantidade.
  - `subtotal() -> float` — `quantidade * preco_unitario`.
- **Relacionamentos**
  - Pertence a um `Carrinho`.

---

### Classe `Pedido`

- **Responsabilidade**: representar o pedido efetivado a partir de um carrinho.
- **Atributos principais**
  - `id: int`
  - `cliente: Cliente`
  - `itens: list[ItemPedido]`
  - `frete: Frete | None`
  - `cupom: Cupom | None`
  - `subtotal: float`
  - `desconto: float`
  - `valor_frete: float`
  - `total: float`
  - `status: str` — ex.: `"CRIADO"`, `"PAGO"`, `"ENVIADO"`, `"ENTREGUE"`, `"CANCELADO"`.
  - `endereco_entrega: Endereco`
  - `criado_em: datetime`
  - `pago_em: datetime | None`
  - `enviado_em: datetime | None`
  - `entregue_em: datetime | None`
  - `cancelado_em: datetime | None`
  - `codigo_rastreio: str | None`
- **Métodos principais**
  - `criar_de_carrinho(carrinho: Carrinho)` — constrói o pedido a partir do carrinho.
  - `calcular_subtotal() -> float`
  - `aplicar_cupom(cupom: Cupom)`
  - `calcular_total() -> float` — considera subtotal, desconto e frete.
  - `aplicar_frete(frete: Frete)`
  - `registrar_pagamento(pagamento: Pagamento)` — atualiza status/valores pagos e baixa estoque.
  - `cancelar()` — aplica regras de cancelamento e estorno de estoque.
  - `gerar_resumo_textual() -> str` — nota/resumo do pedido.
  - `marcar_enviado(codigo_rastreio: str)`
  - `marcar_entregue()`
- **Relacionamentos**
  - Possui vários `ItemPedido`.
  - Associado a um `Cliente`, um `Endereco` e um `Frete`.
  - Relacionado a um ou mais `Pagamento`.

---

### Classe `ItemPedido`

- **Responsabilidade**: representar um item faturado dentro do pedido.
- **Atributos principais**
  - `produto: Produto`  
    *(alternativamente armazenar `sku: str` e `nome: str` para histórico da época do pedido)*  
  - `quantidade: int`
  - `preco_unitario: float`
- **Métodos principais**
  - `total_item() -> float` — `quantidade * preco_unitario`.
- **Relacionamentos**
  - Pertence a um `Pedido`.

---

### Classe `Pagamento`

- **Responsabilidade**: representar um pagamento efetuado para um pedido.
- **Atributos principais**
  - `id: int`
  - `pedido: Pedido`
  - `data_pagamento: datetime`
  - `forma: str` — ex.: `"PIX"`, `"CREDITO"`, `"DEBITO"`, `"BOLETO"`.
  - `valor: float`
- **Métodos principais**
  - `validar_valor() -> bool` — valida se o valor é positivo e faz sentido para o pedido.
  - `confirmar()` — registra pagamento e interage com o estado do `Pedido`.
  - `estornar()` — caso seja necessário cancelamento com estorno.
- **Relacionamentos**
  - Associado a um `Pedido`.

---

### Classe `Cupom`

- **Responsabilidade**: representar cupons de desconto aplicáveis a carrinhos/pedidos.
- **Atributos principais**
  - `codigo: str`
  - `tipo: str` — `"VALOR"` ou `"PERCENTUAL"`.
  - `valor: float` — valor fixo ou percentual.
  - `data_validade: date`
  - `uso_maximo: int`
  - `usos_realizados: int`
  - `categorias_elegiveis: list[str]` — categorias de produtos elegíveis.
- **Métodos principais**
  - `esta_valido(hoje: date) -> bool`
  - `aplicavel(carrinho_ou_pedido) -> bool` — verifica regras de elegibilidade.
  - `calcular_desconto(subtotal: float) -> float`
  - `registrar_uso()` — incrementa contador de usos.
- **Relacionamentos**
  - Pode ser associado a `Carrinho` e `Pedido`.

---

### Classe `Frete`

- **Responsabilidade**: representar a configuração/resultado do cálculo de frete.
- **Atributos principais**
  - `uf: str`
  - `cidade: str`
  - `faixa_cep: str | None`
  - `valor: float`
  - `prazo_dias: int`
- **Métodos principais**
  - `calcular_frete(pedido: Pedido) -> float` — aplica regras com base em UF/cidade/CEP e, se necessário, peso/cubagem.
- **Relacionamentos**
  - Utilizado por `Pedido` para compor o valor final e prazo de entrega.


# 4. Estruturação Modular do Projeto(Prevista):
| 📁 **Arquivo / Camada** | 🎯 **Função** | 📌 **Contém** | 📌 **Status** |
|-------------------------|--------------|----------------|----------------|
| `README.md` | Documentação | introdução, UML, estrutura | ⏳ |
| `settings.json` | Configurações | fretes, descontos, etc. | ⏳ |
| `requirements.txt` | Dependências | libs futuras | ⏳ |
| `loja/` | Código fonte | módulos principais | ⏳ |
| `loja/models/` | Classes OO | produto, cliente, pedido, etc. | ⏳ |
| `loja/storage.py` | Persistência | JSON ou SQLite | ⏳ |
| `loja/services.py` | Regras de negócio | fluxos e validações | ⏳ |
| `loja/cli.py` | CLI | interface básica | ⏳ |
| `tests/` | Testes (pytest) | casos de erro e sucesso | ⏳ |

**Representação visual**

```text
STORE_MANAGEMENT_SOFTWARE/
├─ README.md                
├─ settings.json            
├─ requirements.txt          
│
├─ loja/                     
│  ├─ __init__.py
│  │
│  ├─ models/                
│  │  ├─ __init__.py
│  │  ├─ produto.py
│  │  ├─ cliente.py
│  │  ├─ endereco.py
│  │  ├─ carrinho.py
│  │  ├─ pedido.py
│  │  ├─ pagamento.py
│  │  ├─ cupom.py
│  │  └─ frete.py
│  │
│  ├─ storage.py            
│  ├─ services.py            
│  └─ cli.py                
│
└─ tests/                    
```

# 5. Checklist do Projeto — Sistema de Loja Virtual Simplificada

**Semana 1**
* [X] **UML Textual:** Classes, atributos, métodos e relacionamentos.
* [X] **README Inicial:** Descrição do projeto e estrutura planejada.
* [X] **Classes Iniciais:** Arquivos com classes vazias e docstrings.

**Semana 2**
* [ ] **Classes Base:** Produto, Cliente, Endereco, Carrinho, ItemCarrinho.
* [ ] **Encapsulamento:** Validações com `@property` e regras de negócio básicas.
* [ ] **Métodos Especiais:** __len__, __eq__, __repr__.
* [ ] **Testes Iniciais:** Criação e manipulação básica de objetos.

**Semana 3**
* [ ] **Herança e Relacionamentos:** Pedido, ItemPedido, Pagamento, Cupom, Frete.
* [ ] **Fechar Pedido:** Geração de pedido a partir do carrinho.
* [ ] **Persistência:** JSON ou SQLite + seed inicial.
* [ ] **Relatório Inicial:** Faturamento por período.

**Semana 4**
* [ ] **Regras de Negócio:** Estoque, cupons, frete, pagamento, cancelamento.
* [ ] **Integração:** CLI ou API mínima funcional.
* [ ] **Testes de Fluxos:** Cenários principais e erros esperados.

**Semana 5**
* [ ] **Relatórios Finais:** Faturamento, top N, ticket médio, vendas por UF/categoria.
* [ ] **Documentação Final:** README completo, instruções e diagrama final.
* [ ] **Qualidade:** Todos os testes passando.
* [ ] **Entrega:** Criar tag v1.0 no GitHub.
