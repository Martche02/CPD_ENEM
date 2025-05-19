from util.manipulador import ler_registro

ARQ_DAT = 'dados/questoes.dat'

def menu(indices):
    while True:
        print("\n=== CONSULTA ===")
        print("1) Buscar por identificador")
        print("2) Buscar por dificuldade (B+)")
        print("3) Buscar por prefixo de texto (Patricia)")
        print("4) Buscar por disciplina")
        print("5) Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            try:
                ident = int(input("Digite o identificador: "))
                pos = indices['ident'].buscar(ident)
                if pos is not None:
                    r = ler_registro(ARQ_DAT, pos)
                    print("\n--- Questão encontrada ---")
                    for k,v in r.items():
                        print(f"{k}: {v}")
                else:
                    print("❌ Não encontrado.")
            except: print("❌ Entrada inválida")

        elif opcao == '2':
            try:
                val = float(input("Dificuldade desejada: "))
                resultados = indices['dif'].buscar(val)
                for pos in resultados:
                    r = ler_registro(ARQ_DAT, pos)
                    print(f"ID: {r['identificador']} — dificuldade: {r['dificuldade']}")
            except: print("❌ Valor inválido")

        elif opcao == '3':
            prefixo = input("Prefixo do texto: ")[:20]
            resultados = indices['texto'].buscar_prefixo(prefixo)
            for pos in resultados:
                r = ler_registro(ARQ_DAT, pos)
                print(f"ID: {r['identificador']} — texto: {r['texto_long'][:60]}")

        elif opcao == '4':
            chave = input("Disciplina: ")
            pos = indices['disc'].buscar(chave)
            if pos:
                r = ler_registro(ARQ_DAT, pos)
                print(f"ID: {r['identificador']} — disciplina: {r['disciplina']}")
            else:
                print("❌ Nada encontrado")

        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida")
