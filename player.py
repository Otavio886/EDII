class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.saldo = 1000.0  # Saldo inicial
        self.carteira = {}   # {nome_acao: (quantidade, preco_medio)}
        self.historico = []  # Lista de operações realizadas

    def comprar_acao(self, acao, quantidade):
        custo_total = acao.preco_atual * quantidade
        if self.saldo >= custo_total:
            self.saldo -= custo_total
            
            if acao.nome in self.carteira:
                # Atualiza quantidade e preço médio
                qtd_atual, preco_medio_atual = self.carteira[acao.nome]
                nova_qtd = qtd_atual + quantidade
                novo_preco_medio = ((qtd_atual * preco_medio_atual) + (quantidade * acao.preco_atual)) / nova_qtd
                self.carteira[acao.nome] = (nova_qtd, novo_preco_medio)
            else:
                # Primeira compra desta ação
                self.carteira[acao.nome] = (quantidade, acao.preco_atual)
            
            # Registra no histórico
            self.historico.append(f"Comprou {quantidade} de {acao.nome} por ${acao.preco_atual:.2f} cada")
            return True
        return False

    def vender_acao(self, acao, quantidade):
        if acao.nome in self.carteira:
            qtd_atual, preco_medio = self.carteira[acao.nome]
            if qtd_atual >= quantidade:
                # Vende as ações
                valor_venda = acao.preco_atual * quantidade
                self.saldo += valor_venda
                
                # Atualiza a carteira
                nova_qtd = qtd_atual - quantidade
                if nova_qtd == 0:
                    del self.carteira[acao.nome]
                else:
                    self.carteira[acao.nome] = (nova_qtd, preco_medio)
                
                # Registra no histórico
                lucro = (acao.preco_atual - preco_medio) * quantidade
                self.historico.append(f"Vendeu {quantidade} de {acao.nome} por ${acao.preco_atual:.2f} cada (Lucro: ${lucro:.2f})")
                return True
        return False

    def get_valor_carteira(self, mercado):
        """Calcula o valor total da carteira no mercado atual"""
        valor_total = 0
        for nome_acao, (quantidade, _) in self.carteira.items():
            acao = mercado.get_acao_por_nome(nome_acao)
            if acao:
                valor_total += acao.preco_atual * quantidade
        return valor_total

    def get_patrimonio_total(self, mercado):
        """Retorna saldo + valor da carteira"""
        return self.saldo + self.get_valor_carteira(mercado)