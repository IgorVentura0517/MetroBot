from data.linhas import LINHA_1_AZUL
from core.grafo import construir_grafo
from core.busca import bfs, dfs
from data.locais import buscar_estacao, resolver_local
from core.planejador import planejar_rota

def main():
    grafo = construir_grafo(LINHA_1_AZUL)

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
        "Pinacoteca",
        "Catedral da Sé",
        algoritmo="bfs",
        bloqueadas={"Jabaquara"}
    )


    if resultado["sucesso"]:
        print("Origem:", resultado["origem"])
        print("Destino:", resultado["destino"])
        print("Rota:", resultado["caminho"])
        print("Ordem de visita:", resultado["ordem_visita"])
    else:
        print("Erro:", resultado["erro"])

if __name__=="__main__":
    main()
