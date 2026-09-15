def construir_grafo(estacoes):
    grafo = {}

    for estacao in estacoes:
        grafo[estacao] = []

    for i in range(len(estacoes)-1):
        estacao_atual = estacoes[i]
        proxima_estacao = estacoes[i +1]

        grafo[estacao_atual].append(proxima_estacao)
        grafo[proxima_estacao].append(estacao_atual)


    return grafo

def construir_grafo_multilinhas(linhas):
    grafo = {}
    linhas_do_trecho = {}

    for nome_linha, estacoes in linhas.items():

        for estacao in estacoes:
            if estacao not in grafo:
                grafo[estacao] = []

        for i in range(len(estacoes) - 1):
            atual = estacoes[i]
            proxima = estacoes[i + 1]

            if proxima not in grafo[atual]:
                grafo[atual].append(proxima)

            if atual not in grafo[proxima]:
                grafo[proxima].append(atual)

            linhas_do_trecho.setdefault(
                (atual, proxima),
                set()
            ).add(nome_linha)

            linhas_do_trecho.setdefault(
                (proxima, atual),
                set()
            ).add(nome_linha)

    return grafo, linhas_do_trecho