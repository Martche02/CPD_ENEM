import os
from binaria import BinariaTree
from bmais import BMaisTree
from patricia import PatriciaTree
from manipulador import gravar_registro, ler_registro

CAMINHO_DADOS = 'dados/questoes.dat'
CAMINHO_INDICE_IDENT = 'dados/indice_ident.idx'

# Limpa arquivos anteriores para garantir teste limpo
for caminho in [CAMINHO_DADOS, CAMINHO_INDICE_IDENT]:
    if os.path.exists(caminho):
        os.remove(caminho)

# Registros de teste
registros = [
    {'identificador': '2023123', 'ano': 2023, 'numero': 123, 'prova': 'Ciencias',
     'dificuldade': 0.92, 'taxa_acerto': 0.94,
     'texto': 'Texto da questão 1 sobre gases ideais e pressão.'},

    {'identificador': '2023124', 'ano': 2023, 'numero': 124, 'prova': 'Ciencias',
     'dificuldade': 0.45, 'taxa_acerto': 0.60,
     'texto': 'Texto da questão 2 sobre leis de Newton.'},

    {'identificador': '2023125', 'ano': 2023, 'numero': 125, 'prova': 'Ciencias',
     'dificuldade': 0.91, 'taxa_acerto': 0.20,
     'texto': 'Patri Texto da questão 3 sobre química orgânica.'},

    {'identificador': '2022130', 'ano': 2022, 'numero': 130, 'prova': 'Ciencias',
     'dificuldade': 0.55, 'taxa_acerto': 0.50,
     'texto': 'Pati Texto da questão 4 sobre circuitos elétricos.'},

    {'identificador': '2022120', 'ano': 2022, 'numero': 120, 'prova': 'Ciencias',
     'dificuldade': 0.33, 'taxa_acerto': 0.80,
     'texto': 'Patigua Texto da questão 5 sobre fotossíntese.'},

    {'identificador': '2021110', 'ano': 2021, 'numero': 110, 'prova': 'Ciencias',
     'dificuldade': 0.60, 'taxa_acerto': 0.45,
     'texto': 'Texto da questão 6 sobre óptica e lentes.'},
]

# Inicializa índices
indice_ident = BinariaTree()
indice_dif = BMaisTree(ordem=4)
indice_texto = PatriciaTree()

# Indexação
for reg in registros:
    pos = gravar_registro(CAMINHO_DADOS, reg)
    indice_ident.inserir(reg['identificador'], pos)
    indice_dif.inserir(reg['dificuldade'], pos)
    indice_texto.inserir(reg['texto'], pos)

# Persistência do índice identificador
indice_ident.salvar_em_arquivo(CAMINHO_INDICE_IDENT)

# Consulta por identificador
print("\n🔍 Buscar por identificador '2023124':")
pos = indice_ident.buscar('2023124')
if pos is not None:
    r = ler_registro(CAMINHO_DADOS, pos)
    print(f"Encontrei: {r['identificador']} | Dificuldade: {r['dificuldade']} | Texto: {r['texto'][:40]}...")
else:
    print("Não encontrado.")

# Consulta por prefixo de texto (Patricia)
print("\n🔍 Buscar por texto 'Pati':")
poses = indice_texto.buscar_prefixo('Pati')
print(poses)
for pos in poses:
    r = ler_registro(CAMINHO_DADOS, pos)
    print(f"Encontrei: {r['identificador']} | Dificuldade: {r['dificuldade']} | Texto: {r['texto'][:40]}...")

# Consulta ordenada por dificuldade (B+ Tree)
print("\n📊 Questões por ordem crescente de dificuldade:")
def mostrar(pos):
    r = ler_registro(CAMINHO_DADOS, pos)
    print(f"{r['identificador']} | Dificuldade: {r['dificuldade']:.2f} | Texto: {r['texto'][:30]}...")

indice_dif.percorrer_em_ordem(mostrar)
