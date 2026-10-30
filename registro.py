# registro.py — Issue 3: Validação Estrutural do Bloco <registro>
#
# Contrato:
#   recebe: n (número da linha), texto (a linha do <registro>)
#   devolve: dict {"id_cracha": str, "status": str, "hora": str}
#   erro:    raise erro_estrutura(n, texto)
#
# Estratégia: Expressão Regular compilada (AFD equivalente).
#   O <registro> tem estrutura PLANA e FIXA — sem aninhamento recursivo —
#   o que o classifica como Linguagem Regular, podendo
#   ser reconhecido por um Autômato Finito Determinístico.
#   Pelo Teorema de Kleene, toda Linguagem Regular possui uma ER equivalente,
#   portanto o uso de re.compile é formalmente justificado pela TComp.

import re

from erros import erro_estrutura

# Padrão que reconhece exatamente uma linha de <registro> bem-formada.
# Cada grupo ([^<>]*) captura o valor interno sem permitir '<' ou '>',
# o que impede tags aninhadas ou mal-formadas dentro das folhas.
# Os âncoras ^ e $ garantem que nada exista fora da estrutura esperada.
_PADRAO_REGISTRO = re.compile(
    r"^<registro>"
    r"<id_cracha>([^<>]*)</id_cracha>"
    r"<status>([^<>]*)</status>"
    r"<hora>([^<>]*)</hora>"
    r"</registro>$"
)


def validar_registro(n, texto):
    """Valida a estrutura sintática de uma linha de <registro>."""

    match = _PADRAO_REGISTRO.match(texto.strip())

    if not match:
        raise erro_estrutura(n, texto)

    id_cracha, status, hora = match.groups()
    return {"id_cracha": id_cracha, "status": status, "hora": hora}
