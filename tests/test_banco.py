from unittest import TestCase, mock
from funcoes.banco import *


class TestBanco(TestCase):

    @mock.patch("funcoes.banco.open",
                mock.mock_open(read_data="1234;3322;10/24;165;500;799.0\n"
                                         "1434;3322;10/20;175;0;200\n"
                                         "7634;3322;10/22;142;600;100"))
    def test_validar_dados_do_cartao_ISOK(self):
        detalhes_pagamento = dict(numero="1234", senha="3322", valor_compra=9.99)
        resultado = Banco().validar_dados_do_cartao("0", detalhes_pagamento)
        self.assertTrue(resultado, True)

        detalhes_pagamento = dict(numero="9999", senha="0000", valor_compra=9.99)
        resultado = Banco().validar_dados_do_cartao("0", detalhes_pagamento)
        self.assertFalse(resultado, False)


    @mock.patch("funcoes.banco.Banco.efetuar_pagamento_com_cartao_credito")
    @mock.patch("funcoes.banco.Banco.efetuar_pagamento_com_cartao_debito")
    def test_efetuar_pagamento_ISOK(self, debito, credito):
        debito.return_value = True
        credito.return_value=True

        Banco().efetuar_pagamento("0", {})
        Banco().efetuar_pagamento("1", {})


    @mock.patch("funcoes.banco.open",
                mock.mock_open(read_data="1234;3322;10/24;165;500;799.0\n"
                                         "1434;3322;10/20;175;0;200\n"
                                         "7634;3322;10/22;142;600;100"))
    @mock.patch("funcoes.banco.Banco.validar_dados_do_cartao")
    def test_efetuar_pagamento_com_cartao_credito_ISOK(self, mock_validar_cartao):

        mock_validar_cartao.return_value=True
        detalhes_pagamento = dict(numero="1234", senha="3322", valor_compra=9.99)
        resultado = Banco().efetuar_pagamento_com_cartao_credito(detalhes_pagamento)
        self.assertTrue(resultado, True)

        mock_validar_cartao.return_value=False
        detalhes_pagamento = dict(numero="1234", senha="3322", valor_compra=9.99)
        resultado = Banco().efetuar_pagamento_com_cartao_credito(detalhes_pagamento)
        self.assertFalse(resultado, False)

    @mock.patch("funcoes.banco.open",
                mock.mock_open(read_data="1234;3322;10/24;165;500;799.0\n"
                                         "1434;3322;10/20;175;0;200\n"
                                         "7634;3322;10/22;142;600;100"))
    @mock.patch("funcoes.banco.Banco.validar_dados_do_cartao")
    def test_efetuar_pagamento_com_cartao_debito_ISOK(self, mock_validar_cartao):
        mock_validar_cartao.return_value=True
        detalhes_pagamento = dict(numero="1234", senha="3322", valor_compra=9.99)
        resultado = Banco().efetuar_pagamento_com_cartao_debito(detalhes_pagamento)
        self.assertTrue(resultado, True)

        mock_validar_cartao.return_value=False
        detalhes_pagamento = dict(numero="1234", senha="3322", valor_compra=9.99)
        resultado = Banco().efetuar_pagamento_com_cartao_debito(detalhes_pagamento)
        self.assertFalse(resultado, False)
    @mock.patch("funcoes.banco.Banco.gerar_codigo_boleto")
    def test_gerar_boleto_ISOK(self, mock_gerar):
        mock_gerar.return_value = '1802021042212474037861615099'
        dados_requisicao = dict(valor=150.99,
                                data=15,
                                conta_loja="000124578")
        boleto_como_deveria_vir = {'valor': 150.99,
                  'data_validade': 18,
                  'código': '1802021042212474037861615099',
                  'conta_recebedora': '000124578'}
        resultado = Banco().gerar_boleto(dados_requisicao)
        self.assertEqual(resultado, boleto_como_deveria_vir)


    @mock.patch("funcoes.banco.Banco")
    @mock.patch("funcoes.banco.datetime.datetime")
    def test_gerar_codigo_boleto_ISOK(self, mock_datetime, mock_banco):
        mock_datetime.now.return_value = "0000-00-00 00:00:00.000000"
        mock_banco.codigo_banco.return_value = "180"

        dados = dict(valor=10.56)
        resultado = Banco().gerar_codigo_boleto(dados)
        self.assertEqual(resultado, "180000000000000000000001056")

        mock_datetime.now.assert_called_once()
