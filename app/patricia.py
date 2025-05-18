from typing import List, Tuple

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
        print(f"[INSERIR] '{texto}' em posição {posicao}")
        self._inserir(self.raiz, texto.lower(), posicao)

    def _inserir(self, no: NoPatricia, texto: str, posicao: int) -> None:
        for i, (prefixo, filho) in enumerate(no.filhos):
            comum = self._prefixo_comum(prefixo, texto)
            if comum:
                if comum == prefixo:
                    self._inserir(filho, texto[len(comum):], posicao)
                else:
                    novo_filho = NoPatricia(prefixo[len(comum):])
                    novo_filho.filhos = filho.filhos
                    novo_filho.posicoes = filho.posicoes
                    novo_filho.fim = filho.fim

                    filho.chave = comum
                    filho.filhos = [(novo_filho.chave, novo_filho)]
                    filho.posicoes = []
                    filho.fim = False

                    self._inserir(filho, texto[len(comum):], posicao)
                return

        novo = NoPatricia(texto)
        novo.fim = True
        novo.posicoes.append(posicao)
        no.filhos.append((texto, novo))

    def buscar_prefixo(self, prefixo: str) -> List[int]:
        print(f"[BUSCAR] prefixo '{prefixo}'")
        return self._buscar(self.raiz, prefixo.lower())

    def _buscar(self, no: NoPatricia, prefixo: str) -> List[int]:
        for chave, filho in no.filhos:
            if prefixo.startswith(chave):
                return self._buscar(filho, prefixo[len(chave):])
            elif chave.startswith(prefixo):
                return self._coletar(filho)
        return []

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
