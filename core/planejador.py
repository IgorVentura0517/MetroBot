from data.locais import resolver_local
from core.busca import bfs, dfs

def planejar_rota(grafo, origem_usuario, destino_usuario, algoritmo="bfs", bloqueadas=None):
    origem = resolver_local(origem_usuario)
    destino = resolver_local(destino_usuario)

    if bloqueadas is None:
        bloqueadas = set()

    if origem is None:
        return{
            "sucesso": False,
            "erro": "Origem não encontrada."
        }
    
    if destino is None:
        return{
            "sucesso": False,
            "erro": "Destino não encontrado."
        }
    
    if algoritmo == "bfs":
        caminho, visita= bfs(
        grafo,
        origem, 
        destino, 
        bloqueadas
    )
        
    elif algoritmo =="dfs":
        caminho, visita = dfs(
        grafo,
        origem,
        destino,
        bloqueadas
    )
        
    else:
        return{
            "sucesso": False,
            "erro": "Algoritmo inválido"
        }
    
    if caminho is None:
        return{
            "sucesso": False,
            "erro": "Não foi possível encontrar uma rota."
        }
    
    return{
        "sucesso": True,
        "origem": origem,
        "destino": destino,
        "caminho": caminho,
        "ordem_visita":visita,
        "algoritmo": algoritmo
    }
