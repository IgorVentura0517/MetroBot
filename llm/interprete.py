import json

from llm.cliente import chamar_llm


def interpretar_mensagem(mensagem):
    prompt = f"""
Você é o interpretador de comandos do MetrôBot.

Sua função é obter informações da mensagem do usuário.

Retorne APENAS um JSON válido, sem explicações, sem markdown e sem texto adicional.

Formato obrigatório:

{{
    "origem": "local informado pelo usuário",
    "destino": "local informado pelo usuário",
    "algoritmo": "bfs"
}}

Regras:
- Não calcule nenhuma rota.
- Não invente estações ou locais.
- Preserve os nomes mencionados pelo usuário.
- O algoritmo padrão é "bfs".
- Se o usuário pedir explicitamente DFS, use "dfs".
- Se origem ou destino não forem identificados, use null.

Mensagem do usuário:
"{mensagem}"
"""

    resposta = chamar_llm(prompt)

    try:
        dados = json.loads(resposta)
    except json.JSONDecodeError:
        return {
            "sucesso": False,
            "erro": "O LLM retornou uma resposta inválida."
        }

    origem = dados.get("origem")
    destino = dados.get("destino")
    algoritmo = dados.get("algoritmo", "bfs")

    if not origem:
        return {
            "sucesso": False,
            "erro": "Não foi possível identificar a origem."
        }

    if not destino:
        return {
            "sucesso": False,
            "erro": "Não foi possível identificar o destino."
        }

    if algoritmo not in ("bfs", "dfs"):
        algoritmo = "bfs"

    return {
        "sucesso": True,
        "origem": origem,
        "destino": destino,
        "algoritmo": algoritmo
    }