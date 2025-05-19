import csv, json
from util.manipulador import gravar_registro, ler_registro, reescrever_registro
from util.tri import calcular_taxa_acerto, safe_float

ARQ_DAT = 'dados/questoes.dat'
COMBINADO = 'origem/combinado.json'

def adicionar_csv_manual(path_csv, ano, indices):
    with open(path_csv, newline='', encoding='utf-8') as f:
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


def reaplicar_json(indices):
    with open(COMBINADO, 'r', encoding='utf-8') as f:
        itens = json.load(f)

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
