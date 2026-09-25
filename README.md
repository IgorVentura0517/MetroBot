## Autores: Erick Ventura Gamberini - 03099001; Igor Ventura - 1722540; Fernando Alves Landim - 1794239

# 🚇 MetrôBot SP

> **O LLM conversa. O algoritmo decide.**

O **MetrôBot SP** é uma aplicação de planejamento de rotas para o Metrô de São Paulo que combina **grafos, algoritmos de busca, regras lógicas, API REST, interface web e Large Language Models (LLMs)**.

O sistema permite calcular rotas entre estações, identificar baldeações, considerar estações ou linhas indisponíveis e interpretar solicitações escritas em linguagem natural.

Exemplo:

```text
Quero sair da Pinacoteca e ir para Tatuapé.
```

O sistema interpreta a solicitação, associa a **Pinacoteca** à estação **Luz**, calcula deterministicamente a rota sobre o grafo do metrô, identifica as trocas de linha necessárias e utiliza um LLM para apresentar o resultado de maneira natural.

A principal decisão arquitetural do projeto é:

```text
LLM → interpreta
Algoritmo → calcula
LLM → explica
```

> O modelo de linguagem **não decide a rota**. O cálculo permanece sob responsabilidade dos algoritmos e das regras implementadas no core da aplicação.

---

## 📌 Funcionalidades

- Representação de múltiplas linhas do metrô
- Modelagem da rede utilizando grafos
- Busca de rotas com **BFS**
- Busca de rotas com **DFS**
- Identificação automática de baldeações
- Minimização de trocas desnecessárias entre linhas
- Suporte a estações bloqueadas
- Suporte a linhas indisponíveis
- Associação de pontos de interesse a estações
- Normalização das entradas do usuário
- Interpretação de linguagem natural com LLM
- Geração de respostas amigáveis com LLM
- API REST utilizando FastAPI
- Interface web em HTML, CSS e JavaScript
- Documentação automática via Swagger/OpenAPI
- Testes automatizados com pytest
- Gerenciamento da chave da API através de variável de ambiente

---

# 🏗️ Arquitetura

O projeto utiliza uma arquitetura modular em camadas, separando interface, API, inteligência artificial, regras de negócio, algoritmos e dados.

```text
                         USUÁRIO
                            │
                            ▼
                ┌─────────────────────┐
                │      FRONTEND       │
                │                     │
                │   HTML + CSS + JS   │
                └──────────┬──────────┘
                           │
                           │ HTTP / JSON
                           ▼
                ┌─────────────────────┐
                │       FastAPI       │
                │                     │
                │   /rota    /chat    │
                └──────────┬──────────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      ┌──────────────┐            ┌──────────────┐
      │ Planejador   │            │ Intérprete   │
      │              │            │     LLM      │
      └──────┬───────┘            └──────┬───────┘
             │                           │
             │                    origem/destino
             │                           │
             └─────────────┬─────────────┘
                           ▼
                ┌─────────────────────┐
                │        CORE         │
                │                     │
                │ Grafo               │
                │ BFS / DFS           │
                │ Regras              │
                │ Baldeações          │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Resultado da rota  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Narrador LLM     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │       FastAPI       │
                └──────────┬──────────┘
                           │
                           ▼
                        FRONTEND
```

Essa separação mantém a lógica crítica de roteamento independente do modelo generativo.

---

# 🧠 Princípio central: o LLM não calcula a rota

Uma das principais características do projeto é a separação entre **inteligência generativa** e **lógica determinística**.

Considere a mensagem:

```text
Quero sair da Pinacoteca e ir para Tatuapé.
```

O LLM é responsável por transformar a mensagem em dados estruturados:

```json
{
  "origem": "Pinacoteca",
  "destino": "Tatuapé",
  "algoritmo": "bfs"
}
```

A partir desse ponto, o cálculo passa para o core da aplicação.

O sistema resolve:

```text
Pinacoteca
    ↓
Luz
```

Em seguida, o algoritmo calcula a rota:

```text
Luz
→ São Bento
→ Sé
→ Pedro II
→ Brás
→ Bresser-Mooca
→ Belém
→ Tatuapé
```

Depois, o sistema identifica a baldeação:

```text
Sé
Linha 1-Azul → Linha 3-Vermelha
```

Somente então o resultado calculado é entregue novamente ao LLM para ser apresentado em linguagem natural.

O fluxo pode ser resumido como:

```text
LINGUAGEM NATURAL
        ↓
       LLM
        ↓
DADOS ESTRUTURADOS
        ↓
  ALGORITMOS
        ↓
RESULTADO DETERMINÍSTICO
        ↓
       LLM
        ↓
RESPOSTA NATURAL
```

---

# 🗺️ Modelagem da rede como grafo

A rede do metrô é representada através de um grafo:

```text
G = (V, E)
```

Onde:

- **V** representa o conjunto de vértices
- **E** representa o conjunto de arestas

No MetrôBot:

```text
Vértice = estação
Aresta   = ligação entre estações consecutivas
```

Por exemplo:

```text
Luz ─── São Bento ─── Sé
```

pode ser representado internamente como:

```python
{
    "Luz": ["São Bento"],
    "São Bento": ["Luz", "Sé"],
    "Sé": ["São Bento"]
}
```

A rede é tratada essencialmente como um **grafo não direcionado**, já que os deslocamentos podem ocorrer nos dois sentidos das linhas modeladas.

---

# 🚇 Linhas modeladas

A versão atual trabalha com:

- 🔵 **Linha 1 — Azul**
- 🟢 **Linha 2 — Verde**
- 🔴 **Linha 3 — Vermelha**

As linhas são armazenadas como listas ordenadas de estações.

Exemplo conceitual:

```python
LINHAS = {
    "azul": [...],
    "verde": [...],
    "vermelha": [...]
}
```

A partir dessas listas, o sistema constrói automaticamente as conexões do grafo.

---

# 🔎 Algoritmos de busca

## BFS — Breadth-First Search

A **Busca em Largura (BFS)** explora o grafo nível por nível.

Ela utiliza uma fila seguindo o modelo:

```text
FIFO — First In, First Out
```

Fluxo conceitual:

```text
Origem
  │
  ├── vizinho
  ├── vizinho
  └── vizinho
       │
       └── próximos vizinhos
```

Como a rede modelada é um grafo não ponderado, a BFS permite encontrar um caminho com o **menor número de arestas**.

No contexto atual do projeto, isso corresponde à minimização do número de deslocamentos entre estações.

> Isso não representa necessariamente o menor tempo real de viagem, pois fatores como duração entre estações, espera, lotação e tempo de baldeação não são atualmente utilizados como pesos.

---

## DFS — Depth-First Search

A **Busca em Profundidade (DFS)** explora profundamente um caminho antes de retornar para explorar outras alternativas.

Conceitualmente:

```text
A
│
B
│
C
│
D
```

A DFS pode encontrar um caminho válido entre origem e destino, mas não possui a mesma garantia da BFS de encontrar o menor caminho em quantidade de arestas em um grafo não ponderado.

A presença dos dois algoritmos permite também estudar e visualizar diferentes estratégias de exploração de grafos.

---

# 🧭 Caminho × ordem de visita

Os algoritmos retornam duas informações diferentes:

```text
caminho
ordem_visita
```

### Caminho

Representa a rota final encontrada.

Exemplo:

```text
Luz
→ São Bento
→ Sé
→ Pedro II
→ Brás
→ Bresser-Mooca
→ Belém
→ Tatuapé
```

### Ordem de visita

Representa as estações exploradas pelo algoritmo durante a busca.

Ela permite visualizar o **esforço do algoritmo** até encontrar o destino.

Por isso, a ordem de visita pode conter diversas estações que não fazem parte da rota final.

---

# 🔄 Sistema de baldeações

Após encontrar um caminho, o sistema determina quais linhas podem ser utilizadas em cada trecho.

Exemplo:

```text
Vila Madalena
    ↓
Linha Verde
    ↓
Paraíso
    ↓
Linha Azul
    ↓
Sé
    ↓
Linha Vermelha
    ↓
Tatuapé
```

O resultado pode conter:

```json
[
  {
    "estacao": "Paraíso",
    "de": "verde",
    "para": "azul"
  },
  {
    "estacao": "Sé",
    "de": "azul",
    "para": "vermelha"
  }
]
```

Nesse exemplo:

```text
Total de baldeações: 2
```

---

# 🧮 Minimização de baldeações

Alguns trechos podem pertencer a mais de uma linha.

Escolher arbitrariamente uma linha para cada trecho poderia criar baldeações artificiais.

Por isso, o MetrôBot considera o custo acumulado das escolhas de linha.

A lógica básica é:

```text
continuar na mesma linha → custo +0
trocar de linha          → custo +1
```

Conceitualmente:

```python
if linha_anterior == nova_linha:
    novo_custo = custo_anterior
else:
    novo_custo = custo_anterior + 1
```

A estratégia permite escolher uma sequência de linhas que evite trocas desnecessárias.

---

# 🚫 Restrições e regras

O sistema suporta fatos que alteram as rotas disponíveis.

Exemplos:

```text
estações bloqueadas
linhas indisponíveis
```

Uma

