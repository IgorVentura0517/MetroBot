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
    bloqueadas = set(fatos["bloqueadas"])

    for linha in fatos["linhas_indisponiveis"]:
        if linha in LINHAS:
            bloqueadas.update(LINHAS[linha])

    return bloqueadas