import os
import csv
from binaria import BinariaTree
from bmais import BMaisTree
from patricia import PatriciaTree
from manipulador import gravar_registro, ler_registro
from tri import calcular_taxa_acerto, safe_float

CAMINHO_DADOS = 'dados/questoes.dat'
CAMINHO_INDICE_IDENT = 'dados/indice_ident.idx'
CAMINHO_CSV = 'origem/2022/1055.csv'

# Limpa arquivos anteriores
os.makedirs("dados", exist_ok=True)
for caminho in [CAMINHO_DADOS, CAMINHO_INDICE_IDENT]:
    if os.path.exists(caminho):
        os.remove(caminho)

# Inicializa índices
indice_ident = BinariaTree()
indice_dif = BMaisTree(ordem=4)
indice_texto = PatriciaTree()

# Leitura do CSV
with open(CAMINHO_CSV, newline='', encoding='utf-8') as f:
    leitor = csv.DictReader(f)
    for linha in leitor:
        try:
            numero = int(linha['CO_POSICAO'])
            identificador = f"2022{numero}"
            discriminacao = safe_float(linha['NU_PARAM_A'])
            dificuldade = safe_float(linha['NU_PARAM_B'])
            acerto_chute = safe_float(linha['NU_PARAM_C'])
            taxa_acerto = calcular_taxa_acerto(discriminacao, dificuldade, acerto_chute)
            
            registro = {
                'identificador': identificador,
                'ano': 2022,
                'numero': numero,
                'prova': linha['SG_AREA'],
                'dificuldade': dificuldade,
                'taxa_acerto': taxa_acerto,
                'texto': '',
                'discriminacao': discriminacao,
                'acerto_chute': acerto_chute,
            }


            pos = gravar_registro(CAMINHO_DADOS, registro)
            indice_ident.inserir(identificador, pos)
            indice_dif.inserir(registro['dificuldade'], pos)
            # índice_texto ainda não, pois o texto está vazio

        except Exception as e:
            print(f"❌ Erro ao processar linha: {linha}")
            print(f"Motivo: {e}")

# Salva o índice de identificadores
indice_ident.salvar_em_arquivo(CAMINHO_INDICE_IDENT)
print("✅ Importação concluída.")

# Teste: busca por identificador específico
teste_id = '202250'
print(f"\n🔍 Teste: buscar identificador '{teste_id}':")
pos = indice_ident.buscar(teste_id)
if pos is not None:
    r = ler_registro(CAMINHO_DADOS, pos)
    print(f"✔️ Encontrado: {r}")
else:
    print("❌ Não encontrado.")
