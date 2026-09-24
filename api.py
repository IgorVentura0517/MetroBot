import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from data.linhas import LINHAS
from core.grafo import construir_grafo_multilinhas
from core.logica import criar_fatos
from core.planejador import planejar_rota
from interface.app import montar_dados
from llm.interprete import interpretar_mensagem
from llm.narrador import narrar_rota


app = FastAPI(
    title="MetrôBot API",
    version="1.0.0"
)


grafo, linhas_do_trecho = construir_grafo_multilinhas(LINHAS)

PASTA_INTERFACE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "interface",
    "static"
)

app.mount(
    "/static",
    StaticFiles(directory=PASTA_INTERFACE),
    name="static"
)


class RotaRequest(BaseModel):
    origem: str
    destino: str
    algoritmo: str = "bfs"
    bloqueadas: list[str] = []
    linhas_indisponiveis: list[str] = []

class ChatRequest(BaseModel):
    mensagem: str


@app.get("/")
def inicio():
    return FileResponse(
        os.path.join(PASTA_INTERFACE, "index.html")
    )


@app.get("/status")
def status():
    return {
        "nome": "MetrôBot API",
        "status": "online"
    }


@app.get("/dados")
def dados():
    return montar_dados()


@app.post("/rota")
def calcular_rota(dados: RotaRequest):
    fatos = criar_fatos(
        dados.bloqueadas,
        dados.linhas_indisponiveis
    )

    resultado = planejar_rota(
        grafo,
        linhas_do_trecho,
        dados.origem,
        dados.destino,
        algoritmo=dados.algoritmo,
        fatos=fatos
    )

    return resultado

@app.post("/chat")
def conversar(dados: ChatRequest):

    try:
        interpretacao = interpretar_mensagem(dados.mensagem)
    except Exception as erro:
        return {
            "sucesso": False,
            "erro": f"Não foi possível falar com o LLM: {erro}"
        }

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
        return {
            "sucesso": False,
            "erro": resultado["erro"],
            "interpretacao": interpretacao
        }

    try:
        resposta = narrar_rota(resultado)
    except Exception as erro:
        resposta = f"(Narração indisponível: {erro})"

    return {
        "sucesso": True,
        "mensagem_usuario": dados.mensagem,
        "interpretacao": interpretacao,
        "rota": resultado,
        "resposta": resposta
    }
