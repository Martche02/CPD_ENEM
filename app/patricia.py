from typing import List, Tuple
import pickle

class NoPatricia:
    def __init__(self, chave: str = ''):
        self.chave: str = chave
        self.filhos: List[Tuple[str, 'NoPatricia']] = []
        self.posicoes: List[int] = []
        self.fim: bool = False

class PatriciaTree:
    def __init__(self):
        self.raiz = NoPatricia()

    def inserir(self, texto: str, posicao: int) -> None:
        self._inserir(self.raiz, texto.lower(), posicao)

    def _inserir(self, no: NoPatricia, texto: str, posicao: int) -> None:
        for i, (prefixo, filho) in enumerate(no.filhos):
            comum = self._prefixo_comum(prefixo, texto)
            if comum:
                if comum == prefixo:
                    # Caso comum total, segue para o filho
                    # Caso comum total, segue para o filho
                    self._inserir(filho, texto[len(comum):], posicao)
                else:
                    # Dividir o nó
                    # Dividir o nó
                    novo_filho = NoPatricia(prefixo[len(comum):])
                    # Transferir dados do filho antigo para o novo_filho
                    # Transferir dados do filho antigo para o novo_filho
                    novo_filho.filhos = filho.filhos
                    novo_filho.posicoes = filho.posicoes
                    novo_filho.fim = filho.fim

                    # Atualizar o filho antigo com o prefixo comum
                    # Atualizar o filho antigo com o prefixo comum
                    filho.chave = comum
                    filho.filhos = [(novo_filho.chave, novo_filho)]
                    filho.posicoes = []
                    filho.fim = False
                    no.filhos[i] = (comum, filho)
                    restante = texto[len(comum):]
                    if restante == "":  
                        filho.fim = True
                        filho.posicoes.append(posicao)
                    else:
                        self._inserir(filho, restante, posicao)
                return

        # Não tem prefixo comum: novo filho (caso base)
        # Não tem prefixo comum: novo filho (caso base)
        novo = NoPatricia(texto)
        novo.fim = True
        novo.posicoes.append(posicao)
        no.filhos.append((texto, novo))

    def buscar_prefixo(self, prefixo: str) -> List[int]:
        return self._buscar(self.raiz, prefixo.lower())

    def _buscar(self, no: NoPatricia, prefixo: str) -> List[int]:
        resultado = []

        resultado = []

        for chave, filho in no.filhos:
            if prefixo.startswith(chave):
                resultado.extend(self._buscar(filho, prefixo[len(chave):]))

            elif chave.startswith(prefixo):
                resultado.extend(self._coletar(filho))

        return resultado


    def _coletar(self, no: NoPatricia) -> List[int]:
        resultado = list(no.posicoes) if no.fim else []
        for _, filho in no.filhos:
            resultado.extend(self._coletar(filho))
        return resultado

    def _prefixo_comum(self, a: str, b: str) -> str:
        i = 0
        while i < min(len(a), len(b)) and a[i] == b[i]:
            i += 1
        return a[:i]

    def salvar_em_arquivo(self, caminho: str) -> None:
        """
        Serializa a árvore Patricia em forma plana.
        """
        nodes = []
        index_map = {}

        def walk(no):
            if no in index_map:
                return index_map[no]
            idx = len(nodes)
            index_map[no] = idx
            nodes.append({
                'chave': no.chave,
                'posicoes': no.posicoes,
                'fim': no.fim,
                'filhos': []  # preenchido depois
            })
            for chave, filho in no.filhos:
                child_idx = walk(filho)
                nodes[idx]['filhos'].append((chave, child_idx))
            return idx

        raiz_idx = walk(self.raiz)

        with open(caminho, 'wb') as f:
            pickle.dump({'raiz': raiz_idx, 'nodes': nodes}, f)

    @staticmethod
    def carregar_de_arquivo(caminho: str) -> 'PatriciaTree':
        with open(caminho, 'rb') as f:
            data = pickle.load(f)

        raw_nodes = data['nodes']
        inst = [NoPatricia() for _ in raw_nodes]

        for i, raw in enumerate(raw_nodes):
            inst[i].chave = raw['chave']
            inst[i].posicoes = raw['posicoes']
            inst[i].fim = raw['fim']

        for i, raw in enumerate(raw_nodes):
            inst[i].filhos = [(chave, inst[child_idx]) for chave, child_idx in raw['filhos']]

        tree = PatriciaTree()
        tree.raiz = inst[data['raiz']]
        return tree
