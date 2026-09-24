import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")


def chamar_llm(prompt):
    if not API_KEY:
        raise ValueError(
            "GROQ_API_KEY não encontrada no arquivo .env"
        )

    cliente = Groq(api_key=API_KEY)

    resposta = cliente.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return resposta.choices[0].message.content