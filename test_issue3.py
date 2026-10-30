# test_issue3.py — Testes automáticos da Issue 3 (validar_registro).
# Rodar com: python test_issue3.py

import unittest

from erros import ErroXML, erro_estrutura
from registro import validar_registro


def _msg_esperada(n, texto):
    """Retorna a mensagem de erro_estrutura esperada para comparação."""
    return str(erro_estrutura(n, texto))



# Casos VÁLIDOS — devem retornar o dicionário sem lançar exceção
class TestRegistroValido(unittest.TestCase):

    def test_linha_tipica(self):
        """Registro padrão exatamente como aparece em acessos.xml."""
        r = validar_registro(2, "<registro><id_cracha>98765</id_cracha><status>ENTRADA</status><hora>0830</hora></registro>")
        self.assertEqual(r, {"id_cracha": "98765", "status": "ENTRADA", "hora": "0830"})

    def test_status_saida(self):
        """Status 'SAIDA' também é estruturalmente válido."""
        r = validar_registro(5, "<registro><id_cracha>12345</id_cracha><status>SAIDA</status><hora>1745</hora></registro>")
        self.assertEqual(r, {"id_cracha": "12345", "status": "SAIDA", "hora": "1745"})

    def test_id_grande(self):
        """ID com muitos dígitos (sem limite superior) deve passar."""
        r = validar_registro(11, "<registro><id_cracha>9999999999</id_cracha><status>ENTRADA</status><hora>2359</hora></registro>")
        self.assertEqual(r["id_cracha"], "9999999999")

    def test_valores_semanticamente_invalidos_passam(self):
        """Issue 3 NÃO valida semântica — valores errados devem passar aqui."""
        r = validar_registro(1, "<registro><id_cracha>-5</id_cracha><status>TALVEZ</status><hora>830</hora></registro>")
        self.assertEqual(r, {"id_cracha": "-5", "status": "TALVEZ", "hora": "830"})

    def test_campo_vazio_passa(self):
        """Campo vazio é estruturalmente aceitável; Issue 4 deve rejeitar."""
        r = validar_registro(1, "<registro><id_cracha></id_cracha><status></status><hora></hora></registro>")
        self.assertEqual(r, {"id_cracha": "", "status": "", "hora": ""})

    def test_strip_de_espacos_externos(self):
        """Espaços nas bordas da linha devem ser ignorados (como faz ler_arquivo)."""
        r = validar_registro(3, "  <registro><id_cracha>1</id_cracha><status>ENTRADA</status><hora>0000</hora></registro>  ")
        self.assertEqual(r["id_cracha"], "1")



# Casos INVÁLIDOS — todos devem lançar ErroXML com mensagem de erro_estrutura
class TestRegistroInvalido(unittest.TestCase):

    def _deve_ser_erro_estrutura(self, n, texto):
        """Auxiliar: confirma que ErroXML é levantada com a mensagem correta."""
        with self.assertRaises(ErroXML) as ctx:
            validar_registro(n, texto)
        self.assertEqual(str(ctx.exception), _msg_esperada(n, texto))

    def test_sem_tag_abertura_registro(self):
        """Falta <registro> de abertura."""
        self._deve_ser_erro_estrutura(
            2,
            "<id_cracha>1</id_cracha><status>ENTRADA</status><hora>0000</hora></registro>"
        )

    def test_sem_tag_fechamento_registro(self):
        """Falta </registro> de fechamento."""
        self._deve_ser_erro_estrutura(
            2,
            "<registro><id_cracha>1</id_cracha><status>ENTRADA</status><hora>0000</hora>"
        )

    def test_tag_id_faltando(self):
        """Tag <id_cracha> ausente."""
        self._deve_ser_erro_estrutura(
            3,
            "<registro><status>ENTRADA</status><hora>0830</hora></registro>"
        )

    def test_tag_status_faltando(self):
        """Tag <status> ausente."""
        self._deve_ser_erro_estrutura(
            3,
            "<registro><id_cracha>123</id_cracha><hora>0830</hora></registro>"
        )

    def test_tag_hora_faltando(self):
        """Tag <hora> ausente."""
        self._deve_ser_erro_estrutura(
            4,
            "<registro><id_cracha>123</id_cracha><status>SAIDA</status></registro>"
        )

    def test_ordem_errada_status_antes_id(self):
        """Ordem trocada: <status> antes de <id_cracha>."""
        self._deve_ser_erro_estrutura(
            5,
            "<registro><status>ENTRADA</status><id_cracha>123</id_cracha><hora>0000</hora></registro>"
        )

    def test_ordem_errada_hora_antes_status(self):
        """Ordem trocada: <hora> antes de <status>."""
        self._deve_ser_erro_estrutura(
            5,
            "<registro><id_cracha>123</id_cracha><hora>0000</hora><status>ENTRADA</status></registro>"
        )

    def test_tag_desconhecida_extra(self):
        """Tag extra <nome> não pertence ao esquema."""
        self._deve_ser_erro_estrutura(
            6,
            "<registro><id_cracha>1</id_cracha><status>ENTRADA</status><hora>0000</hora><nome>Arthur</nome></registro>"
        )

    def test_tag_id_duplicada(self):
        """<id_cracha> duplicada."""
        self._deve_ser_erro_estrutura(
            6,
            "<registro><id_cracha>1</id_cracha><id_cracha>2</id_cracha><status>ENTRADA</status><hora>0000</hora></registro>"
        )

    def test_tag_status_duplicada(self):
        """<status> duplicado."""
        self._deve_ser_erro_estrutura(
            7,
            "<registro><id_cracha>1</id_cracha><status>ENTRADA</status><status>SAIDA</status><hora>0000</hora></registro>"
        )

    def test_tag_nao_fechada(self):
        """Tag <id_cracha> sem fechamento (tag aberta ao invés de fechada)."""
        self._deve_ser_erro_estrutura(
            8,
            "<registro><id_cracha>123<id_cracha><status>ENTRADA</status><hora>0000</hora></registro>"
        )

    def test_texto_solto_antes_de_registro(self):
        """Texto livre antes de <registro>."""
        self._deve_ser_erro_estrutura(
            9,
            "abc<registro><id_cracha>1</id_cracha><status>ENTRADA</status><hora>0000</hora></registro>"
        )

    def test_texto_solto_apos_registro(self):
        """Texto livre após </registro>."""
        self._deve_ser_erro_estrutura(
            9,
            "<registro><id_cracha>1</id_cracha><status>ENTRADA</status><hora>0000</hora></registro>xyz"
        )

    def test_texto_solto_entre_tags_filhas(self):
        """Texto solto entre as tags filhas."""
        self._deve_ser_erro_estrutura(
            10,
            "<registro><id_cracha>1</id_cracha>LIXO<status>ENTRADA</status><hora>0000</hora></registro>"
        )

    def test_tag_com_angulo_no_valor(self):
        """Valor com '<' (tentativa de injetar tag) deve ser rejeitado."""
        self._deve_ser_erro_estrutura(
            11,
            "<registro><id_cracha><evil></id_cracha><status>ENTRADA</status><hora>0000</hora></registro>"
        )

    def test_linha_completamente_vazia(self):
        """String vazia não é um <registro> válido."""
        self._deve_ser_erro_estrutura(1, "")

    def test_apenas_tag_registro_vazia(self):
        """<registro></registro> sem filhas."""
        self._deve_ser_erro_estrutura(
            2,
            "<registro></registro>"
        )



# Verificação do formato da mensagem de erro 
class TestFormatoMensagemErro(unittest.TestCase):

    def test_mensagem_contem_numero_da_linha(self):
        """A mensagem de erro deve conter o número da linha."""
        with self.assertRaises(ErroXML) as ctx:
            validar_registro(42, "<registro_invalido/>")
        self.assertIn("42", str(ctx.exception))

    def test_mensagem_contem_texto_da_linha(self):
        """A mensagem de erro deve conter o texto que causou o erro."""
        texto = "<registro_invalido/>"
        with self.assertRaises(ErroXML) as ctx:
            validar_registro(1, texto)
        self.assertIn(texto, str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
