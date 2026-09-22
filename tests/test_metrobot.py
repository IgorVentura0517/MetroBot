from data.linhas import LINHAS
from core.grafo import construir_grafo_multilinhas
from core.planejador import planejar_rota
from core.busca import bfs, dfs
from core.logica import criar_fatos, estacao_bloqueada, pode_usar_estacao, calcular_bloqueadas, trecho_disponivel


grafo, linhas_do_trecho = construir_grafo_multilinhas(LINHAS)


def test_rota_verde_para_azul():
    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        "Vila Madalena",
        "São Joaquim",
        algoritmo="bfs"
    )

    assert resultado["sucesso"] is True
    assert resultado["total_baldeacoes"] == 1
    assert resultado["baldeacoes"][0]["estacao"] == "Paraíso"


def test_rota_sem_baldeacao():
    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        "Brigadeiro",
        "Chácara Klabin",
        algoritmo="bfs"
    )

    assert resultado["sucesso"] is True
    assert resultado["total_baldeacoes"] == 0


def test_rota_tres_linhas():
    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        "Vila Madalena",
        "Tatuapé",
        algoritmo="bfs"
    )

    assert resultado["sucesso"] is True
    assert resultado["total_baldeacoes"] == 2

    assert resultado["baldeacoes"][0]["estacao"] == "Paraíso"
    assert resultado["baldeacoes"][1]["estacao"] == "Sé"

def test_estacao_bloqueada():
    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        "Vila Madalena",
        "São Joaquim",
        algoritmo="bfs",
        bloqueadas={"Paraíso"}
    )

    assert resultado["sucesso"] is False


def test_origem_inexistente():
    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        "Estação Inventada",
        "Sé",
        algoritmo="bfs"
    )

    assert resultado["sucesso"] is False
    assert resultado["erro"] == "Origem não encontrada."


def test_destino_inexistente():
    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        "Sé",
        "Estação Inventada",
        algoritmo="bfs"
    )

    assert resultado["sucesso"] is False
    assert resultado["erro"] == "Destino não encontrado."


def test_algoritmo_invalido():
    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        "Sé",
        "Tatuapé",
        algoritmo="dijkstra"
    )

    assert resultado["sucesso"] is False
    assert resultado["erro"] == "Algoritmo inválido"

def test_bfs_encontra_menor_caminho():
    caminho, ordem_visita = bfs(
        grafo,
        "Sé",
        "São Joaquim"
    )

    assert caminho == [
        "Sé",
        "Japão-Liberdade",
        "São Joaquim"
    ]

    assert ordem_visita is not None


def test_bfs_respeita_bloqueio():
    caminho, ordem_visita = bfs(
        grafo,
        "Sé",
        "São Joaquim",
        bloqueadas={"Japão-Liberdade"}
    )

    assert caminho is None
    assert "Japão-Liberdade" not in ordem_visita


def test_dfs_encontra_caminho():
    caminho, ordem_visita = dfs(
        grafo,
        "Sé",
        "São Joaquim"
    )

    assert caminho is not None
    assert caminho[0] == "Sé"
    assert caminho[-1] == "São Joaquim"

def test_regras_estacao_bloqueada():
    fatos = criar_fatos({"Paraíso"})

    assert estacao_bloqueada(fatos, "Paraíso") is True
    assert pode_usar_estacao(fatos, "Paraíso") is False
    assert pode_usar_estacao(fatos, "Sé") is True

def test_planejador_com_fatos():
    fatos = criar_fatos({"Paraíso"})

    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        "Vila Madalena",
        "São Joaquim",
        algoritmo="bfs",
        fatos=fatos
    )

    assert resultado["sucesso"] is False


def test_linha_indisponivel():
    fatos = criar_fatos(
        linhas_indisponiveis={"verde"}
    )

    assert trecho_disponivel(
        fatos,
        linhas_do_trecho,
        "Brigadeiro",
        "Paraíso"
    ) is False

    assert trecho_disponivel(
        fatos,
        linhas_do_trecho,
        "Paraíso",
        "Ana Rosa"
    ) is True

    assert trecho_disponivel(
        fatos,
        linhas_do_trecho,
        "Paraíso",
        "Vergueiro"
    ) is True

def test_planejador_com_linha_indisponivel():
    fatos = criar_fatos(
        linhas_indisponiveis={"verde"}
    )

    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        "Brigadeiro",
        "São Joaquim",
        algoritmo="bfs",
        fatos=fatos
    )

    assert resultado["sucesso"] is False

def test_azul_funciona_com_verde_indisponivel():
    fatos = criar_fatos(
        linhas_indisponiveis={"verde"}
    )

    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        "Vergueiro",
        "Vila Mariana",
        algoritmo="bfs",
        fatos=fatos
    )

    assert resultado["sucesso"] is True
    assert "Paraíso" in resultado["caminho"]
    assert "Ana Rosa" in resultado["caminho"]