import pickle
from typing import List, Dict

class NoBinaria:
    def __init__(self, chave: str, posicao: int):
        self.chave: str = chave
        self.posicao: int = posicao
        self.esq: NoBinaria | None = None
        self.dir: NoBinaria | None = None

class BinariaTree:
    def __init__(self):
        self.raiz: NoBinaria | None = None

    def inserir(self, chave: str, posicao: int) -> None:
        if self.raiz is None:
            self.raiz = NoBinaria(chave, posicao)
        else:
            self._inserir_rec(self.raiz, chave, posicao)

    def _inserir_rec(self, no: NoBinaria, chave: str, posicao: int) -> None:
        if chave < no.chave:
            if no.esq is None:
                no.esq = NoBinaria(chave, posicao)
            else:
                self._inserir_rec(no.esq, chave, posicao)
        elif chave > no.chave:
            if no.dir is None:
                no.dir = NoBinaria(chave, posicao)
            else:
                self._inserir_rec(no.dir, chave, posicao)
        else:
            no.posicao = posicao

    def buscar(self, chave: str) -> int | None:
        return self._buscar_rec(self.raiz, chave)

    def _buscar_rec(self, no: NoBinaria | None, chave: str) -> int | None:
        if no is None:
            return None
        if chave == no.chave:
            return no.posicao
        if chave < no.chave:
            return self._buscar_rec(no.esq, chave)
        return self._buscar_rec(no.dir, chave)

    def salvar_em_arquivo(self, caminho: str) -> None:
        """
        Serializa a árvore em forma plana:
        - 'nodes': lista de dicionários com 'chave', 'posicao', 'esq', 'dir'
        - 'raiz': índice do nó raiz na lista (ou None)
        """
        if self.raiz is None:
            data = {'raiz': None, 'nodes': []}
        else:
            nodes: List[Dict] = []
            mapping: Dict[NoBinaria, int] = {}
            stack = [self.raiz]
            while stack:
                node = stack.pop()
                if node not in mapping:
                    idx = len(nodes)
                    mapping[node] = idx
                    nodes.append({'chave': node.chave, 'posicao': node.posicao, 'esq': None, 'dir': None})
                    if node.esq:
                        stack.append(node.esq)
                    if node.dir:
                        stack.append(node.dir)
            for node, idx in mapping.items():
                entry = nodes[idx]
                entry['esq'] = mapping.get(node.esq)
                entry['dir'] = mapping.get(node.dir)
            data = {'raiz': mapping[self.raiz], 'nodes': nodes}
        with open(caminho, 'wb') as f:
            pickle.dump(data, f)

    def carregar_de_arquivo(self, caminho: str) -> None:
        """
        Lê a lista plana e reconstrói a árvore binária em memória.
        """
        try:
            with open(caminho, 'rb') as f:
                data = pickle.load(f)
        except FileNotFoundError:
            self.raiz = None
            return

        nodes_data = data.get('nodes', [])
        raiz_idx = data.get('raiz')
        if raiz_idx is None or not nodes_data:
            self.raiz = None
            return

        instancias: List[NoBinaria] = []
        for entry in nodes_data:
            instancias.append(NoBinaria(entry['chave'], entry['posicao']))
        for idx, entry in enumerate(nodes_data):
            no = instancias[idx]
            esq = entry.get('esq')
            dir_ = entry.get('dir')
            no.esq = instancias[esq] if esq is not None else None
            no.dir = instancias[dir_] if dir_ is not None else None
        self.raiz = instancias[raiz_idx]

    def todos(self):
        resultados = []
        def percorrer(no: NoBinaria) -> None:
            if no is None:
                return
            percorrer(no.esq)
            resultados.append((no.chave, no.posicao))
            percorrer(no.dir)
        percorrer(self.raiz)
        return resultados