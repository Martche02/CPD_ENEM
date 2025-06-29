from util.manipulador import ler_registro
import msvcrt

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
                    pos = pos[0]
                    r = ler_registro(ARQ_DAT, pos)
                    print("\n--- Questão encontrada ---")
                    for k,v in r.items():
                        print(f"{k}: {v}")
                else:
                    print("❌ Não encontrado.")
            except: print("❌ Entrada inválida")

        elif opcao == '2':
            try:
                val_min = float(input("Dificuldade [0,1]: "))
                val_max = val_min + 0.05
                val_min = val_min - 0.05
                if val_min < 0:
                    val_min = 0
                if val_max > 1:
                    val_max = 1
                resultados = indices['dif'].buscar_intervalo(val_min, val_max)
                total_resultados = len(resultados)
                tamanho_pagina = 10
                total_paginas = (total_resultados + tamanho_pagina - 1) // tamanho_pagina

                if total_resultados == 0:
                    print("Nenhum resultado encontrado.")
                else:
                    print(f"\n {total_resultados} resultado(s) encontrado(s). Use ← e → para navegar, 'q' para sair.")

                    pagina_atual = 0
                    while True:
                        # Limpa a tela (opcional)
                        print(f"\n Página {pagina_atual + 1} de {total_paginas}")
                        inicio = pagina_atual * tamanho_pagina
                        fim = inicio + tamanho_pagina
                        pagina = resultados[inicio:fim]

                        for pos in pagina:
                            r = ler_registro(ARQ_DAT, pos)
                            print(f"ID: {r['identificador']} — dificuldade: {r['dificuldade']}")

                        print("\n  ← : Esquerda / → : Direita / q para sair")

                        key = msvcrt.getch()
                        if key == b'\xe0':  #setas
                            key = msvcrt.getch()
                            if key == b'M':  #seta direita
                                if pagina_atual + 1 < total_paginas:
                                    pagina_atual += 1
                                else:
                                    print("Última página.")
                            elif key == b'K':  #seta esquerda
                                if pagina_atual > 0:
                                    pagina_atual -= 1
                                else:
                                    print("Primeira página.")
                        elif key == b'q':
                            print("Saindo...")
                            break
            except:
                print("❌ Entrada inválida")

        elif opcao == '3':
            try:
                prefixo = input("Prefixo do texto: ")[:20]
                resultados = indices['texto'].buscar_prefixo(prefixo)
                total_resultados = len(resultados)
                tamanho_pagina = 10
                total_paginas = (total_resultados + tamanho_pagina - 1) // tamanho_pagina

                if total_resultados == 0:
                    print("Nenhum resultado encontrado.")
                else:
                    print(f"\n {total_resultados} resultado(s) encontrado(s). Use ← e → para navegar, 'q' para sair.")

                    pagina_atual = 0
                    while True:
                        # Limpa a tela (opcional)
                        print(f"\n Página {pagina_atual + 1} de {total_paginas}")
                        inicio = pagina_atual * tamanho_pagina
                        fim = inicio + tamanho_pagina
                        pagina = resultados[inicio:fim]

                        for pos in pagina:
                            r = ler_registro(ARQ_DAT, pos)
                            print(f"ID: {r['identificador']} — texto: {r['texto_long'][:60]}")

                        print("\n  ← : Esquerda / → : Direita / q para sair")

                        key = msvcrt.getch()
                        if key == b'\xe0':  #setas
                            key = msvcrt.getch()
                            if key == b'M':  #seta direita
                                if pagina_atual + 1 < total_paginas:
                                    pagina_atual += 1
                                else:
                                    print("Última página.")
                            elif key == b'K':  #seta esquerda
                                if pagina_atual > 0:
                                    pagina_atual -= 1
                                else:
                                    print("Primeira página.")
                        elif key == b'q':
                            print("Saindo...")
                            break
            except:
                print("❌ Entrada inválida")
        elif opcao == '4':
            try:
                chave = input("Disciplina: ")
                resultados = indices['disc'].buscar(chave)
                total_resultados = len(resultados)
                tamanho_pagina = 10
                total_paginas = (total_resultados + tamanho_pagina - 1) // tamanho_pagina

                if total_resultados == 0:
                    print("Nenhum resultado encontrado.")
                else:
                    print(f"\n {total_resultados} resultado(s) encontrado(s). Use ← e → para navegar, 'q' para sair.")

                    pagina_atual = 0
                    while True:
                        # Limpa a tela (opcional)
                        print(f"\n Página {pagina_atual + 1} de {total_paginas}")
                        inicio = pagina_atual * tamanho_pagina
                        fim = inicio + tamanho_pagina
                        pagina = resultados[inicio:fim]

                        for pos in pagina:
                            r = ler_registro(ARQ_DAT, pos)
                            print(f"ID: {r['identificador']} — disciplina: {r['disciplina']}")

                        print("\n  ← : Esquerda / → : Direita / q para sair")

                        key = msvcrt.getch()
                        if key == b'\xe0':  #setas
                            key = msvcrt.getch()
                            if key == b'M':  #seta direita
                                if pagina_atual + 1 < total_paginas:
                                    pagina_atual += 1
                                else:
                                    print("Última página.")
                            elif key == b'K':  #seta esquerda
                                if pagina_atual > 0:
                                    pagina_atual -= 1
                                else:
                                    print("Primeira página.")
                        elif key == b'q':
                            print("Saindo...")
                            break
            except:
                print("❌ Entrada inválida")

        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida")
