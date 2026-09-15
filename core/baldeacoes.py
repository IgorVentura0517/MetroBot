def identificar_baldeacoes(caminho, linhas_do_trecho):
    if caminho is None or len(caminho) < 2:
        return []

    baldeacoes = []
    linha_atual = None

    for i in range(len(caminho) - 1):
        atual = caminho[i]
        proxima = caminho[i + 1]

        linhas = linhas_do_trecho[(atual, proxima)]

        if linha_atual is None:
            linha_atual = sorted(linhas)[0]

        elif linha_atual not in linhas:
            nova_linha = sorted(linhas)[0]

            baldeacoes.append({
                "estacao": atual,
                "de": linha_atual,
                "para": nova_linha
            })

            linha_atual = nova_linha

    return baldeacoes