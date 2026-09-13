from data.linhas import LINHA_1_AZUL
from core.grafo import construir_grafo
from core.busca import bfs

def main():
    grafo = construir_grafo(LINHA_1_AZUL)

    caminho, ordem_visita = bfs(
        grafo,
        "Sé", 
        "São Joaquim"
    )

    if caminho is None:
        print("Não foi possível encontrar uma rota.")
    else:
    
        print("Ordem de visita:")
        print(ordem_visita)

        print("\nRota encontrada:")
        print(caminho)

if __name__=="__main__":
    main()
