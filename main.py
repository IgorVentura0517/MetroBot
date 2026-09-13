from data.linhas import LINHA_1_AZUL
from core.grafo import construir_grafo
from core.busca import bfs, dfs

def main():
    grafo = construir_grafo(LINHA_1_AZUL)

    caminho_bfs, visita_bfs = bfs(
        grafo,
        "Sé", 
        "São Joaquim",
        bloqueadas={"Japão-Liberdade"}
    )

    print(caminho_bfs)
    print(visita_bfs)

    caminho_dfs, visita_dfs = dfs(
        grafo,
        "Sé",
        "São Joaquim",
        bloqueadas={"Jpão-Liberdade"}
    )

    print(caminho_dfs)
    print(visita_dfs)


if __name__=="__main__":
    main()
