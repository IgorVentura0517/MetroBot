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
            print("Destino encontrado")
            break
        
        for vizinho in grafo[atual]:
            if vizinho not in visitados and vizinho not in pai:
                pai[vizinho] = atual
                fila.append(vizinho)


    print(pai)