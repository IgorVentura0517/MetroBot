import unicodedata

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
