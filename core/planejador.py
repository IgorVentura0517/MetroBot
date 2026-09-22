from data.locais import resolver_local
from core.busca import bfs, dfs
from core.baldeacoes import identificar_baldeacoes
from core.logica import criar_fatos, calcular_bloqueadas

def planejar_rota(grafo, linhas_do_trecho, origem_usuario, destino_usuario, algoritmo="bfs", bloqueadas=None, fatos=None):
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
    
    if fatos is None:
        fatos = criar_fatos(bloqueadas)
    bloqueadas = calcular_bloqueadas(fatos)
    
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
    
    baldeacoes = identificar_baldeacoes(
    caminho,
    linhas_do_trecho
    )
    
    return {
        "sucesso": True,
        "origem": origem,
        "destino": destino,
        "caminho": caminho,
        "ordem_visita": visita,
        "algoritmo": algoritmo,
        "baldeacoes": baldeacoes,
        "total_baldeacoes": len(baldeacoes)
    }
