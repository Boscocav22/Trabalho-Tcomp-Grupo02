# test_issue1.py — testes automáticos da Issue 1.
# Rodar com: python test_issue1.py

import os
import unittest

from erros import (ErroXML, erro_estrutura, erro_sintatico, erro_tipo,
                   erro_vazio, sucesso)
from entrada import ler_arquivo
from main import validar

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testes")


def arq(nome):
    return os.path.join(PASTA, nome)


class TestEntrada(unittest.TestCase):
    def test_le_linhas_com_numero(self):
        linhas = ler_arquivo(arq("valido.xml"))
        self.assertEqual(linhas[0], (1, "<acessos>"))
        self.assertEqual(linhas[-1], (4, "</acessos>"))
        self.assertEqual(len(linhas), 4)

    def test_mantem_numeracao_original_com_linhas_em_branco(self):
        linhas = ler_arquivo(arq("valido_com_linhas_em_branco.xml"))
        self.assertEqual([n for n, _ in linhas], [2, 4, 5, 7])

    def test_arquivo_vazio(self):
        with self.assertRaises(ErroXML) as c:
            ler_arquivo(arq("vazio.xml"))
        self.assertEqual(str(c.exception), "Erro: Arquivo xml vazio")

    def test_arquivo_so_com_espacos(self):
        with self.assertRaises(ErroXML) as c:
            ler_arquivo(arq("so_espacos.xml"))
        self.assertEqual(str(c.exception), "Erro: Arquivo xml vazio")

    def test_arquivo_inexistente(self):
        with self.assertRaises(ErroXML) as c:
            ler_arquivo(arq("nao_existe.xml"))
        self.assertIn("não encontrado", str(c.exception))


class TestMensagens(unittest.TestCase):
    def test_formatos(self):
        self.assertEqual(str(erro_vazio()), "Erro: Arquivo xml vazio")
        self.assertEqual(str(erro_sintatico("Elemento <acessos> não foi aberto.")),
                         "Erro sintático: Elemento <acessos> não foi aberto.")
        self.assertEqual(str(erro_estrutura(1, "<registro>")),
                         "Erro de validação na linha 1: Estrutura inválida em <registro>.")
        self.assertEqual(str(erro_tipo(2, "<registro>")),
                         "Erro de validação na linha 2: Tipo de dados inválido em <registro>.")


class TestMain(unittest.TestCase):
    def test_valido(self):
        self.assertEqual(validar(arq("valido.xml")), sucesso())

    def test_vazio(self):
        self.assertEqual(validar(arq("vazio.xml")), "Erro: Arquivo xml vazio")


if __name__ == "__main__":
    unittest.main(verbosity=2)