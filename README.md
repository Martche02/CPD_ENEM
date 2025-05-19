# Projeto De Busca de Questões do ENEM

Este projeto usa estruturas de dados avançadas (árvore binária, árvore B+, árvore Patricia) para classificar e pesquisar questões do ENEM com base em múltiplos critérios (ID, texto, dificuldade, disciplina etc.).

## Requisitos

- Python 3.12

### OU

- Docker instalado ([veja como instalar aqui](https://www.docker.com/products/docker-desktop/))

## Como rodar

Abra o terminal e execute:

```bash
git clone https://github.com/Martche02/CPD_ENEM.git
cd CPD_ENEM
python app/main.py
```

### Com Docker

```bash
git clone https://github.com/Martche02/CPD_ENEM.git
cd CPD_ENEM
docker compose up
```

---

## Para desenvolvedores

### Visão geral

O sistema é dividido em módulos com responsabilidades bem definidas. O ponto central de controle é o `main.py`, que orquestra as operações administrativas: carregamento da base, atualizações e testes.

### Arquivos principais e responsabilidades

| Arquivo         | Função principal                                                                 |
|-----------------|----------------------------------------------------------------------------------|
| `main.py`       | Entrada do sistema. Gerencia o menu principal e chama as funções necessárias.   |
| `carregar.py`   | Criação, limpeza, inserção e persistência de todos os índices.                  |
| `atualizar.py`  | Permite adicionar CSVs manuais e reaplicar dados do `combinado.json`.           |
| `interface.py`  | Interface de navegação interativa via terminal para buscas manuais.             |
| `testes.py`     | Contém testes práticos para validação rápida do funcionamento.                  |
| `manipulador.py`| Leitura, escrita e reescrita de registros `.dat` com mapeamento fixo.           |
| `tri.py`        | Lógica de cálculo da taxa de acerto segundo o modelo TRI (3 parâmetros).        |

### Estruturas de dados

| Arquivo         | Estrutura                     | Uso                                                          |
|-----------------|-------------------------------|--------------------------------------------------------------|
| `binaria.py`    | Árvore Binária de Busca       | Para campos categóricos (disciplina, conteúdo, tópico etc.) |
| `bmais.py`      | Árvore B+                     | Para valores ordenáveis como a dificuldade (NU_PARAM_B).     |
| `patricia.py`   | Árvore Patricia               | Para texto longo com busca por prefixo (`texto_long`).       |

Todos os índices são persistidos em disco, com serialização manual (plana) para evitar problemas de recursão com `pickle`.

### Estrutura de dados

- Registros são armazenados no arquivo binário `questoes.dat`.
- Cada índice aponta para uma posição exata dentro desse arquivo.
- Há suporte completo à reconstrução dos índices sem necessidade de reprocessar os CSVs.

---

O sistema é modular, extensível e projetado para escalar com segurança. Basta alterar o `main.py` ou criar novas interfaces para expandir suas funcionalidades.
