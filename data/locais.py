import unicodedata
from data.linhas import LINHAS

LOCAIS = {
    "Catedral da Sé": "Sé",
    "Pinacoteca": "Luz",
    "Museu da Língua Portuguesa": "Luz",
    "Terminal Rodoviário Tietê": "Portuguesa-Tietê",
    "Bairro da Liberdade": "Japão-Liberdade",
    "Shopping Santa Cruz": "Santa Cruz",
}

def buscar_estacao(local):
    local_normalizado = normalizar_texto(local)

    for nome_local, estacao in LOCAIS.items():
        if normalizar_texto(nome_local) == local_normalizado:
            return estacao   
    return None

def normalizar_texto(texto):
    texto = texto.strip().lower()

    texto = unicodedata.normalize("NFD", texto)

    texto= "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
    return texto

def resolver_local(entrada):
    entrada_normalizada = normalizar_texto(entrada)

    for estacoes in LINHAS.values():
        for estacao in estacoes:
            if normalizar_texto(estacao) == entrada_normalizada:
                return estacao

    return buscar_estacao(entrada)
