import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from market import Mercado
from player import Jogador
from algorithms import buscar
import random
import heapq
from collections import Counter

# --- ALGORITMO 1: Hash com Extração para ações compradas ---
class HashTableExtracao:
    def __init__(self, size=101):
        self.size = size                    # Tamanho da tabela hash
        self.table = [None] * size          # Array de 101 posições

    def _hash(self, key):
        key_str = str(key)
        # EXTRAÇÃO: pega primeiro + último caractere
        extracao = (ord(key_str[0]) + ord(key_str[-1])) % self.size
        return extracao

    def insert(self, key, value):
        idx = self._hash(key)               # Calcula posição
        # Resolve colisão com linear probing
        while self.table[idx] is not None and self.table[idx][0] != key:
            idx = (idx + 1) % self.size
        self.table[idx] = (key, value)      # Insere (nome, preço)

    def all_items(self):
        return [item for item in self.table if item is not None]  # Retorna tudo

# --- ALGORITMO 2: Linear Probing para ações vendidas ---
class LinearProbingTable:
    def __init__(self, size=20):
        self.size = size                    # Tabela menor
        self.table = [None] * size

    def _hash(self, key):
        return sum(ord(c) for c in key) % self.size  # Soma ASCII de todos chars

    def insert(self, key):
        idx = self._hash(key)               # Posição inicial
        for _ in range(self.size):
            if self.table[idx] is None or self.table[idx] == key:
                self.table[idx] = key       # Insere apenas nome
                return
            idx = (idx + 1) % self.size     # Próxima posição (linear)

    def get_all(self):
        return [k for k in self.table if k is not None]

# --- ALGORITMO 3: Huffman para compressão ---
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char                    # Caractere
        self.freq = freq                    # Frequência
        self.left = None                    # Filho esquerdo
        self.right = None                   # Filho direito

    def __lt__(self, other):
        return self.freq < other.freq       # Para ordenação no heap

def build_huffman_tree(text):
    freq = Counter(text)                    # Conta frequência dos chars
    heap = [HuffmanNode(ch, fr) for ch, fr in freq.items()]  # Cria nós
    heapq.heapify(heap)                     # Min-heap
    
    while len(heap) > 1:                    # Constrói árvore
        n1 = heapq.heappop(heap)            # Menor frequência
        n2 = heapq.heappop(heap)            # Segunda menor
        merged = HuffmanNode(None, n1.freq + n2.freq)  # Nó pai
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)        # De volta ao heap
    
    return heap[0] if heap else None

def build_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node:
        if node.char is not None:           # Folha da árvore
            codebook[node.char] = prefix    # Associa char ao código
        build_codes(node.left, prefix + "0", codebook)   # Esquerda = 0
        build_codes(node.right, prefix + "1", codebook)  # Direita = 1
    return codebook

def huffman_compress(text):
    tree = build_huffman_tree(text)         # Constrói árvore
    codebook = build_codes(tree)            # Gera códigos binários
    compressed = ''.join(codebook[ch] for ch in text)  # Comprime
    return compressed, codebook

# --- CONFIGURAÇÃO DOS DESAFIOS ---
DESAFIOS = [
    ("Lucre $50 em 10 dias", 50, 10),      # (descrição, meta, prazo)
    ("Lucre $100 em 8 dias", 100, 8),
    ("Lucre $200 em 7 dias", 200, 7),
    ("Sobreviva 7 dias com saldo positivo", 0, 7),
    ("Multiplique o saldo por 1.2 em 10 dias", 200, 10)
]

class Desafio:
    def __init__(self, descricao, lucro_necessario, dias_max):
        self.descricao = descricao          # Nome do desafio
        self.lucro_necessario = lucro_necessario  # Meta de lucro
        self.dias_max = dias_max            # Prazo limite
        self.dia_atual = 0                  # Contador de dias
        self.ativo = False                  # Status do desafio

    def iniciar(self):
        self.ativo = True                   # Ativa desafio
        self.dia_atual = 0                  # Reseta contador

    def avancar_dia(self):
        if self.ativo:
            self.dia_atual += 1             # Incrementa dia

    def verificar_conclusao(self, lucro, saldo):
        if not self.ativo:
            return "inativo"
        if "Sobreviva" in self.descricao:   # Desafio especial
            if self.dia_atual >= self.dias_max:
                self.ativo = False
                return "concluido" if saldo > 0 else "falhou"
        else:
            if lucro >= self.lucro_necessario:  # Meta atingida
                self.ativo = False
                return "concluido"
            elif self.dia_atual >= self.dias_max:  # Tempo esgotado
                self.ativo = False
                return "falhou"
        return "em andamento"

# --- CLASSE PRINCIPAL DA APLICAÇÃO ---
class App:
    def __init__(self, root):
        # Configuração da janela
        self.root = root
        self.root.title("Simulador da Bolsa de Valores")
        self.root.geometry("900x650")
        
        # Inicialização dos componentes
        self.mercado = Mercado()            # Sistema de ações
        self.jogador = Jogador("Investidor")  # Jogador com $1000
        self.desafio_atual = None           # Desafio ativo
        self.proximo_desafio = 0            # Índice do próximo desafio

        # Estruturas de dados dos algoritmos
        self.recentes_vendidas = LinearProbingTable()    # Linear probing
        self.recentes_compradas = HashTableExtracao()    # Hash extração

        # Filtro em tempo real (Rabin-Karp)
        self.busca_var_substring = tk.StringVar()
        self.busca_var_substring.trace_add('write', lambda *args: self.atualizar_tela())

        # Criação das abas
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill='both', expand=True)
        
        self.tab_mercado = ttk.Frame(self.tabs)
        self.tab_carteira = ttk.Frame(self.tabs)
        self.tab_desafios = ttk.Frame(self.tabs)
        self.tab_historico = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_mercado, text='📈 Mercado')
        self.tabs.add(self.tab_carteira, text='💼 Carteira')
        self.tabs.add(self.tab_desafios, text='🎯 Desafios')
        self.tabs.add(self.tab_historico, text='📜 Histórico')

        # Barra de status
        self.status_bar = tk.Label(root, text="Dia: 0 | Saldo: $1000.00", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Configuração de cada aba
        self.setup_mercado()
        self.setup_carteira()
        self.setup_desafios()
        self.setup_historico()
        self.atualizar_tela()

    def setup_mercado(self):
        # Label do desafio ativo
        self.label_desafio_mercado = ttk.Label(self.tab_mercado, text="", foreground="blue")
        self.label_desafio_mercado.pack(pady=5)

        # Botões dos algoritmos
        ttk.Button(self.tab_mercado, text="Ver Ações Recentemente Vendidas", command=self.mostrar_recentes_vendidas).pack(pady=2)
        ttk.Button(self.tab_mercado, text="Ver Ações Recentemente Compradas", command=self.mostrar_recentes_compradas).pack(pady=2)
        ttk.Button(self.tab_mercado, text="Buscar Ação no Histórico (Sequencial)", command=self.buscar_acao_historico_sequencial).pack(pady=2)
        ttk.Button(self.tab_mercado, text="Buscar Mercado (Binária)", command=self.buscar_mercado_binaria).pack(pady=2)

        # Container com scroll para muitas ações
        frame_acoes_container = ttk.Frame(self.tab_mercado)
        frame_acoes_container.pack(fill='both', expand=True, padx=10, pady=10)
        canvas = tk.Canvas(frame_acoes_container)
        scrollbar = ttk.Scrollbar(frame_acoes_container, orient='vertical', command=canvas.yview)
        self.frame_acoes = ttk.Frame(canvas)
        self.frame_acoes.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.frame_acoes, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        # Botão avançar dia
        self.btn_avancar = ttk.Button(self.tab_mercado, text="⏭️ Avançar 1 Dia", command=self.avancar_dia)
        self.btn_avancar.pack(pady=5)

        # Campo de filtro (usa Rabin-Karp)
        busca_frame_sub = ttk.Frame(self.tab_mercado)
        busca_frame_sub.pack(pady=5)
        ttk.Label(busca_frame_sub, text="Filtrar ações por substring:").pack(side=tk.LEFT)
        ttk.Entry(busca_frame_sub, textvariable=self.busca_var_substring, width=15).pack(side=tk.LEFT, padx=2)

    def setup_carteira(self):
        # Frame principal da carteira
        self.frame_carteira = ttk.Frame(self.tab_carteira)
        self.frame_carteira.pack(fill='both', expand=True, padx=10, pady=10)

        # Filtro da carteira (usa Rabin-Karp)
        busca_frame = ttk.Frame(self.tab_carteira)
        busca_frame.pack(pady=5)
        self.busca_carteira_var = tk.StringVar()
        self.busca_carteira_var.trace_add('write', lambda *args: self.atualizar_tela())
        ttk.Label(busca_frame, text="Filtrar ações na carteira por substring:").pack(side=tk.LEFT)
        ttk.Entry(busca_frame, textvariable=self.busca_carteira_var, width=15).pack(side=tk.LEFT, padx=2)

    def setup_desafios(self):
        # Frame dos desafios
        self.frame_desafios = ttk.Frame(self.tab_desafios)
        self.frame_desafios.pack(fill='both', expand=True, padx=10, pady=10)
        self.label_desafios = ttk.Label(self.frame_desafios, text="Desafios disponíveis:")
        self.label_desafios.pack(pady=5)
        self.lista_desafios = ttk.Frame(self.frame_desafios)
        self.lista_desafios.pack()
        self.atualizar_desafios_disponiveis()

    def setup_historico(self):
        # Frame do histórico
        self.frame_historico = ttk.Frame(self.tab_historico)
        self.frame_historico.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Área de texto do histórico
        self.historico_text = tk.Text(self.frame_historico, height=20, state='disabled')
        self.historico_text.pack(fill='both', expand=True)
        
        # Label do lucro total
        self.label_lucro_total = ttk.Label(self.frame_historico, text="")
        self.label_lucro_total.pack(pady=5)
        
        # Botão da compressão Huffman
        ttk.Button(self.frame_historico, text="Ver Compressão Huffman", command=self.mostrar_historico_comprimido).pack(pady=2)

    # --- FUNÇÕES DOS ALGORITMOS ---

    def mostrar_recentes_vendidas(self):
        # ALGORITMO: Linear Probing - mostra ações vendidas
        vendidas = self.recentes_vendidas.get_all()
        messagebox.showinfo("Ações Recentemente Vendidas", "\n".join(vendidas) if vendidas else "Nenhuma ação vendida recentemente.")

    def mostrar_recentes_compradas(self):
        # ALGORITMO: Hash Extração - mostra ações compradas
        compradas = self.recentes_compradas.all_items()
        if compradas:
            lista = "\n".join([f"{nome}: ${preco:.2f}" for nome, preco in compradas])
            messagebox.showinfo("Ações Recentemente Compradas", lista)
        else:
            messagebox.showinfo("Ações Recentemente Compradas", "Nenhuma ação comprada recentemente.")

    def buscar_acao_historico_sequencial(self):
        # ALGORITMO: Busca Sequencial - percorre histórico
        nome = simpledialog.askstring("Busca Sequencial", "Nome da ação para buscar no histórico:")
        if not nome:
            return
        for linha in self.jogador.historico:
            if nome.lower() in linha.lower():
                messagebox.showinfo("Busca Sequencial", f"Ação encontrada no histórico:\n{linha}")
                return
        messagebox.showwarning("Busca Sequencial", "Ação não encontrada no histórico.")

    def mostrar_historico_comprimido(self):
        # ALGORITMO: Huffman - comprime histórico
        historico_str = '\n'.join(self.jogador.historico)
        if not historico_str:
            messagebox.showinfo("Huffman", "Histórico vazio.")
            return
        compressed, codebook = huffman_compress(historico_str)
        tamanho_original = len(historico_str.encode('utf-8'))
        tamanho_comprimido = len(compressed) // 8 + 1
        messagebox.showinfo("Huffman", f"Tamanho original: {tamanho_original} bytes\nTamanho comprimido: {tamanho_comprimido} bytes")

    def buscar_mercado_binaria(self):
        # ALGORITMO: Busca Binária - busca no mercado ordenado
        nome = simpledialog.askstring("Busca Binária", "Nome da ação no mercado:")
        if not nome:
            return
        acoes = sorted(self.mercado.listar_acoes(), key=lambda x: x[0])  # Ordena primeiro
        nomes = [n for n, _ in acoes]
        idx = buscar('binaria', nomes, nome)  # Busca binária do algorithms.py
        if idx != -1:
            messagebox.showinfo("Busca Binária", f"Ação encontrada: {acoes[idx][0]} - ${acoes[idx][1]:.2f}")
        else:
            messagebox.showwarning("Busca Binária", "Ação não encontrada.")

    def atualizar_historico(self):
        # Atualiza texto do histórico e calcula lucro
        self.historico_text.config(state='normal')
        self.historico_text.delete(1.0, tk.END)
        for linha in self.jogador.historico:
            self.historico_text.insert(tk.END, linha + "\n")
        self.historico_text.config(state='disabled')
        
        lucro = self.jogador.saldo + self.calcular_lucro_total() - 1000.0
        cor = "green" if lucro >= 0 else "red"
        self.label_lucro_total.config(text=f"Lucro/Prejuízo Total: ${lucro:.2f}", foreground=cor)

    def atualizar_desafios_disponiveis(self):
        # Mostra próximo desafio disponível
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
        # Inicia o próximo desafio
        desc, lucro, dias = DESAFIOS[self.proximo_desafio]
        self.desafio_atual = Desafio(desc, lucro, dias)
        self.desafio_atual.iniciar()
        self.tabs.select(self.tab_mercado)
        messagebox.showinfo("Desafio Iniciado", f"{desc}")
        self.atualizar_tela()

    def atualizar_tela(self):
        # FUNÇÃO PRINCIPAL - atualiza toda a interface
        # Mostra desafio ativo
        self.label_desafio_mercado.config(text=f"Desafio: {self.desafio_atual.descricao}" if self.desafio_atual and self.desafio_atual.ativo else "")

        # Atualiza lista de ações no mercado
        for widget in self.frame_acoes.winfo_children():
            widget.destroy()
        filtro = self.busca_var_substring.get()
        acoes = self.mercado.listar_acoes()
        
        # ALGORITMO: Rabin-Karp - filtra ações por substring
        if filtro:
            acoes = [(nome, preco) for nome, preco in acoes if buscar('rabin_karp', nome, filtro) != -1]
        
        # Cria widgets para cada ação
        for nome, preco in acoes:
            qtd = self.jogador.carteira.get(nome, (0,))[0]
            frame = ttk.Frame(self.frame_acoes, relief=tk.RIDGE, padding=10)
            frame.pack(fill='x', pady=5)
            lbl = ttk.Label(frame, text=f"{nome} - ${preco:.2f}  |  Qtde: {qtd}")
            lbl.pack(side=tk.LEFT)
            ttk.Button(frame, text="Comprar", command=lambda n=nome: self.comprar_acao(n)).pack(side=tk.LEFT, padx=5)
            ttk.Button(frame, text="Vender", command=lambda n=nome: self.vender_acao(n)).pack(side=tk.LEFT)

        # Atualiza carteira
        for widget in self.frame_carteira.winfo_children():
            widget.destroy()
        filtro_carteira = self.busca_carteira_var.get()
        carteira_itens = list(self.jogador.carteira.items())
        
        # ALGORITMO: Rabin-Karp - filtra carteira
        if filtro_carteira:
            carteira_itens = [(nome, v) for nome, v in carteira_itens if buscar('rabin_karp', nome, filtro_carteira) != -1]
        
        # Mostra cada ação da carteira com lucro/prejuízo
        for nome, (qtd, preco_medio) in carteira_itens:
            acao = self.mercado.get_acao_por_nome(nome)
            lucro = round((acao.preco_atual - preco_medio) * qtd, 2)
            cor = "green" if lucro >= 0 else "red"
            txt = f"{nome}: {qtd} ações | Preço Médio: ${preco_medio:.2f} | Atual: ${acao.preco_atual:.2f} | Lucro: ${lucro:.2f}"
            lbl = tk.Label(self.frame_carteira, text=txt, fg=cor)
            lbl.pack(anchor='w', pady=2)

        # Atualiza status bar
        lucro_total = self.calcular_lucro_total()
        self.status_bar.config(text=f"Dia: {self.mercado.dia} | Saldo: ${self.jogador.saldo:.2f} | Lucro Total: ${lucro_total:.2f}")

        self.atualizar_historico()

        # Verifica status do desafio
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
        # Avança um dia no simulador
        self.gerar_noticia_mercado()        # 30% chance de notícia
        self.mercado.avancar_dia()          # Atualiza preços
        if self.desafio_atual:
            self.desafio_atual.avancar_dia()  # Incrementa contador
        self.atualizar_tela()

    def gerar_noticia_mercado(self):
        # Gera notícia aleatória que afeta preço de ação
        if random.random() < 0.3:           # 30% de chance
            acoes = self.mercado.listar_acoes()
            if not acoes:
                return
            nome, _ = random.choice(acoes)   # Escolhe ação aleatória
            impacto = random.choice([-1, 1]) * random.uniform(0.05, 0.2)  # ±5% a ±20%
            acao = self.mercado.get_acao_por_nome(nome)
            acao.preco_atual *= (1 + impacto)
            acao.preco_atual = max(1, round(acao.preco_atual, 2))
            noticia = f"Notícia: {'Boa' if impacto > 0 else 'Ruim'} para {nome}! Preço alterado para ${acao.preco_atual:.2f}"
            self.jogador.historico.append(noticia)

    def calcular_lucro_total(self):
        # Calcula lucro/prejuízo total da carteira
        total = 0
        for nome, (qtd, preco_medio) in self.jogador.carteira.items():
            acao = self.mercado.get_acao_por_nome(nome)
            total += (acao.preco_atual - preco_medio) * qtd
        return total

    def comprar_acao(self, nome):
        # Compra 1 ação - usa Hash Extração para registrar
        acao_obj = self.mercado.get_acao_por_nome(nome)
        if not acao_obj:
            messagebox.showerror("Erro", "Ação não encontrada.")
            return
        if self.jogador.comprar_acao(acao_obj, 1):
            # ALGORITMO: Hash Extração - registra compra
            self.recentes_compradas.insert(nome, acao_obj.preco_atual)
            self.atualizar_tela()
        else:
            messagebox.showerror("Erro", "Saldo insuficiente para comprar.")

    def vender_acao(self, nome):
        # Vende 1 ação - usa Linear Probing para registrar
        acao_obj = self.mercado.get_acao_por_nome(nome)
        if not acao_obj:
            messagebox.showerror("Erro", "Ação não encontrada.")
            return
        if self.jogador.vender_acao(acao_obj, 1):
            # ALGORITMO: Linear Probing - registra venda
            self.recentes_vendidas.insert(nome)
            self.atualizar_tela()
        else:
            messagebox.showerror("Erro", "Você não possui essa ação ou quantidade insuficiente.")

# Inicialização da aplicação
if __name__ == "__main__":
    root = tk.Tk()                          # Cria janela principal
    app = App(root)                         # Instancia aplicação
    root.mainloop()                         # Inicia loop de eventos