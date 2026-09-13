LOCAIS = {
    "Catedral da Sé": "Sé",
    "Pinacoteca": "Luz",
    "Museu da Língua Portuguesa": "Luz",
    "Terminal Rodoviário Tietê": "Portuguesa-Tietê",
    "Bairro da Liberdade": "Japão-Liberdade",
    "Shopping Santa Cruz": "Santa Cruz",
}

def buscar_estacao(local):
    return LOCAIS.get(local)