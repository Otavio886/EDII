import tkinter as tk
from tkinter import ttk, messagebox
from market import Mercado
from player import Jogador
from algorithms import buscar

# Lista de desafios progressivos
DESAFIOS = [
    ("Lucre $200 em 10 dias", 200, 10),
    ("Lucre $500 em 8 dias", 500, 8),
    ("Lucre $1000 em 7 dias", 1000, 7),
    ("Sobreviva 15 dias com saldo positivo", 0, 15),
    ("Multiplique o saldo por 2 em 20 dias", 1000, 20)
]

class Desafio:
    def __init__(self, descricao, lucro_necessario, dias_max):
        self.descricao = descricao
        self.lucro_necessario = lucro_necessario
        self.dias_max = dias_max
        self.dia_atual = 0
        self.ativo = False

    def iniciar(self):
        self.ativo = True
        self.dia_atual = 0

    def avancar_dia(self):
        if self.ativo:
            self.dia_atual += 1

    def verificar_conclusao(self, lucro, saldo):
        if not self.ativo:
            return "inativo"
        if "Sobreviva" in self.descricao:
            if self.dia_atual >= self.dias_max:
                self.ativo = False
                return "concluido" if saldo > 0 else "falhou"
        else:
            if lucro >= self.lucro_necessario:
                self.ativo = False
                return "concluido"
            elif self.dia_atual >= self.dias_max:
                self.ativo = False
                return "falhou"
        return "em andamento"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador da Bolsa de Valores")
        self.root.geometry("800x600")
        self.mercado = Mercado()
        self.jogador = Jogador("Investidor")
        self.desafio_atual = None
        self.proximo_desafio = 0

        # Elementos para busca
        self.busca_var_substring = tk.StringVar()
        self.busca_var_substring.trace_add('write', lambda *args: self.atualizar_tela())

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill='both', expand=True)

        self.tab_mercado = ttk.Frame(self.tabs)
        self.tab_carteira = ttk.Frame(self.tabs)
        self.tab_desafios = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_mercado, text='📈 Mercado')
        self.tabs.add(self.tab_carteira, text='💼 Carteira')
        self.tabs.add(self.tab_desafios, text='🎯 Desafios')

        self.status_bar = tk.Label(root, text="Dia: 0 | Saldo: $1000.00", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.setup_mercado()
        self.setup_carteira()
        self.setup_desafios()
        self.atualizar_tela()

    def setup_mercado(self):
        self.label_desafio_mercado = ttk.Label(self.tab_mercado, text="", foreground="blue")
        self.label_desafio_mercado.pack(pady=5)

        # Frame com scrollbar para ações do mercado
        frame_acoes_container = ttk.Frame(self.tab_mercado)
        frame_acoes_container.pack(fill='both', expand=True, padx=10, pady=10)
        canvas = tk.Canvas(frame_acoes_container)
        scrollbar = ttk.Scrollbar(frame_acoes_container, orient='vertical', command=canvas.yview)
        self.frame_acoes = ttk.Frame(canvas)
        self.frame_acoes.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.frame_acoes, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        self.btn_avancar = ttk.Button(self.tab_mercado, text="⏭️ Avançar 1 Dia", command=self.avancar_dia)
        self.btn_avancar.pack(pady=5)

        # Filtro substring no mercado (Rabin-Karp)
        busca_frame_sub = ttk.Frame(self.tab_mercado)
        busca_frame_sub.pack(pady=5)
        ttk.Label(busca_frame_sub, text="Filtrar ações por substring:").pack(side=tk.LEFT)
        ttk.Entry(busca_frame_sub, textvariable=self.busca_var_substring, width=15).pack(side=tk.LEFT, padx=2)


    def setup_carteira(self):
        self.frame_carteira = ttk.Frame(self.tab_carteira)
        self.frame_carteira.pack(fill='both', expand=True, padx=10, pady=10)

        # Filtro substring na carteira (Rabin-Karp)
        busca_frame = ttk.Frame(self.tab_carteira)
        busca_frame.pack(pady=5)
        self.busca_carteira_var = tk.StringVar()
        self.busca_carteira_var.trace_add('write', lambda *args: self.atualizar_tela())
        ttk.Label(busca_frame, text="Filtrar ações na carteira por substring:").pack(side=tk.LEFT)
        ttk.Entry(busca_frame, textvariable=self.busca_carteira_var, width=15).pack(side=tk.LEFT, padx=2)



    def setup_desafios(self):
        self.frame_desafios = ttk.Frame(self.tab_desafios)
        self.frame_desafios.pack(fill='both', expand=True, padx=10, pady=10)
        self.label_desafios = ttk.Label(self.frame_desafios, text="Desafios disponíveis:")
        self.label_desafios.pack(pady=5)
        self.lista_desafios = ttk.Frame(self.frame_desafios)
        self.lista_desafios.pack()

        self.atualizar_desafios_disponiveis()

    def atualizar_desafios_disponiveis(self):
        for widget in self.lista_desafios.winfo_children():
            widget.destroy()

        if self.proximo_desafio < len(DESAFIOS):
            desc, lucro, dias = DESAFIOS[self.proximo_desafio]
            frame = ttk.Frame(self.lista_desafios, padding=5)
            frame.pack()
            lbl = ttk.Label(frame, text=desc)
            lbl.pack(side=tk.LEFT, padx=5)
            btn = ttk.Button(frame, text="Iniciar Desafio", command=self.iniciar_desafio)
            btn.pack(side=tk.LEFT, padx=5)
        else:
            lbl = ttk.Label(self.lista_desafios, text="Todos os desafios foram concluídos! 🎉")
            lbl.pack()

    def iniciar_desafio(self):
        desc, lucro, dias = DESAFIOS[self.proximo_desafio]
        self.desafio_atual = Desafio(desc, lucro, dias)
        self.desafio_atual.iniciar()
        self.tabs.select(self.tab_mercado)
        messagebox.showinfo("Desafio Iniciado", f"{desc}")
        self.atualizar_tela()

    def atualizar_tela(self):
        self.label_desafio_mercado.config(text=f"Desafio: {self.desafio_atual.descricao}" if self.desafio_atual and self.desafio_atual.ativo else "")

        # Atualizar ações com filtro substring (Rabin-Karp)
        for widget in self.frame_acoes.winfo_children():
            widget.destroy()
        filtro = self.busca_var_substring.get()
        acoes = self.mercado.listar_acoes()
        if filtro:
            acoes = [(nome, preco) for nome, preco in acoes if buscar('rabin_karp', nome, filtro) != -1]
        for nome, preco in acoes:
            qtd = self.jogador.carteira.get(nome, (0,))[0]
            frame = ttk.Frame(self.frame_acoes, relief=tk.RIDGE, padding=10)
            frame.pack(fill='x', pady=5)
            lbl = ttk.Label(frame, text=f"{nome} - ${preco:.2f}  |  Qtde: {qtd}")
            lbl.pack(side=tk.LEFT)
            ttk.Button(frame, text="Comprar", command=lambda n=nome: self.comprar_acao(n)).pack(side=tk.LEFT, padx=5)
            ttk.Button(frame, text="Vender", command=lambda n=nome: self.vender_acao(n)).pack(side=tk.LEFT)

        # Atualizar carteira com filtro substring (Rabin-Karp)
        for widget in self.frame_carteira.winfo_children():
            widget.destroy()
        filtro_carteira = self.busca_carteira_var.get()
        carteira_itens = list(self.jogador.carteira.items())
        if filtro_carteira:
            carteira_itens = [(nome, v) for nome, v in carteira_itens if buscar('rabin_karp', nome, filtro_carteira) != -1]
        for nome, (qtd, preco_medio) in carteira_itens:
            acao = self.mercado.get_acao_por_nome(nome)
            lucro = (acao.preco_atual - preco_medio) * qtd
            cor = "green" if lucro >= 0 else "red"
            txt = f"{nome}: {qtd} ações | Preço Médio: ${preco_medio:.2f} | Atual: ${acao.preco_atual:.2f} | Lucro: ${lucro:.2f}"
            lbl = tk.Label(self.frame_carteira, text=txt, fg=cor)
            lbl.pack(anchor='w', pady=2)

        lucro_total = self.calcular_lucro_total()
        self.status_bar.config(text=f"Dia: {self.mercado.dia} | Saldo: ${self.jogador.saldo:.2f} | Lucro Total: ${lucro_total:.2f}")

        if self.desafio_atual:
            status = self.desafio_atual.verificar_conclusao(lucro_total, self.jogador.saldo)
            if status == "concluido":
                messagebox.showinfo("Desafio", "Parabéns! Você concluiu o desafio!")
                self.proximo_desafio += 1
                self.desafio_atual = None
                self.atualizar_desafios_disponiveis()
            elif status == "falhou":
                messagebox.showwarning("Desafio", "Você falhou no desafio.")
                self.desafio_atual = None
                self.atualizar_desafios_disponiveis()

    def avancar_dia(self):
        self.mercado.avancar_dia()
        if self.desafio_atual:
            self.desafio_atual.avancar_dia()
        self.atualizar_tela()

    def comprar_acao(self, nome):
        acao = self.mercado.get_acao_por_nome(nome)
        if self.jogador.comprar_acao(acao, 1):
            self.atualizar_tela()
        else:
            messagebox.showerror("Erro", "Saldo insuficiente!")

    def vender_acao(self, nome):
        acao = self.mercado.get_acao_por_nome(nome)
        if self.jogador.vender_acao(acao, 1):
            self.atualizar_tela()
        else:
            messagebox.showerror("Erro", "Você não possui essa ação.")

    def calcular_lucro_total(self):
        total = 0
        for nome, (qtd, preco_medio) in self.jogador.carteira.items():
            acao = self.mercado.get_acao_por_nome(nome)
            total += (acao.preco_atual - preco_medio) * qtd
        return round(total, 2)
