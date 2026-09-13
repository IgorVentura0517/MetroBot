from data.linhas import LINHA_1_AZUL
from core.grafo import construir_grafo
from core.busca import bfs

def main():
    grafo = construir_grafo(LINHA_1_AZUL)

    bfs(
        grafo,
        "Sé",
        "São Joaquim"
    )

if __name__=="__main__":
    main()
