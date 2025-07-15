# tests_algoritmos.py
from algorithms import busca_sequencial, busca_binaria, rabin_karp

print("== Testes de Algoritmos de Busca ==")

# Busca Sequencial
lista = ['TechWave', 'AgroPlus', 'BankNow', 'HealthMax', 'GreenEnergy']
print("Busca Sequencial - Procurando 'BankNow':")
print("Índice encontrado:", busca_sequencial(lista, 'BankNow'))

# Busca Binária (em lista ordenada)
lista_ordenada = sorted([10, 20, 30, 40, 50])
print("Busca Binária - Procurando 30:")
print("Índice encontrado:", busca_binaria(lista_ordenada, 30))

# Rabin-Karp
texto = "O mercado financeiro está em alta com a TechWave liderando."
padrao = "TechWave"
print("Rabin-Karp - Procurando 'TechWave':")
print("Posição encontrada:", rabin_karp(texto, padrao))
