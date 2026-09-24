"""
Camada de apresentação da interface web.

Aqui ficam apenas os dados que a interface precisa para se montar
(cores, nomes de exibição das linhas, estações e locais). Nenhuma decisão
de rota acontece neste módulo: quem decide é core/ (busca + regras) e
quem explica é llm/. Os arquivos da interface estão em interface/static/.
"""
import os

from data.linhas import LINHAS
from data.locais import LOCAIS


# As chaves de LINHAS são curtas ("azul"); na tela mostramos o nome completo.
NOMES_LINHAS = {
    "azul": "Linha 1-Azul",
    "verde": "Linha 2-Verde",
    "vermelha": "Linha 3-Vermelha",
}

CORES = {
    "azul": "#1e88e5",
    "verde": "#2e7d32",
    "vermelha": "#d32f2f",
}

ALGORITMOS = [
    {"codigo": "bfs", "rotulo": "BFS - busca em largura (menos paradas)"},
    {"codigo": "dfs", "rotulo": "DFS - busca em profundidade"},
]


def listar_estacoes():
    """Todas as estações, sem repetir as de integração (Sé, Paraíso, Ana Rosa)."""
    estacoes = []

    for lista in LINHAS.values():
        for estacao in lista:
            if estacao not in estacoes:
                estacoes.append(estacao)

    return estacoes


def integracoes():
    """Estações que aparecem em mais de uma linha."""
    contagem = {}

    for lista in LINHAS.values():
        for estacao in lista:
            contagem[estacao] = contagem.get(estacao, 0) + 1

    return sorted(
        estacao
        for estacao, vezes in contagem.items()
        if vezes > 1
    )


def linhas_da_estacao(estacao):
    """Chaves das linhas que atendem a estação."""
    return [
        chave
        for chave, lista in LINHAS.items()
        if estacao in lista
    ]


def llm_configurado():
    """A interpretação e a narração por LLM só funcionam com a chave do Groq."""
    return bool(os.getenv("GROQ_API_KEY"))


def montar_dados():
    """Payload usado pela interface para montar os formulários e o mapa."""
    return {
        "linhas": LINHAS,
        "nomes_linhas": NOMES_LINHAS,
        "cores": CORES,
        "estacoes": listar_estacoes(),
        "locais": LOCAIS,
        "integracoes": integracoes(),
        "algoritmos": ALGORITMOS,
        "llm_configurado": llm_configurado(),
    }
