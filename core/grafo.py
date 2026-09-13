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