# raiz.py — Issue 2: validação do elemento raiz <acessos>.
#
# Contrato:
#   recebe: lista de (n, texto) com as linhas não vazias do arquivo
#   devolve: lista de (n, texto) entre <acessos> e </acessos>
#   erro:    raise erro_sintatico(...)

from erros import erro_sintatico


def validar_raiz(linhas):
    """Valida as tags externas do documento e retorna as linhas internas."""
    if not linhas:
        raise erro_sintatico("Elemento <acessos> não foi aberto.")

    _, primeiro_texto = linhas[0]
    if primeiro_texto.strip() != "<acessos>":
        raise erro_sintatico("Elemento <acessos> não foi aberto.")

    _, ultimo_texto = linhas[-1]
    if ultimo_texto.strip() != "</acessos>":
        raise erro_sintatico("Elemento <acessos> não foi fechado.")

    internas = linhas[1:-1]
    for _, texto in internas:
        if texto.strip() in ("<acessos>", "</acessos>"):
            raise erro_sintatico("Elemento <acessos> deve aparecer somente uma vez.")

    return internas
