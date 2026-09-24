from fastapi import FastAPI
from pydantic import BaseModel

from data.linhas import LINHAS
from core.grafo import construir_grafo_multilinhas
from core.planejador import planejar_rota
from llm.interprete import interpretar_mensagem
from llm.narrador import narrar_rota


app = FastAPI(
    title="MetrôBot API",
    version="1.0.0"
)


grafo, linhas_do_trecho = construir_grafo_multilinhas(LINHAS)


class RotaRequest(BaseModel):
    origem: str
    destino: str
    algoritmo: str = "bfs"

class ChatRequest(BaseModel):
    mensagem: str


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

@app.post("/chat")
def conversar(dados: ChatRequest):

    interpretacao = interpretar_mensagem(dados.mensagem)

    if not interpretacao["sucesso"]:
        return {
            "sucesso": False,
            "erro": interpretacao["erro"]
        }

    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        interpretacao["origem"],
        interpretacao["destino"],
        algoritmo=interpretacao["algoritmo"]
    )

    if not resultado["sucesso"]:
        return resultado

    resposta = narrar_rota(resultado)

    return {
        "sucesso": True,
        "mensagem_usuario": dados.mensagem,
        "interpretacao": interpretacao,
        "rota": resultado,
        "resposta": resposta
    }