from fastapi import FastAPI
from pydantic import BaseModel

from data.linhas import LINHAS
from core.grafo import construir_grafo_multilinhas
from core.planejador import planejar_rota


app = FastAPI(
    title="MetrôBot API",
    version="1.0.0"
)


grafo, linhas_do_trecho = construir_grafo_multilinhas(LINHAS)


class RotaRequest(BaseModel):
    origem: str
    destino: str
    algoritmo: str = "bfs"


@app.get("/")
def inicio():
    return {
        "nome": "MetrôBot API",
        "status": "online"
    }


@app.post("/rota")
def calcular_rota(dados: RotaRequest):
    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        dados.origem,
        dados.destino,
        algoritmo=dados.algoritmo
    )

    return resultado