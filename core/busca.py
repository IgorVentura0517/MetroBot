from collections import deque

def bfs(grafo, origem, destino):
    fila = deque([origem])
    visitados = set()
    pai = {origem: None}

    while fila:
        atual = fila.popleft()

        if atual in visitados:
            continue

        visitados.add(atual)

        print(f"Visitando: {atual}")


        if atual == destino:
            return reconstruir_caminho(pai, destino)
            
        
        for vizinho in grafo[atual]:
            if vizinho not in visitados and vizinho not in pai:
                pai[vizinho] = atual
                fila.append(vizinho)
        
    return None


def reconstruir_caminho(pai, destino):
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = pai[atual]

    caminho.reverse()

    return caminho