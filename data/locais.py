import unicodedata
from data.linhas import LINHAS

LOCAIS = {
   "Shopping Metrô Tucuruvi": "Tucuruvi",
    "Terminal Rodoviário Tietê": "Portuguesa-Tietê",
    "Pinacoteca": "Luz",
    "Catedral da Sé": "Sé",
    "Bairro da Liberdade": "Japão-Liberdade",
    "Terminal Rodoviário Jabaquara": "Jabaquara",
    "Hospital das Clínicas": "Clínicas",
    "MASP": "Trianon-Masp",
    "Parque da Independência": "Santos-Imigrantes",
    "Theatro Municipal": "Anhangabaú",
    "Mercado Municipal": "São Bento",
    "Neo Química Arena": "Corinthians-Itaquera",
    "Mooca": "Bresser-Mooca"
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
