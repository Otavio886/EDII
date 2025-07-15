# market.py
import random

class Acao:
    def __init__(self, nome, preco_inicial):
        self.nome = nome
        self.preco_atual = preco_inicial
        self.historico = [preco_inicial]
        self.tendencia = random.choice(['alta', 'baixa', 'estavel'])

    def atualizar_preco(self):
        variacao = random.uniform(-0.05, 0.05)
        if self.tendencia == 'alta':
            variacao += 0.02
        elif self.tendencia == 'baixa':
            variacao -= 0.02
        novo_preco = round(self.preco_atual * (1 + variacao), 2)
        self.preco_atual = max(novo_preco, 1.0)
        self.historico.append(self.preco_atual)

    def get_historico(self):
        return self.historico

class Mercado:
    def __init__(self):
        self.acoes = []
        self.dia = 0
        self.gerar_acoes_iniciais()

    def gerar_acoes_iniciais(self):
        nomes = [
            'TechWave', 'AgroPlus', 'BankNow', 'HealthMax', 'GreenEnergy',
            'EduSmart', 'Foodies', 'TravelNow', 'BuildIt', 'FashionX',
            'PetLovers', 'AutoDrive', 'MobiPay', 'BioGen', 'CloudNet'
        ]
        for nome in nomes:
            preco_inicial = round(random.uniform(10, 100), 2)
            self.acoes.append(Acao(nome, preco_inicial))

    def avancar_dia(self):
        self.dia += 1
        for acao in self.acoes:
            acao.atualizar_preco()

    def listar_acoes(self):
        return [(acao.nome, acao.preco_atual) for acao in self.acoes]

    def get_acao_por_nome(self, nome):
        for acao in self.acoes:
            if acao.nome == nome:
                return acao
        return None
