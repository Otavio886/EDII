# challenges.py
class Desafio:
    def __init__(self, descricao, meta_lucro, dias_max):
        self.descricao = descricao
        self.meta_lucro = meta_lucro
        self.dias_max = dias_max
        self.dias_passados = 0
        self.iniciado = False

    def iniciar(self):
        self.dias_passados = 0
        self.iniciado = True

    def avancar_dia(self):
        if self.iniciado:
            self.dias_passados += 1

    def verificar_conclusao(self, lucro_total):
        if not self.iniciado:
            return False
        if self.dias_passados > self.dias_max:
            return "falhou"
        if lucro_total >= self.meta_lucro:
            return "concluido"
        return "em andamento"
