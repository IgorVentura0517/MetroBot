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

- 🚇 Representação de múltiplas linhas do metrô
- 🗺️ Modelagem da rede utilizando grafos
- 🔎 Busca de rotas com **BFS**
- 🌲 Busca de rotas com **DFS**
- 🔄 Identificação automática de baldeações
- 🧠 Minimização de trocas desnecessárias entre linhas
- 🚫 Suporte a estações bloqueadas
- ⚠️ Suporte a linhas indisponíveis
- 📍 Associação de pontos de interesse a estações
- 🔤 Normalização das entradas do usuário
- 🤖 Interpretação de linguagem natural com LLM
- 💬 Geração de respostas amigáveis com LLM
- 🌐 API REST utilizando FastAPI
- 🎨 Interface web em HTML, CSS e JavaScript
- 📑 Documentação automática via Swagger/OpenAPI
- 🧪 Testes automatizados com pytest
- 🔐 Gerenciamento da chave da API através de variável de ambiente

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

Uma estação bloqueada representa uma restrição sobre um **vértice** do grafo.

```text
A ─── B ─── C

     B
     X
```

Já uma linha indisponível representa uma restrição sobre as **arestas associadas àquela linha**.

Essa diferença é importante porque uma estação de integração pode pertencer a várias linhas.

Desativar uma linha não significa necessariamente bloquear a estação inteira.

---

# 📍 Pontos de interesse

O usuário não precisa obrigatoriamente conhecer o nome da estação.

O sistema possui uma camada para relacionar locais conhecidos a estações.

Exemplos:

```text
Pinacoteca
    ↓
Luz

Museu da Língua Portuguesa
    ↓
Luz

Catedral da Sé
    ↓
Sé

Shopping Santa Cruz
    ↓
Santa Cruz
```

Essa responsabilidade permanece no código da aplicação, e não no LLM.

---

# 🔤 Normalização de entradas

As entradas passam por normalização para reduzir problemas causados por diferenças de escrita.

Por exemplo:

```text
Sé
SÉ
sé
se
```

podem ser comparadas de maneira mais consistente.

São utilizadas operações de normalização envolvendo:

- remoção de espaços extras;
- conversão para letras minúsculas;
- normalização Unicode;
- tratamento de acentuação.

---

# 🤖 Integração com LLM

O projeto utiliza um LLM através da API da **Groq**.

A camada de IA é dividida em três responsabilidades:

```text
llm/
├── cliente.py
├── interprete.py
└── narrador.py
```

## `cliente.py`

Encapsula a comunicação com o provedor do modelo.

Outros componentes utilizam uma abstração semelhante a:

```python
chamar_llm(prompt)
```

e não precisam conhecer detalhes de autenticação, SDK ou comunicação com o provedor.

---

## `interprete.py`

Transforma linguagem natural em dados estruturados.

Entrada:

```text
Estou na Vila Madalena e quero chegar em Tatuapé.
```

Saída:

```json
{
  "origem": "Vila Madalena",
  "destino": "Tatuapé",
  "algoritmo": "bfs"
}
```

O interpretador **não calcula a rota**.

---

## `narrador.py`

Recebe uma rota já calculada e transforma o resultado técnico em uma resposta amigável.

O narrador não deve recalcular ou alterar:

- estações;
- caminho;
- baldeações;
- origem;
- destino.

Sua responsabilidade é apresentar o resultado calculado pelo core.

---

# 🌐 API REST

O backend utiliza **FastAPI**.

A API funciona como ponte entre:

```text
Frontend
   ↕
HTTP / JSON
   ↕
Backend Python
```

Entre os principais endpoints estão:

```text
GET  /
POST /rota
POST /chat
```

---

# 🛣️ Endpoint `/rota`

Permite solicitar diretamente uma rota estruturada.

### Requisição

```http
POST /rota
```

Exemplo:

```json
{
  "origem": "Vila Madalena",
  "destino": "Tatuapé",
  "algoritmo": "bfs"
}
```

### Resposta

Exemplo simplificado:

```json
{
  "sucesso": true,
  "origem": "Vila Madalena",
  "destino": "Tatuapé",
  "caminho": [
    "Vila Madalena",
    "Sumaré",
    "Clínicas",
    "Consolação",
    "Trianon-Masp",
    "Brigadeiro",
    "Paraíso",
    "Vergueiro",
    "São Joaquim",
    "Japão-Liberdade",
    "Sé",
    "Pedro II",
    "Brás",
    "Bresser-Mooca",
    "Belém",
    "Tatuapé"
  ],
  "algoritmo": "bfs",
  "baldeacoes": [
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
  ],
  "total_baldeacoes": 2
}
```

---

# 💬 Endpoint `/chat`

O endpoint `/chat` aceita uma solicitação em linguagem natural.

### Requisição

```http
POST /chat
```

```json
{
  "mensagem": "Quero sair da Pinacoteca e ir para Tatuapé"
}
```

Fluxo interno:

```text
mensagem
   ↓
interprete.py
   ↓
LLM
   ↓
origem + destino + algoritmo
   ↓
planejador
   ↓
grafo + regras + BFS/DFS
   ↓
baldeações
   ↓
narrador.py
   ↓
LLM
   ↓
resposta
```

### Resposta

Exemplo simplificado:

```json
{
  "sucesso": true,
  "mensagem_usuario": "Quero sair da Pinacoteca e ir para Tatuapé",
  "interpretacao": {
    "sucesso": true,
    "origem": "Pinacoteca",
    "destino": "Tatuapé",
    "algoritmo": "bfs"
  },
  "rota": {
    "sucesso": true,
    "origem": "Luz",
    "destino": "Tatuapé",
    "caminho": [
      "Luz",
      "São Bento",
      "Sé",
      "Pedro II",
      "Brás",
      "Bresser-Mooca",
      "Belém",
      "Tatuapé"
    ],
    "baldeacoes": [
      {
        "estacao": "Sé",
        "de": "azul",
        "para": "vermelha"
      }
    ],
    "total_baldeacoes": 1
  },
  "resposta": "Resposta em linguagem natural gerada pelo MetrôBot."
}
```

---

# 🎨 Frontend

A interface foi construída utilizando:

- **HTML5**
- **CSS3**
- **JavaScript**

Ela permite:

- conversar com o MetrôBot;
- selecionar origem;
- selecionar destino;
- escolher BFS ou DFS;
- visualizar quantidade de paradas;
- visualizar quantidade de baldeações;
- visualizar número de estações exploradas;
- visualizar onde trocar de linha;
- visualizar o caminho calculado;
- visualizar a ordem de visita da busca.

O frontend consome os serviços disponibilizados pelo backend FastAPI.

---

# 🧩 Estrutura do projeto

```text
MetroBot/
│
├── api.py
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env
│
├── core/
│   ├── __init__.py
│   ├── grafo.py
│   ├── busca.py
│   ├── logica.py
│   ├── baldeacoes.py
│   └── planejador.py
│
├── data/
│   ├── __init__.py
│   ├── linhas.py
│   └── locais.py
│
├── llm/
│   ├── __init__.py
│   ├── cliente.py
│   ├── interprete.py
│   └── narrador.py
│
├── interface/
│   ├── __init__.py
│   ├── app.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── app.js
│
└── tests/
    └── test_metrobot.py
```

---

# 📂 Responsabilidade dos módulos

| Módulo | Responsabilidade |
|---|---|
| `data/linhas.py` | Define linhas e estações |
| `data/locais.py` | Resolve locais e normaliza entradas |
| `core/grafo.py` | Constrói a representação da rede |
| `core/busca.py` | Implementa BFS e DFS |
| `core/logica.py` | Gerencia fatos e restrições |
| `core/baldeacoes.py` | Identifica e otimiza trocas de linha |
| `core/planejador.py` | Orquestra o cálculo das rotas |
| `llm/cliente.py` | Encapsula a comunicação com o LLM |
| `llm/interprete.py` | Converte linguagem natural em dados |
| `llm/narrador.py` | Converte o resultado técnico em linguagem natural |
| `api.py` | Expõe os serviços através do FastAPI |
| `interface/` | Implementa a interface web |
| `tests/` | Contém os testes automatizados |

---

# 🧱 Conceitos de Engenharia de Software aplicados

## Separação de responsabilidades

Cada módulo possui uma responsabilidade específica.

O algoritmo de busca não precisa saber como o frontend funciona, e o frontend não precisa conhecer a implementação interna da BFS.

## Encapsulamento

Detalhes de implementação são escondidos atrás de interfaces simples.

Por exemplo:

```python
chamar_llm(prompt)
```

O restante do sistema não precisa conhecer os detalhes internos da API da Groq.

## Baixo acoplamento

Os módulos dependem o mínimo possível dos detalhes internos uns dos outros.

Por exemplo, `busca.py` não precisa conhecer:

```text
FastAPI
Groq
HTML
CSS
JavaScript
```

## Alta coesão

Funcionalidades relacionadas permanecem agrupadas.

```text
busca.py       → algoritmos de busca
baldeacoes.py  → trocas de linha
locais.py      → resolução de locais
cliente.py     → comunicação com LLM
```

## Testabilidade

O core pode ser testado independentemente da interface web e, em diversos cenários, independentemente do LLM.

Isso permite detectar regressões rapidamente.

---

# 🧪 Testes automatizados

Os testes utilizam **pytest**.

Entre os cenários testados estão:

- rota entre Linha Verde e Linha Azul;
- rota sem baldeação;
- rota envolvendo três linhas;
- estação bloqueada;
- origem inexistente;
- destino inexistente;
- algoritmo inválido;
- menor caminho com BFS;
- respeito a bloqueios;
- funcionamento da DFS;
- regras para estações bloqueadas;
- planejamento utilizando fatos;
- linha indisponível;
- planejamento com linha indisponível;
- funcionamento de outra linha quando uma linha está indisponível.

Para executar:

```bash
pytest -v
```

---

# 🛠️ Tecnologias utilizadas

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

## Estruturas de Dados e Algoritmos

- Grafos
- Listas de adjacência
- Filas
- Dicionários
- Conjuntos
- BFS — Breadth-First Search
- DFS — Depth-First Search
- Reconstrução de caminho
- Estratégia de custo para minimização de baldeações

## Inteligência Artificial

- Large Language Models
- Groq API
- Engenharia de prompts
- Interpretação estruturada
- Geração de linguagem natural

## Frontend

- HTML5
- CSS3
- JavaScript

## Qualidade e desenvolvimento

- pytest
- Git
- GitHub
- Variáveis de ambiente
- Swagger
- OpenAPI

---

# ⚙️ Instalação

## 1. Clone o repositório

```bash
git clone https://github.com/IgorVentura0517/MetroBot.git
```

Entre no diretório:

```bash
cd MetroBot
```

---

## 2. Crie um ambiente virtual

### Windows

```bash
python -m venv .venv
```

Ative:

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

# 🔑 Configuração do LLM

Para utilizar os recursos de linguagem natural, é necessária uma chave da API da Groq.

Crie um arquivo `.env` na raiz:

```text
.env
```

Adicione:

```env
GROQ_API_KEY=SUA_CHAVE_AQUI
```

> ⚠️ **Nunca publique sua chave de API no GitHub.**

O `.env` deve permanecer incluído no `.gitignore`.

Sem uma chave válida, os recursos que dependem do LLM não funcionarão. As funcionalidades determinísticas podem continuar disponíveis de acordo com a configuração da aplicação.

---

# ▶️ Executando o projeto

Com o ambiente virtual ativado e as dependências instaladas:

```bash
uvicorn api:app --reload
```

O servidor será iniciado localmente.

Abra no navegador:

```text
http://127.0.0.1:8000
```

---

# 📚 Swagger / documentação da API

A documentação interativa pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

O Swagger permite testar os endpoints diretamente pelo navegador.

Por exemplo:

```text
POST /rota
POST /chat
```

---

# 🧪 Executando os testes

Na raiz do projeto:

```bash
pytest -v
```

Uma execução bem-sucedida deverá apresentar os testes como:

```text
PASSED
```

Recomenda-se executar a suíte antes de commits e merges importantes.

---

# 🔄 Fluxo completo de uma solicitação

Considere:

```text
Quero sair da Pinacoteca e ir para Tatuapé.
```

### 1. Frontend

Envia:

```json
{
  "mensagem": "Quero sair da Pinacoteca e ir para Tatuapé"
}
```

para:

```text
POST /chat
```

### 2. FastAPI

Recebe e valida a requisição.

### 3. Intérprete LLM

Extrai:

```text
origem: Pinacoteca
destino: Tatuapé
algoritmo: BFS
```

### 4. Resolução de local

O sistema identifica:

```text
Pinacoteca → Luz
```

### 5. Planejador

Coordena as regras e o algoritmo.

### 6. Grafo

A rede é consultada para encontrar conexões possíveis.

### 7. BFS

Calcula:

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

### 8. Baldeações

Identifica:

```text
Sé
Linha Azul → Linha Vermelha
```

### 9. Narrador

Recebe o resultado calculado e produz uma explicação natural.

### 10. API

Retorna o resultado em JSON.

### 11. Frontend

Apresenta a rota ao usuário.

---

# 🔐 Segurança

Algumas decisões adotadas:

- chave da Groq armazenada em variável de ambiente;
- `.env` ignorado pelo Git;
- nenhuma chave de API armazenada no JavaScript;
- frontend não acessa diretamente o provedor do LLM;
- chamadas ao LLM passam pelo backend.

Fluxo:

```text
Browser
   ↓
FastAPI
   ↓
cliente.py
   ↓
.env
   ↓
Groq
```

A credencial permanece no lado servidor.

---

# 🚀 Possíveis evoluções

O projeto pode futuramente incorporar:

- [ ] Demais linhas do Metrô de São Paulo
- [ ] Integração com linhas da CPTM
- [ ] Pesos nas arestas
- [ ] Tempo estimado de viagem
- [ ] Distância entre estações
- [ ] Tempo de baldeação
- [ ] Algoritmo de Dijkstra
- [ ] Algoritmo A*
- [ ] Comparação entre diferentes critérios de rota
- [ ] Mapa gráfico interativo
- [ ] Informações operacionais em tempo real
- [ ] Persistência em banco de dados
- [ ] Histórico de consultas
- [ ] Autenticação
- [ ] Deploy em nuvem
- [ ] Docker
- [ ] CI/CD
- [ ] Testes de integração
- [ ] Testes end-to-end

Uma evolução natural seria transformar o grafo não ponderado atual em um **grafo ponderado**.

Assim, em vez de otimizar principalmente o número de trechos, seria possível considerar:

```text
tempo
distância
baldeações
```

ou uma função de custo combinando esses fatores.

---

# 🎯 Objetivos técnicos

O MetrôBot foi desenvolvido não apenas como uma aplicação de rotas, mas também como projeto para aplicar de forma integrada conceitos de:

- Engenharia de Software
- Estruturas de Dados
- Algoritmos
- Grafos
- Inteligência Artificial
- APIs REST
- Desenvolvimento Web
- Testes automatizados
- Arquitetura modular
- Desenvolvimento colaborativo
- Controle de versão

---

# 💡 Resumo arquitetural

A essência do MetrôBot pode ser resumida em:

```text
┌───────────────────────────────┐
│              LLM              │
│    entende linguagem humana   │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│       CORE DETERMINÍSTICO     │
│                               │
│ Grafo → Regras → BFS/DFS      │
│       → Baldeações            │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│              LLM              │
│       explica o resultado     │
└───────────────────────────────┘
```

## **O LLM conversa. O algoritmo decide.**

---

# 👥 Desenvolvimento

O projeto é desenvolvido de forma colaborativa, com separação entre o desenvolvimento do **backend/core algorítmico** e da **interface frontend**.

Git e GitHub são utilizados para:

- controle de versão;
- branches;
- commits incrementais;
- colaboração;
- integração das funcionalidades.

Fluxo recomendado:

```text
feature branch
      ↓
    commit
      ↓
     push
      ↓
Pull Request
      ↓
    review
      ↓
    merge
      ↓
     main
```

---

# 📄 Licença

A licença do projeto ainda deve ser definida.

Para projetos de portfólio e código aberto, uma opção possível é a **MIT License**.

---

# 🚇 MetrôBot SP

### Grafos + Algoritmos + API + Web + Inteligência Artificial

Uma aplicação em que a Inteligência Artificial melhora a interação com o usuário sem substituir a lógica determinística responsável pela solução do problema.

> **O LLM conversa. O algoritmo decide.**
