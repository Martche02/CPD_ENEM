import os, json
from binaria import BinariaTree
from bmais import BMaisTree
from patricia import PatriciaTree
from manipulador import gravar_registro, ler_registro

# caminhos
CAM_DADOS       = 'dados/questoes.dat'
CAM_IND_IDENT   = 'dados/indice_ident.idx'
CAM_IND_DIF     = 'dados/indice_dif.idx'
CAM_IND_TEXTO   = 'dados/indice_texto.idx'
CAM_IND_DISC    = 'dados/indice_disc.idx'
COMBINADO_JSON  = 'origem/combinado.json'

# limpa
os.makedirs('dados', exist_ok=True)
for f in [CAM_DADOS, CAM_IND_IDENT]:
    if os.path.exists(f): os.remove(f)

# índices
idx_ident = BinariaTree()
idx_dif   = BMaisTree(ordem=4)
idx_texto = PatriciaTree()
idx_disc  = BinariaTree()   # disciplina
idx_cont  = BinariaTree()   # conteúdo
idx_top   = BinariaTree()   # tópico

# carrega JSON
with open(COMBINADO_JSON, 'r', encoding='utf-8') as f:
    itens = json.load(f)

for it in itens:
    ano  = it['Ano']
    num  = it['Questão']
    ident= f"{ano}{num}"
    cats = it.get('categorias', [])
    # monta texto completo
    texto_full = ' '.join(it.get('enunciado', []))
    # imagens e alternativas, se quiser
    texto_full += ' ' + ' '.join(it.get('imagens', []))
    texto_full += ' ' + ' | '.join(it.get('alternativas', []))

    enunciados = it.get('enunciado') or []
    imgs        = it.get('imagens')   or []
    alts        = it.get('alternativas') or []
    # pega disciplina/conteúdo/tópico com fallback
    disciplina = cats[2] if len(cats) > 2 else ''
    conteudo   = cats[3] if len(cats) > 3 else ''
    topico     = cats[4] if len(cats) > 4 else ''

    registro = {
        'identificador': ident,
        'ano': ano,
        'numero': num,
        'prova': it.get('Prova',''),
        # ainda zero
        'dificuldade':  0.0,
        'taxa_acerto':  0.0,
        'texto_long':   texto_full[:2000],
        'discriminacao': 0.0,
        'acerto_chute': 0.0,
        'disciplina':   disciplina,
        'conteudo':     conteudo,
        'topico':       topico,
    }

    pos = gravar_registro(CAM_DADOS, registro)

    # atualiza índices
    idx_ident.inserir(ident, pos)
    idx_dif.inserir(0.0, pos)  # placeholder
    idx_texto.inserir(texto_full[:20], pos)
    idx_disc.inserir(disciplina, pos)
    idx_cont.inserir(conteudo, pos)
    idx_top.inserir(topico, pos)

# salva identificado r e opcionalmente outros
idx_ident.salvar_em_arquivo(CAM_IND_IDENT)
print("✅ JSON importado, índices por identific, texto (20c), disciplina, conteúdo e tópico prontos.")
# ——— Início dos testes de sanity check ———

print("\n==== Iniciando testes automáticos ====")
erros = []

# 1) Lookup de IDs válidos (primeiros 5 itens)
for it in itens[:5]:
    test_id = f"{it['Ano']}{it['Questão']}"
    pos = idx_ident.buscar(test_id)
    if pos is None:
        erros.append(f"[FAIL] ID não encontrado: {test_id}")

# 2) Lookup de ID inválido
if idx_ident.buscar("999999") is not None:
    erros.append("[FAIL] ID inválido retornou posição")

# 3) Patricia: prefixo existente
prefixo = "Analise a figura"  # do enunciado do primeiro item
res = idx_texto.buscar_prefixo(prefixo)
if not res:
    erros.append(f"[FAIL] Patricia não retornou nada para prefixo '{prefixo}'")

# 4) Patricia: prefixo inexistente
if idx_texto.buscar_prefixo("XYZInexistente"):
    erros.append("[FAIL] Patricia retornou algo para prefixo inexistente")

# 5) Discipline index (primeira 5 disciplinas)
for it in itens[:5]:
    disc = it['categorias'][2]
    if idx_disc.buscar(disc) is None:
        erros.append(f"[FAIL] Disciplina não indexada: {disc}")

# 6) Content index (item #3)
conteudo = itens[2]['categorias'][3]
if idx_cont.buscar(conteudo) is None:
    erros.append(f"[FAIL] Conteúdo não indexado: {conteudo}")

# 7) Topic index (item #1)
topico = itens[0]['categorias'][4]
if idx_top.buscar(topico) is None:
    erros.append(f"[FAIL] Tópico não indexado: {topico}")

# 8) Round-trip de leitura
test_id = f"{itens[0]['Ano']}{itens[0]['Questão']}"
pos0 = idx_ident.buscar(test_id)
rec = ler_registro(CAM_DADOS, pos0)
if rec['identificador'] != test_id:
    erros.append(f"[FAIL] Round-trip falhou para {test_id}")

# 9) Busca de categoria vazia (fallback)
# Deve retornar None ou posição para itens sem categoria
if idx_disc.buscar("") is False:
    erros.append("[FAIL] Busca de disciplina vazia não retornou None ou válida")

# 10) Prefixo curto que deve abranger vários:
short = itens[1]['enunciado'][0][:10]
res_multi = idx_texto.buscar_prefixo(short)
if not isinstance(res_multi, list) or len(res_multi) < 1:
    erros.append(f"[FAIL] Prefixo curto '{short}' não retornou lista válida")

# Relatório
if not erros:
    print("🎉 Todos os testes passaram com sucesso!")
else:
    print("⚠️ Alguns testes falharam:")
    for e in erros:
        print("   ", e)

print("==== Fim dos testes ====")
# ——— Fim dos testes ———
# ——— Testes de verificação visual ———

print("\n==== Verificações manuais ====")

# 1) Mostrar 3 registros lidos vs. o JSON original
print("\n1) Round‑trip de 3 registros (identificador, texto e disciplina):")
for it in itens[:3]:
    test_id = f"{it['Ano']}{it['Questão']}"
    pos = idx_ident.buscar(test_id)
    rec = ler_registro(CAM_DADOS, pos)
    esperado_texto = ' '.join(it.get('enunciado', []))[:20]
    esperado_disc = it.get('categorias', ['','', ''])[2] if len(it.get('categorias', []))>2 else ''
    print(f"  ID:   real={rec['identificador']}  | esperado={test_id}")
    print(f"  TEX:  real={rec['texto_long']!r} | esperado={esperado_texto!r}")
    print(f"  DISC: real={rec['disciplina']!r} | esperado={esperado_disc!r}")
    print("  ---")

# 2) Patricia: prefixo e primeiras 3 buscas
prefixo = itens[0]['enunciado'][0][:15]
print(f"\n2) Patricia busca prefixo {prefixo!r}:")
res = idx_texto.buscar_prefixo(prefixo)
print("  Resultados (até 3 posições):", res[:3])
print("  Textos correspondentes:")
for p in res[:3]:
    print("   -", ler_registro(CAM_DADOS, p)['texto_long'][:30], "…")

# 3) Índice de disciplina: listar todas as disciplinas únicas e um exemplo
disciplinas = sorted({ it.get('categorias',[])[2] for it in itens if len(it.get('categorias',[]))>2 })
print("\n3) Disciplinas indexadas e um ID de exemplo:")
for disc in disciplinas:
    pos = idx_disc.buscar(disc)
    exemplo = ler_registro(CAM_DADOS, pos)['identificador'] if pos else None
    print(f"  {disc!r}: exemplo ID={exemplo}")

print("==== Fim das verificações manuais ====")
