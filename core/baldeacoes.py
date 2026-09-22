def identificar_baldeacoes(caminho, linhas_do_trecho):
    if caminho is None or len(caminho) < 2:
        return []

    primeiro_trecho = (
        caminho[0],
        caminho[1]
    )

    linhas_iniciais = linhas_do_trecho[primeiro_trecho]

    custos = {}
    historicos = {}

    for linha in linhas_iniciais:
        custos[linha] = 0
        historicos[linha] = [linha]

    for i in range(1, len(caminho) - 1):
        atual = caminho[i]
        proxima = caminho[i + 1]

        linhas_disponiveis = linhas_do_trecho[
            (atual, proxima)
        ]

        novos_custos = {}
        novos_historicos = {}

        for nova_linha in linhas_disponiveis:
            menor_custo = None
            melhor_historico = None

            for linha_anterior, custo_anterior in custos.items():

                if linha_anterior == nova_linha:
                    novo_custo = custo_anterior
                else:
                    novo_custo = custo_anterior + 1

                if (
                    menor_custo is None
                    or novo_custo < menor_custo
                ):
                    menor_custo = novo_custo
                    melhor_historico = historicos[linha_anterior] + [
                        nova_linha
                    ]

            novos_custos[nova_linha] = menor_custo
            novos_historicos[nova_linha] = melhor_historico

        custos = novos_custos
        historicos = novos_historicos

    linha_final = min(
        custos,
        key=custos.get
    )

    sequencia_linhas = historicos[linha_final]

    baldeacoes = []

    for i in range(1, len(sequencia_linhas)):
        linha_anterior = sequencia_linhas[i - 1]
        linha_atual = sequencia_linhas[i]

        if linha_anterior != linha_atual:
            baldeacoes.append({
                "estacao": caminho[i],
                "de": linha_anterior,
                "para": linha_atual
            })

    return baldeacoes