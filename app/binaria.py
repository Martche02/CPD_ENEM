import pickle

class NoBinaria:
    def __init__(self, chave: str, posicao: int):
        self.chave: str = chave                # Ex: "2023123"
        self.posicao: int = posicao         # Pode ter várias posições com a mesma chave
        self.esq: NoBinaria | None = None
        self.dir: NoBinaria | None = None

class BinariaTree:
    def __init__(self):
        self.raiz = None

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

    def _buscar_rec(self, no: NoBinaria, chave: str) -> int | None:
        if no is None:
            return None
        if chave == no.chave:
            return no.posicao
        elif chave < no.chave:
            return self._buscar_rec(no.esq, chave)
        else:
            return self._buscar_rec(no.dir, chave)

    def salvar_em_arquivo(self, caminho: str) -> None:
        with open(caminho, 'wb') as f:
            pickle.dump(self.raiz, f)

    def carregar_de_arquivo(self, caminho: str) -> None:
        try:
            with open(caminho, 'rb') as f:
                self.raiz = pickle.load(f)
        except FileNotFoundError:
            self.raiz = None
