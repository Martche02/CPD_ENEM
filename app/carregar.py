import os, csv, json
from binaria import BinariaTree
from bmais import BMaisTree
from patricia import PatriciaTree
from manipulador import gravar_registro, ler_registro, reescrever_registro
from tri import calcular_taxa_acerto, safe_float

BASE_ORIGEM = 'origem'
BASE_DADOS  = 'dados'
COMBINADO   = os.path.join(BASE_ORIGEM, 'combinado.json')
ARQ_DAT     = os.path.join(BASE_DADOS, 'questoes.dat')

# Caminhos individuais para cada índice
CAMINHOS_INDICES = {
    'ident': os.path.join(BASE_DADOS, 'indice_ident.idx'),
    'dif':   os.path.join(BASE_DADOS, 'indice_dif.idx'),
    'texto': os.path.join(BASE_DADOS, 'indice_texto.idx'),
    'disc':  os.path.join(BASE_DADOS, 'indice_disc.idx'),
    'cont':  os.path.join(BASE_DADOS, 'indice_cont.idx'),
    'top':   os.path.join(BASE_DADOS, 'indice_top.idx')
}

# Mapeia o tipo de cada índice
CLASSES_INDICES = {
    'ident': BinariaTree,
    'dif':   BMaisTree,          # ← sem lambda
    'texto': PatriciaTree,
    'disc':  BinariaTree,
    'cont':  BinariaTree,
    'top':   BinariaTree
}



def limpar_bases():
    os.makedirs(BASE_DADOS, exist_ok=True)
    for f in list(CAMINHOS_INDICES.values()) + [ARQ_DAT]:
        if os.path.exists(f):
            os.remove(f)

def criar_indices_vazios():
    return {
        'ident': BinariaTree(),
        'dif':   BMaisTree(ordem=4),     # ← ordem manual
        'texto': PatriciaTree(),
        'disc':  BinariaTree(),
        'cont':  BinariaTree(),
        'top':   BinariaTree()
    }

def salvar_indices(indices):
    for chave, caminho in CAMINHOS_INDICES.items():
        indices[chave].salvar_em_arquivo(caminho)

def carregar_indices():
    indices = {}
    for chave, caminho in CAMINHOS_INDICES.items():
        if not os.path.exists(caminho):
            return criar_indices_vazios()
        if chave == 'dif':
            indices[chave] = BMaisTree.carregar_de_arquivo(caminho)
        else:
            indices[chave] = CLASSES_INDICES[chave].carregar_de_arquivo(caminho)
    return indices

def inserir_csvs(indices):
    total = 0
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
                    indices['ident'].inserir(identificador, pos)
                    indices['dif'].inserir(dif, pos)
                    indices['texto'].inserir('', pos)
                    indices['disc'].inserir('', pos)
                    indices['cont'].inserir('', pos)
                    indices['top'].inserir('', pos)
                    total += 1
    return total

def atualizar_combinado(indices):
    with open(COMBINADO, 'r', encoding='utf-8') as f:
        itens = json.load(f)

    atualizados = 0
    for it in itens:
        cats     = it.get('categorias', [])
        ano_json = it.get('Ano')
        try:
            valido = len(cats) > 1 and ano_json == int(cats[1])
        except:
            valido = False

        try:
            identificador = int(it.get('Código Enem'))
        except:
            continue

        pos = indices['ident'].buscar(identificador)
        if pos is None:
            continue

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
        indices['texto'].inserir(txt[:20], pos)
        indices['disc'].inserir(disc, pos)
        indices['cont'].inserir(cont, pos)
        indices['top'].inserir(top, pos)
        atualizados += 1

    return atualizados
