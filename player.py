# player.py
class Jogador:
    def __init__(self, nome, saldo_inicial=1000.0):
        self.nome = nome
        self.saldo = saldo_inicial
        self.carteira = {}  # nome_acao -> (quantidade, preco_medio)
        self.historico = []

    def comprar_acao(self, acao, quantidade):
        custo_total = acao.preco_atual * quantidade
        if custo_total > self.saldo:
            return False
        self.saldo -= custo_total
        if acao.nome in self.carteira:
            qtd_antiga, preco_antigo = self.carteira[acao.nome]
            nova_qtd = qtd_antiga + quantidade
            novo_preco = ((qtd_antiga * preco_antigo) + custo_total) / nova_qtd
            self.carteira[acao.nome] = (nova_qtd, novo_preco)
        else:
            self.carteira[acao.nome] = (quantidade, acao.preco_atual)
        self.historico.append(f"Comprou {quantidade}x {acao.nome} a ${acao.preco_atual}")
        return True

    def vender_acao(self, acao, quantidade):
        if acao.nome not in self.carteira or self.carteira[acao.nome][0] < quantidade:
            return False
        qtd_antiga, preco_medio = self.carteira[acao.nome]
        ganho = acao.preco_atual * quantidade
        self.saldo += ganho
        nova_qtd = qtd_antiga - quantidade
        if nova_qtd > 0:
            self.carteira[acao.nome] = (nova_qtd, preco_medio)
        else:
            del self.carteira[acao.nome]
        self.historico.append(f"Vendeu {quantidade}x {acao.nome} a ${acao.preco_atual}")
        return True

    def resumo_carteira(self, mercado):
        resumo = []
        for nome, (qtd, preco_medio) in self.carteira.items():
            acao = mercado.get_acao_por_nome(nome)
            atual = acao.preco_atual
            total_pago = preco_medio * qtd
            total_atual = atual * qtd
            lucro = round(total_atual - total_paid, 2)
            resumo.append((nome, qtd, preco_medio, atual, lucro))
        return resumo
