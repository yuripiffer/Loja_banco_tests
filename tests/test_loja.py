from unittest import TestCase, mock
from funcoes.loja import *


class TestLoja(TestCase):

    @mock.patch("funcoes.banco.Banco.efetuar_pagamento")
    def test_solicitar_pagamento_com_cartao_ISOK(self, mock_pagamento):
        dados_cartao = dict(numero=1734, senha=3322)

        mock_pagamento.return_value = True
        resultado = Loja().solicitar_pagamento_com_cartao(dados_cartao,9.99, "0")
        self.assertTrue(resultado, True)

        mock_pagamento.return_value = False
        resultado = Loja().solicitar_pagamento_com_cartao(dados_cartao,9.99, "2")
        self.assertFalse(resultado, False)



    @mock.patch("funcoes.banco.Banco.gerar_boleto")
    def test_solicitar_boleto_ISOK(self, mock_boleto):
        mock_boleto.return_values =  {'valor': 150.99,
                                      'data_validade': 18,
                                      'código': '1802021042214283055948715099',
                                      'conta_recebedora': '000124578'}

        resultado = Loja().solicitar_boleto(dict(valor=150.99, data=15))
        resultado_forcado = {'valor': 150.99,
                             'data_validade': 18,
                             'código': '1802021042214283055948715099',
                             'conta_recebedora': '000124578'}
        self.assertTrue(resultado, resultado_forcado)


    def test_efetuar_pagamento_com_dinheiro_ISOK(self):
        resultado = Loja().efetuar_pagamento_com_dinheiro(0, 30)
        self.assertFalse(resultado, False)

        resultado = Loja().efetuar_pagamento_com_dinheiro(30, 0)
        self.assertTrue(resultado, True)




