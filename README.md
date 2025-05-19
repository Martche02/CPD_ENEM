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
docker compose run --rm app
```

---

## Para desenvolvedores

### Estrutura de pastas

O projeto está organizado em três partes principais:

```
app/
├── main.py              # ponto de entrada principal
├── arvores/             # estruturas de dados
│   ├── binaria.py
│   ├── bmais.py
│   └── patricia.py
└── util/                # utilidades e lógica do domínio
    ├── atualizar.py
    ├── carregar.py
    ├── interface.py
    ├── manipulador.py
    ├── testes.py
    └── tri.py
```

### Visão geral dos arquivos

| Arquivo               | Função principal                                                                |
| --------------------- | ------------------------------------------------------------------------------- |
| `main.py`             | Entrada do sistema. Menu interativo para carregar dados, consultar, testar etc. |
| `util/carregar.py`    | Criação, limpeza, inserção e persistência de todos os índices.                  |
| `util/atualizar.py`   | Permite adicionar novos CSVs ou reaplicar dados do `combinado.json`.            |
| `util/interface.py`   | Interface de navegação interativa via terminal.                                 |
| `util/testes.py`      | Testes práticos rápidos.                                                        |
| `util/manipulador.py` | Leitura e escrita de registros `.dat` com estrutura binária fixa.               |
| `util/tri.py`         | Lógica da Teoria de Resposta ao Item (TRI).                                     |
| `arvores/binaria.py`  | Árvore binária para índices categóricos.                                        |
| `arvores/bmais.py`    | Árvore B+ para campos ordenáveis (como dificuldade).                            |
| `arvores/patricia.py` | Árvore Patricia para busca por prefixo em textos longos.                        |

### Detalhes técnicos

- Os dados das questões são armazenados no arquivo binário `questoes.dat`.
- Cada índice mapeia para a posição binária do registro.
- Os índices são persistidos em disco com serialização manual (plana), evitando problemas de recursão.
- O sistema suporta reconstrução total dos índices a partir do `.dat` e do `combinado.json`.

---

O sistema é modular, direto e extensível. Basta adaptar o `main.py` ou criar novas interfaces com base na estrutura já disponível.
