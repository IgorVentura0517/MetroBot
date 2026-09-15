from data.linhas import LINHAS
from core.grafo import construir_grafo_multilinhas
from core.busca import bfs, dfs
from data.locais import buscar_estacao, resolver_local
from core.planejador import planejar_rota
from core.baldeacoes import identificar_baldeacoes

def main():
    grafo, linhas_do_trecho = construir_grafo_multilinhas(LINHAS)

    origem_usuario = "Pinacoteca"
    destino_usuario = "Catedral da Sé"

    origem = resolver_local(origem_usuario)
    destino = resolver_local(destino_usuario)

    if origem is None:
        print("Origem não encontrada.")
        return

    if destino is None:
        print("Destino não encontrado.")
        return

    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        "Vila Madalena",
        "São Joaquim",
        algoritmo="bfs"
    )
    
    baldeacoes = identificar_baldeacoes(
    resultado["caminho"],
    linhas_do_trecho
)

    print("Rota:", resultado["caminho"])
    print("Baldeações:", baldeacoes)


    if resultado["sucesso"]:
        print("Origem:", resultado["origem"])
        print("Destino:", resultado["destino"])
        print("Rota:", resultado["caminho"])
        print("Baldeações:", resultado["baldeacoes"])
        print("Total de baldeações:", resultado["total_baldeacoes"])
        print("Ordem de visita:", resultado["ordem_visita"])
    else:
        print("Erro:", resultado["erro"])


if __name__=="__main__":
    main()
