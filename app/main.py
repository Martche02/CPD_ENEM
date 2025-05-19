from util.carregar import (
    limpar_bases, criar_indices_vazios,
    inserir_csvs, atualizar_combinado,
    salvar_indices, carregar_indices
)
from util.atualizar import adicionar_csv_manual, reaplicar_json
from util.interface import menu
from util.testes import verificar_exemplo_por_id, testar_prefixo, testar_disciplina
from util.manipulador import TAMANHO_REGISTRO
import os

ARQ_DAT = 'dados/questoes.dat'

if __name__ == '__main__':
    while True:
        print("\n=== MENU ADMINISTRATIVO ===")
        print("1) Recarregar base completa (CSV + JSON)")
        print("2) Adicionar novo CSV manualmente")
        print("3) Atualizar registros com combinado.json")
        print("4) Testes rápidos")
        print("5) Entrar na interface de consulta")
        print("6) Sair")

        opcao = input("Escolha: ")

        # Carrega índices existentes apenas para leitura/consulta
        if opcao in ['3', '4', '5']:
            indices = carregar_indices()
        # Cria do zero para operações destrutivas
        else:
            indices = criar_indices_vazios()

        if opcao == '1':
            limpar_bases()
            inserir_csvs(indices)
            atualizar_combinado(indices)
            salvar_indices(indices)

        elif opcao == '2':
            caminho = input("Caminho do CSV: ")
            ano = int(input("Ano da prova: "))
            adicionar_csv_manual(caminho, ano, indices)
            salvar_indices(indices)

        elif opcao == '3':
            reaplicar_json(indices)
            salvar_indices(indices)

        elif opcao == '4':
            verificar_exemplo_por_id(indices)
            testar_prefixo(indices)
            testar_disciplina(indices)

        elif opcao == '5':
            menu(indices)

        else:
            print("Encerrando...")
            break
