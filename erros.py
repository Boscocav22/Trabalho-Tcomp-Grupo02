# erros.py — padrão de mensagens de erro e sucesso usado por TODOS os módulos.
# Qualquer módulo que encontrar um problema faz: raise erro_xxx(...)
# O main captura ErroXML e imprime a mensagem.


class ErroXML(Exception):
    """Exceção única do projeto. A mensagem já vem formatada."""
    pass


def erro_vazio():
    return ErroXML("Erro: Arquivo xml vazio")


def erro_arquivo_nao_encontrado(caminho):
    return ErroXML(f"Erro: Arquivo {caminho} não encontrado")


def erro_sintatico(msg):
    # Ex.: erro_sintatico("Elemento <acessos> não foi aberto.")
    return ErroXML(f"Erro sintático: {msg}")


def erro_estrutura(n, texto):
    return ErroXML(f"Erro de validação na linha {n}: Estrutura inválida em {texto}.")


def erro_tipo(n, texto):
    return ErroXML(f"Erro de validação na linha {n}: Tipo de dados inválido em {texto}.")


def sucesso():
    return "Sucesso: Arquivo XML válido."
