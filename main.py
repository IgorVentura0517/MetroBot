from data.linhas import LINHA_1_AZUL
from core.grafo import construir_grafo
from core.busca import bfs, dfs

def main():
    grafo = construir_grafo(LINHA_1_AZUL)

    caminho_bfs, visita_bfs = bfs(
        grafo,
        "Sé", 
        "São Joaquim"
    )

    caminho_dfs, visita_dfs = dfs(
        grafo,
        "Sé",
        "São Joaquim"
    )

    print("BFS")
    print("Ordem de visita:", visita_bfs)
    print("Caminho:", caminho_bfs)

    print("\nDFS")
    print("Ordem de visita:", visita_dfs)
    print("Caminho:", caminho_dfs)

if __name__=="__main__":
    main()
