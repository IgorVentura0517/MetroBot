from collections import deque

def reconstruir_caminho(pai, destino):
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = pai[atual]

    caminho.reverse()

    return caminho

def bfs(grafo, origem, destino, bloqueadas=None, trecho_permitido=None):
    if bloqueadas is None:
        bloqueadas = set()

    if origem not in grafo or destino not in grafo:
        return None, []
    
    if origem in bloqueadas or destino in bloqueadas:
        return None, []
    
    fila = deque([origem])
    visitados = set()
    pai = {origem: None}
    ordem_visita=[]

    while fila:
        atual = fila.popleft()

        if atual in visitados:
            continue

        visitados.add(atual)
        ordem_visita.append(atual)

        if atual == destino:
            caminho = reconstruir_caminho(pai, destino)
            return caminho, ordem_visita
            
        
        for vizinho in grafo[atual]:
            if trecho_permitido is not None:
                if not trecho_permitido(atual, vizinho):
                    continue

            if (vizinho not in visitados 
                and vizinho not in pai 
                and vizinho not in bloqueadas
            ):
                pai[vizinho] = atual
                fila.append(vizinho)
        
    return None, ordem_visita

def dfs(grafo, origem, destino, bloqueadas=None, trecho_permitido=None):
    if bloqueadas is None:
        bloqueadas = set()
        
    if origem not in grafo or destino not in grafo:
        return None, []
    
    if origem in bloqueadas or destino in bloqueadas:
        return None, []
    
    pilha = [origem]
    visitados = set()
    pai = {origem: None}
    ordem_visita=[]

    while pilha:
        atual = pilha.pop()

        if atual in visitados:
            continue

        visitados.add(atual)
        ordem_visita.append(atual)

        if atual == destino:
            caminho = reconstruir_caminho(pai, destino)
            return caminho, ordem_visita
        
        for vizinho in grafo[atual]:
            if trecho_permitido is not None:
                if not trecho_permitido(atual, vizinho):
                    continue

            if (vizinho not in visitados 
                and vizinho not in pai
                and vizinho not in bloqueadas
            ):
                pai[vizinho] = atual
                pilha.append(vizinho)

    return None, ordem_visita

