# entrada.py — leitura do arquivo XML linha a linha.
#
# FORMATO DE DADOS TROCADO ENTRE OS MÓDULOS:
#   lista de tuplas (numero_linha, texto_da_linha)
#   - numero_linha: número real da linha no arquivo (começa em 1)
#   - texto_da_linha: conteúdo sem espaços/quebras nas pontas
#   - linhas em branco são descartadas, mas a numeração original é mantida

from erros import erro_vazio, erro_arquivo_nao_encontrado


def ler_arquivo(caminho):
    try:
        with open(caminho, encoding="utf-8") as f:
            linhas = [(i, l.strip()) for i, l in enumerate(f, start=1) if l.strip()]
    except FileNotFoundError:
        raise erro_arquivo_nao_encontrado(caminho)

    if not linhas:
        raise erro_vazio()
    return linhas
