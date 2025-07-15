# algorithms.py


# Busca Sequencial: percorre a lista do início ao fim procurando o elemento alvo.
# Retorna o índice do elemento se encontrado, ou -1 se não estiver na lista.
def busca_sequencial(lista, alvo):
    for i, item in enumerate(lista):
        if item == alvo:
            return i
    return -1


# Busca Binária: eficiente para listas ordenadas.
# Divide a lista ao meio e descarta metade a cada iteração, até encontrar o alvo ou esgotar as opções.
# Retorna o índice do elemento se encontrado, ou -1 se não estiver na lista.
def busca_binaria(lista, alvo):
    inicio, fim = 0, len(lista) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if lista[meio] == alvo:
            return meio
        elif lista[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1


# Rabin-Karp: algoritmo eficiente para busca de substring em texto.
# Usa hashing para comparar rapidamente o padrão com partes do texto.
# Retorna o índice inicial da substring encontrada, ou -1 se não encontrar.
def rabin_karp(texto, padrao):
    d = 256  # número de caracteres possíveis (ASCII)
    q = 101  # número primo para módulo do hash
    m = len(padrao)
    n = len(texto)
    h = pow(d, m-1) % q  # valor de d^(m-1) % q
    p = 0  # hash do padrão
    t = 0  # hash do texto

    # Calcula o hash do padrão e do primeiro bloco do texto
    for i in range(m):
        p = (d * p + ord(padrao[i])) % q
        t = (d * t + ord(texto[i])) % q

    # Desliza o padrão sobre o texto
    for s in range(n - m + 1):
        if p == t:
            # Se o hash bate, verifica caractere a caractere
            if texto[s:s+m] == padrao:
                return s
        if s < n - m:
            # Atualiza o hash do texto (remove o primeiro caractere e adiciona o próximo)
            t = (d * (t - ord(texto[s]) * h) + ord(texto[s + m])) % q
            t = (t + q) % q  # garante valor positivo
    return -1



# Função genérica para buscar usando o algoritmo escolhido.
# Permite escolher entre busca sequencial, binária ou Rabin-Karp.
# - Para listas: use 'sequencial' ou 'binaria'.
# - Para texto: use 'rabin_karp'.
# Retorna o índice do elemento/padrão encontrado, ou -1 se não encontrar.
def buscar(algoritmo, dados, alvo):
    """
    algoritmo: str - 'sequencial', 'binaria' ou 'rabin_karp'
    dados: lista (para sequencial/binaria) ou texto (para rabin_karp)
    alvo: valor a ser buscado (ou padrão para rabin_karp)
    """
    if algoritmo == 'sequencial':
        return busca_sequencial(dados, alvo)
    elif algoritmo == 'binaria':
        return busca_binaria(dados, alvo)
    elif algoritmo == 'rabin_karp':
        return rabin_karp(dados, alvo)
    else:
        raise ValueError("Algoritmo de busca desconhecido.")


# Exemplos de uso das funções de busca
if __name__ == "__main__":
    print("== Exemplos de Algoritmos de Busca ==")

    # Busca Sequencial
    lista = ['TechWave', 'AgroPlus', 'BankNow', 'HealthMax', 'GreenEnergy']
    print("Busca Sequencial - Procurando 'BankNow':")
    print("Índice encontrado:", buscar('sequencial', lista, 'BankNow'))

    # Busca Binária (em lista ordenada)
    lista_ordenada = sorted([10, 20, 30, 40, 50])
    print("Busca Binária - Procurando 30:")
    print("Índice encontrado:", buscar('binaria', lista_ordenada, 30))

    # Rabin-Karp
    texto = "O mercado financeiro está em alta com a TechWave liderando."
    padrao = "TechWave"
    print("Rabin-Karp - Procurando 'TechWave':")
    print("Posição encontrada:", buscar('rabin_karp', texto, padrao))
