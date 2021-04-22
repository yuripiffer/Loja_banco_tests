import datetime


class Banco:

    def __init__(self):
        self.saldo = 50000000
        self.codigo_banco = 180
        self.codigo_tipo_pagamento = {"0": self.efetuar_pagamento_com_cartao_credito,
                                      "1": self.efetuar_pagamento_com_cartao_debito}

    def validar_dados_do_cartao(self, modalidade_pagamento, detalhes_pagamento):
        with open("cartoes.txt", "r") as file:
            lines = file.readlines()

        verificacoes = []
        for linha in lines:
            linha = linha.split(";")
            if detalhes_pagamento["numero"] == linha[0]:
                verificacoes.append(detalhes_pagamento["senha"] == linha[1])
                verificacoes.append(datetime.datetime.strptime(linha[2], "%m/%y") >= datetime.datetime.today())
                if modalidade_pagamento == "1":
                    verificacoes.append(detalhes_pagamento["valor_compra"] <= float(linha[4]))
                elif modalidade_pagamento == "0":
                    verificacoes.append(detalhes_pagamento["valor_compra"] <= float(linha[5].strip()))

                return all(verificacoes)

        return False

    def efetuar_pagamento(self, modalidade_pagamento: str, detalhes_pagamento: dict):
        return self.codigo_tipo_pagamento[modalidade_pagamento](detalhes_pagamento)

    def efetuar_pagamento_com_cartao_credito(self, detalhes_pagamento):
        modalidade_pagamento = "0"
        if self.validar_dados_do_cartao(modalidade_pagamento, detalhes_pagamento):
            with open("cartoes.txt", "r") as file:
                lines = file.readlines()

            with open("cartoes.txt", "w") as file:
                for i in range(len(lines)):
                    linha = lines[i].split(";")
                    if linha[0] == detalhes_pagamento["numero"]:
                        novo_saldo = float(linha[5].strip()) - detalhes_pagamento["valor_compra"]
                        linha[5] = str(novo_saldo) + "\n"
                        lines[i] = ";".join(linha)

                file.write("".join(lines))

            return True
        return False

    def efetuar_pagamento_com_cartao_debito(self, detalhes_pagamento):
        modalidade_pagamento = "1"
        if self.validar_dados_do_cartao(modalidade_pagamento, detalhes_pagamento):
            with open("cartoes.txt", "r") as file:
                lines = file.readlines()

            with open("cartoes.txt", "w") as file:
                for i in range(len(lines)):
                    linha = lines[i].split(";")
                    if linha[0] == detalhes_pagamento["numero"]:
                        novo_saldo = float(linha[4]) - detalhes_pagamento["valor_compra"]
                        linha[4] = str(novo_saldo)
                        lines[i] = ";".join(linha)

                file.write("".join(lines))

            return True
        return False

    def gerar_boleto(self, dados_requisicao: dict) -> dict:
        boleto = dict()
        boleto["valor"] = dados_requisicao["valor"]
        boleto["data_validade"] = dados_requisicao["data"] + 3
        boleto["código"] = self.gerar_codigo_boleto(dados_requisicao)
        boleto["conta_recebedora"] = dados_requisicao["conta_loja"]

        return boleto

    def gerar_codigo_boleto(self, dados_requisicao: dict) -> str:
        atual_instante = str(datetime.datetime.now())
        for simbolo in ["-", ".", ":", " "]:
            atual_instante = atual_instante.replace(simbolo, "")

        codigo = str(self.codigo_banco)
        codigo += atual_instante
        codigo += str(dados_requisicao["valor"]).replace(".", "")

        return codigo


# print(Banco().validar_dados_do_cartao("0", dict(numero="1234", senha="3322", valor_compra=9.99)))
