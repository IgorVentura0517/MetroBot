from data.linhas import LINHA_1_AZUL
from core.grafo import construir_grafo
from core.busca import bfs, dfs
from data.locais import buscar_estacao

def main():
    grafo = construir_grafo(LINHA_1_AZUL)

    local = "Catedral da Sé"
    destino = buscar_estacao(local)

    if destino is None:
        print("Local não encontrado.")
        return

    caminho_bfs, visita_bfs = bfs(
        grafo,
        "Tucuruvi", 
        destino
    )

    print(buscar_estacao("Catedral da Sé"))
    print(buscar_estacao("catedral da sé"))
    print(buscar_estacao("CATEDRAL DA SÉ"))
    print(buscar_estacao("   Catedral da Sé   "))
    print(buscar_estacao("catedral da se"))
    print(buscar_estacao("MUSEU DA LINGUA PORTUGUESA"))
    print(buscar_estacao("MASP"))


    caminho_dfs, visita_dfs = dfs(
        grafo,
        "Tucuruvi",
        destino
    )





if __name__=="__main__":
    main()
