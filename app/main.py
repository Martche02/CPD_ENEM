import os, csv, json, struct
from binaria import BinariaTree
from bmais import BMaisTree
from patricia import PatriciaTree
from manipulador import (
    gravar_registro, ler_registro, reescrever_registro,
    pad_str, FORMATO_REGISTRO, TAMANHO_REGISTRO
)
from tri import calcular_taxa_acerto, safe_float

# --- Caminhos ---
BASE_ORIGEM = 'origem'
BASE_DADOS  = 'dados'
COMBINADO   = os.path.join(BASE_ORIGEM, 'combinado.json')

ARQ_DAT   = os.path.join(BASE_DADOS, 'questoes.dat')
IDX_IDENT = os.path.join(BASE_DADOS, 'indice_ident.idx')

# --- Limpeza ---
os.makedirs(BASE_DADOS, exist_ok=True)
for f in [ARQ_DAT, IDX_IDENT]:
    if os.path.exists(f):
        os.remove(f)

# --- Índices ---
idx_ident = BinariaTree()
idx_dif   = BMaisTree(ordem=4)
idx_texto = PatriciaTree()
idx_disc  = BinariaTree()
idx_cont  = BinariaTree()
idx_top   = BinariaTree()

# --- 1) Inserção CSVs 2016–2022 ---
for ano in range(2016, 2023):
    pasta = os.path.join(BASE_ORIGEM, str(ano))
    if not os.path.isdir(pasta):
        continue
    for arq in os.listdir(pasta):
        if not arq.endswith('.csv'):
            continue
        with open(os.path.join(pasta, arq), newline='', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            for linha in leitor:
                co_item = linha.get('CO_ITEM')
                if not co_item:
                    continue
                identificador = int(co_item)
                numero = int(linha.get('CO_POSICAO','0') or 0)
                discr = safe_float(linha.get('NU_PARAM_A',''))
                dif   = safe_float(linha.get('NU_PARAM_B',''))
                chute = safe_float(linha.get('NU_PARAM_C',''))
                tac   = calcular_taxa_acerto(discr, dif, chute)

                registro = {
                    'identificador':  identificador,
                    'ano':             ano,
                    'numero':          numero,
                    'prova':           linha.get('SG_AREA',''),
                    'dificuldade':     dif,
                    'taxa_acerto':     tac,
                    'texto_long':      '',
                    'disciplina':      '',
                    'conteudo':        '',
                    'topico':          '',
                    'discriminacao':   discr,
                    'acerto_chute':    chute,
                }
                pos = gravar_registro(ARQ_DAT, registro)
                idx_ident.inserir(identificador, pos)
                idx_dif.inserir(dif, pos)
                idx_texto.inserir('', pos)
                idx_disc.inserir('', pos)
                idx_cont.inserir('', pos)
                idx_top.inserir('', pos)


# persiste índice primário
idx_ident.salvar_em_arquivo(IDX_IDENT)

# --- 2) Atualização combinado.json ---
with open(COMBINADO, 'r', encoding='utf-8') as f:
    itens = json.load(f)

for it in itens:
    cats     = it.get('categorias', [])
    ano_json = it.get('Ano')
    valido = len(cats) > 1 and ano_json == int(cats[1])

    codigo   = it.get('Código Enem')
    try:
        identificador = int(codigo)
    except:
        continue
    pos = idx_ident.buscar(identificador)
    #print(f"[JSON] Buscando ID {identificador}...", end='')
    pos = idx_ident.buscar(identificador)
    if pos is None:
        #print("❌ não encontrado")
        continue
    #print(f"✔️ encontrado na posição {pos}")    

    if not valido:
        txt = disc = cont = top = "Nenhum resultado"
    else:
        partes = (it.get('enunciado') or []) + (it.get('imagens') or []) + (it.get('alternativas') or [])
        txt  = ' '.join(partes)[:2000]
        disc = cats[2] if len(cats)>2 else "Nenhum resultado"
        cont = cats[3] if len(cats)>3 else "Nenhum resultado"
        top  = cats[4] if len(cats)>4 else "Nenhum resultado"

    registro = ler_registro(ARQ_DAT, pos)
    registro['texto_long'] = txt
    registro['disciplina'] = disc
    registro['conteudo']   = cont
    registro['topico']     = top

    reescrever_registro(ARQ_DAT, pos, registro)
    idx_texto.inserir(txt[:20], pos)
    idx_disc.inserir(disc, pos)
    idx_cont.inserir(cont, pos)
    idx_top.inserir(top, pos)
    #print("\n--- Verificando registros diretamente do .dat ---")

print("\n=== TESTES ===")
print("Buscando ID 24455 (int)...")
print("Encontrado:", idx_ident.buscar(24455))

print("Buscando texto prefixo 'Analise a figur'...")
print("Resultados:", idx_texto.buscar_prefixo("Analise a figur"))

print("Buscando disciplina 'Química'...")
print("Resultados:", idx_disc.buscar('Química'))

# --- 3) Testes rápidos ---
print("Total de registros:", os.path.getsize(ARQ_DAT) // TAMANHO_REGISTRO)
print("Exemplo CSV existe?   ", idx_ident.buscar(97446)  is not None)
pos = idx_ident.buscar(97446)
registro = ler_registro(ARQ_DAT, pos)
for chave, valor in registro.items():
    print(f"{chave}: {valor}")
print("Prefixo ex.:          ", idx_texto.buscar_prefixo("A respeito das in")[:3])
print("Disciplina ex.:       ", idx_disc.buscar("Química") is not None)
print("Fim.")
