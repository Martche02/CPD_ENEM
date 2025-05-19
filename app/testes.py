from manipulador import ler_registro
ARQ_DAT = 'dados/questoes.dat'

def verificar_exemplo_por_id(indices, ident=24455):
    print(f"\n🔎 Verificando ID={ident}...")
    pos = indices['ident'].buscar(ident)
    if pos is None:
        print("❌ ID não encontrado")
        return
    r = ler_registro(ARQ_DAT, pos)
    for k, v in r.items():
        print(f"{k}: {v}")

def testar_prefixo(indices, prefixo="Analise a figur"):
    print(f"\n🔎 Buscando prefixo: '{prefixo}'")
    result = indices['texto'].buscar_prefixo(prefixo)
    for pos in result[:3]:
        r = ler_registro(ARQ_DAT, pos)
        print(f"ID: {r['identificador']} | Texto: {r['texto_long'][:50]}")

def testar_disciplina(indices, disc="Química"):
    print(f"\n🔎 Testando disciplina: {disc}")
    pos = indices['disc'].buscar(disc)
    if pos:
        r = ler_registro(ARQ_DAT, pos)
        print(f"✔️ ID: {r['identificador']} | Disciplina: {r['disciplina']}")
    else:
        print("❌ Não encontrada")
