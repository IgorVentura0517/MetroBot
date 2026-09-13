from data.linhas import LINHA_1_AZUL
from core.grafo import construir_grafo
from core.busca import bfs, dfs
from data.locais import buscar_estacao, resolver_local

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

    caminho_bfs, visita_bfs = bfs(
        grafo,
        origem, 
        destino
    )
    print("\nBFS")
    print("Origem:", origem)
    print("Destino:", destino)
    print("Rota:", caminho_bfs)

    caminho_dfs, visita_dfs = dfs(
        grafo,
        origem,
        destino
    )
    print("\nDFS")
    print("Origem:", origem)
    print("Destino:", destino)
    print("Rota:", caminho_dfs)

if __name__=="__main__":
    main()
