# main.py — orquestra os módulos das Issues 2, 3 e 4 e imprime o resultado.
# Uso: python main.py caminho/do/arquivo.xml

import sys

from erros import ErroXML, sucesso
from entrada import ler_arquivo
from raiz import validar_raiz          # Issue 2
from registro import validar_registro  # Issue 3
from tipos import validar_tipos        # Issue 4


def validar(caminho):
    """Retorna a mensagem final (sucesso ou o primeiro erro encontrado)."""
    try:
        linhas = ler_arquivo(caminho)
        internas = validar_raiz(linhas)
        for n, texto in internas:
            valores = validar_registro(n, texto)
            validar_tipos(n, texto, valores)
        return sucesso()
    except ErroXML as e:
        return str(e)


def main():
    caminho = sys.argv[1] if len(sys.argv) > 1 else "acessos.xml"
    print(validar(caminho))


if __name__ == "__main__":
    main()
