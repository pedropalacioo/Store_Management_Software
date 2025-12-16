# Relatorio Final de Entrega

**Principais aprendizados**

- Conceitos de POO
- Fluxo básico entre regras de negócio e rotas da API
- Inicialização e operação em banco de dados (SQLite)

---

## Relato
Nas semanas iniciais de desenvolvimento do projeto, foi muito tranquilo aplicar os conceitos aprendidos em sala de aula no projeto (*inicialização de classes, atributos e métodos simples*). Contudo, entre a quarta e quinta semana de entrega, obtive muita dificuldade para dar continuidade ao projeto, o que me fez recomeçá-lo do zero utilizando uma linha de desenvolvimento diferente:

**Classe(atributos, métodos, etc.)** --> **Banco de dados (SQLite)** --> **API_routes**

Inicialmente, foquei em finalizar a estrutura necessária para o CRUD de Clientes e Produtos, e fazer dessa forma foi essencial para que eu entendesse melhor a integração e correlação entre as classes, banco de dados e rotas na API. Também aproveitei para reoganizar um pouco a estrutura modular do projeto já que estava achando muito complicada a estrutura passada.
Após finalizar toda a estrutura necessária para conseguir criar, ler, atualizar e deletar objetos das classes `Cliente` e `Produto`, comecei a reescrever cada classe necessária para dar o próximo passo no fluxo básico de compra. Desse modo, pude compreender como funciona a operabilidade de um banco de dados em SQLite. Uma das classes que possuem algumas diferenças é a `frete.py` que é uma @dataclass, basicamente uma classe focada em armazenamento de dados. A parte de regras de negócio relacionadas ao frete se encontram na file `services_frete.py`. depois de implementar toda a lógica necessária para fechamento de pedido, foquei em colocar validações dos atributos através das classes e no próprio banco de dados, através de `services_database.py`. 

Durante o desenvolvimento d projeto, utilizei ferramentas como o chatGPT e outras LLMs para solução de problemas principalmente relacionados à solução de bugs envolvendo rotas e bugs relacionados ao banco de Dados, mas fiz questão de escrever todas as classes (pelo menos 2x) incluindo seus métodos e atributos bem encapsulados.

Esse projeto foi bastante desafiador e exaustivo, mas também me motivou à querer aprender mais sobre funcionamento de APIs e boas práticas de código.

Pretendo adicionar docstrings eficientes no futuro, para facilitar a compreensão do código, e também desenvolver uma interface intuitiva que possibilite o teste das funcionalidades com representações visuais.