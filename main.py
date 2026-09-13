from data.linhas import LINHA_1_AZUL
from core.grafo import construir_grafo
from core.busca import bfs, dfs
from data.locais import buscar_estacao

def main():
    grafo = construir_grafo(LINHA_1_AZUL)

    local = "MASP"
    destino = buscar_estacao(local)

    if destino is None:
        print("Local não encontrado.")
        return

    caminho_bfs, visita_bfs = bfs(
        grafo,
        "Tucuruvi", 
        destino
    )

    print("Destino solicitado:", local)
    print("Estação de destino:", destino)
    print("Rota:", caminho_bfs)


    caminho_dfs, visita_dfs = dfs(
        grafo,
        "Tucuruvi",
        destino
    )

    print("Destino solicitado:", local)
    print("Estação de destino:", destino)
    print("Rota:", caminho_dfs)





if __name__=="__main__":
    main()
