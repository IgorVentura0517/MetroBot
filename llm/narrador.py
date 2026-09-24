import json

from llm.cliente import chamar_llm


def narrar_rota(resultado):
    if not resultado.get("sucesso"):
        return resultado.get(
            "erro",
            "Não foi possível calcular a rota."
        )

    prompt = f"""
Você é o assistente MetrôBot.

Sua função é explicar de forma clara e objetiva uma rota de metrô
que JÁ FOI CALCULADA pelo sistema.

Você NÃO deve:
- recalcular a rota;
- alterar estações;
- inventar estações;
- alterar baldeações;
- sugerir caminhos diferentes.

Apenas transforme os dados fornecidos em uma resposta natural.

Dados da rota:

{json.dumps(resultado, ensure_ascii=False, indent=2)}

Explique:
- estação de origem;
- estação de destino;
- sequência de estações;
- onde devem ser feitas as baldeações;
- total de baldeações.

Se não houver baldeações, informe isso.

Não mencione detalhes técnicos como BFS, DFS ou ordem de visita,
a menos que seja necessário.
"""

    return chamar_llm(prompt)