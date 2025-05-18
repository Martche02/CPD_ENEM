from typing import List, Callable

class NoBMais:
    def __init__(self, folha=False):
        self.folha: bool = folha
        self.chaves: List[float] = []
        self.filhos: List[int | 'NoBMais'] = []  # Se folha: são posições no arquivo .dat; se interno: são filhos
        self.prox: NoBMais | None = None  # Ponteiro para próxima folha (só para nós folha)

class BMaisTree:
    def __init__(self, ordem: int = 4):
        self.raiz = NoBMais(folha=True)
        self.ordem = ordem

    def buscar(self, chave: str, no: NoBMais = None) -> int | None:
        if no is None:
            no = self.raiz

        if no.folha:
            for i, k in enumerate(no.chaves):
                if k == chave:
                    return no.filhos[i]  # posição no .dat
            return None
        else:
            for i, k in enumerate(no.chaves):
                if chave < k:
                    return self.buscar(chave, no.filhos[i])
            return self.buscar(chave, no.filhos[-1])

    def inserir(self, chave: str, posicao: int) -> None:
        raiz = self.raiz
        if len(raiz.chaves) == self.ordem - 1:
            nova_raiz = NoBMais()
            nova_raiz.filhos.append(self.raiz)
            self._dividir_filho(nova_raiz, 0)
            self.raiz = nova_raiz

        self._inserir_nao_cheio(self.raiz, chave, posicao)

    def _inserir_nao_cheio(self, no: NoBMais, chave: str, posicao: int) -> None:
        if no.folha:
            i = 0
            while i < len(no.chaves) and chave > no.chaves[i]:
                i += 1
            no.chaves.insert(i, chave)
            no.filhos.insert(i, posicao)
        else:
            i = 0
            while i < len(no.chaves) and chave > no.chaves[i]:
                i += 1
            filho = no.filhos[i]
            if len(filho.chaves) == self.ordem - 1:
                self._dividir_filho(no, i)
                if chave > no.chaves[i]:
                    i += 1
            self._inserir_nao_cheio(no.filhos[i], chave, posicao)

    def _dividir_filho(self, pai: NoBMais, i: int) -> None:
        ordem = self.ordem
        y = pai.filhos[i]
        z = NoBMais(folha=y.folha)

        meio = ordem // 2

        pai.chaves.insert(i, y.chaves[meio])
        pai.filhos.insert(i + 1, z)

        z.chaves = y.chaves[meio + 1:]
        y.chaves = y.chaves[:meio]

        if y.folha:
            z.filhos = y.filhos[meio + 1:]
            y.filhos = y.filhos[:meio + 1]
            z.prox = y.prox
            y.prox = z
        else:
            z.filhos = y.filhos[meio + 1:]
            y.filhos = y.filhos[:meio + 1]

    def percorrer_em_ordem(self, callback: Callable[[int], None]) -> None:
        no = self.raiz
        while not no.folha:
            no = no.filhos[0]
        while no:
            for pos in no.filhos:
                callback(pos)
            no = no.prox
