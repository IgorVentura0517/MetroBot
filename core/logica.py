from data.linhas import LINHAS

def criar_fatos(bloqueadas=None, linhas_indisponiveis=None):
    if bloqueadas is None:
        bloqueadas = set()

    if linhas_indisponiveis is None:
        linhas_indisponiveis = set()

    return {
        "bloqueadas": set(bloqueadas),
        "linhas_indisponiveis": set(linhas_indisponiveis)
    }


def estacao_bloqueada(fatos, estacao):
    return estacao in fatos["bloqueadas"]

def pode_usar_estacao(fatos, estacao):
    return not estacao_bloqueada(fatos, estacao)

def obter_bloqueadas(fatos):
    return fatos["bloqueadas"]

def linha_disponivel(fatos, linha):
    return linha not in fatos["linhas_indisponiveis"]

def calcular_bloqueadas(fatos):
    return set(fatos["bloqueadas"])

def trecho_disponivel(fatos, linhas_do_trecho, origem, destino):
    linhas = linhas_do_trecho.get((origem, destino), set())

    for linha in linhas:
        if linha_disponivel(fatos, linha):
            return True

    return False