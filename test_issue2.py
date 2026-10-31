# test_issue2.py — Testes automáticos da Issue 2 (validar_raiz).
# Rodar com: python test_issue2.py

import unittest

from erros import ErroXML, erro_sintatico
from raiz import validar_raiz


class TestRaizValida(unittest.TestCase):
    def test_documento_com_registros_retorna_apenas_linhas_internas(self):
        linhas = [
            (1, "<acessos>"),
            (2, "<registro>...</registro>"),
            (4, "<registro>...</registro>"),
            (5, "</acessos>"),
        ]

        self.assertEqual(validar_raiz(linhas), linhas[1:-1])

    def test_documento_sem_registros_e_valido(self):
        linhas = [(1, "<acessos>"), (2, "</acessos>")]

        self.assertEqual(validar_raiz(linhas), [])

    def test_espacos_externos_nas_tags_sao_ignorados(self):
        linhas = [(1, "  <acessos>  "), (3, "</acessos>  ")]

        self.assertEqual(validar_raiz(linhas), [])


class TestRaizInvalida(unittest.TestCase):
    def _deve_ser_erro_sintatico(self, linhas, mensagem):
        with self.assertRaises(ErroXML) as contexto:
            validar_raiz(linhas)
        self.assertEqual(str(contexto.exception), str(erro_sintatico(mensagem)))

    def test_lista_vazia(self):
        self._deve_ser_erro_sintatico(
            [], "Elemento <acessos> não foi aberto."
        )

    def test_tag_de_abertura_ausente(self):
        self._deve_ser_erro_sintatico(
            [(1, "<registro/>"), (2, "</acessos>")],
            "Elemento <acessos> não foi aberto.",
        )

    def test_tag_de_fechamento_ausente(self):
        self._deve_ser_erro_sintatico(
            [(1, "<acessos>"), (2, "<registro/>")],
            "Elemento <acessos> não foi fechado.",
        )

    def test_tag_raiz_duplicada_no_interior(self):
        self._deve_ser_erro_sintatico(
            [(1, "<acessos>"), (2, "<acessos>"), (3, "</acessos>")],
            "Elemento <acessos> deve aparecer somente uma vez.",
        )

    def test_fechamento_raiz_duplicado_no_interior(self):
        self._deve_ser_erro_sintatico(
            [(1, "<acessos>"), (2, "</acessos>"), (3, "</acessos>")],
            "Elemento <acessos> deve aparecer somente uma vez.",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
