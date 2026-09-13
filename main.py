from data.linhas import LINHA_1_AZUL
from core.grafo import construir_grafo
from core.busca import bfs

def main():
    grafo = construir_grafo(LINHA_1_AZUL)

    caminho = bfs(
        grafo,
        "Sé", 
        "São Joaquim"
    )

    print("\n Rota encontrada: ")
    print(caminho)

if __name__=="__main__":
    main()
