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
                    # Caso comum total, segue para o filho
                    self._inserir(filho, texto[len(comum):], posicao)
                else:
                    # Dividir o nó
                    novo_filho = NoPatricia(prefixo[len(comum):])
                    # Transferir dados do filho antigo para o novo_filho
                    novo_filho.filhos = filho.filhos
                    novo_filho.posicoes = filho.posicoes
                    novo_filho.fim = filho.fim

                    # Atualizar o filho antigo com o prefixo comum
                    filho.chave = comum
                    filho.filhos = [(novo_filho.chave, novo_filho)]
                    filho.posicoes = []
                    filho.fim = False
                    # **Correção 1: atualizar aresta no pai**
                    no.filhos[i] = (comum, filho)

                    # Inserir o restante no filho antigo (agora ajustado)
                    restante = texto[len(comum):]
                    if restante == "":  
                        # **Correção 2: texto inserido termina exatamente aqui**
                        filho.fim = True
                        filho.posicoes.append(posicao)
                    else:
                        self._inserir(filho, restante, posicao)
                return

        # Não tem prefixo comum: novo filho (caso base)
        novo = NoPatricia(texto)
        novo.fim = True
        novo.posicoes.append(posicao)
        no.filhos.append((texto, novo))

    def buscar_prefixo(self, prefixo: str) -> List[int]:
        print(f"[BUSCAR] prefixo '{prefixo}'")
        return self._buscar(self.raiz, prefixo.lower())

    def _buscar(self, no: NoPatricia, prefixo: str) -> List[int]:
        resultado = []

        for chave, filho in no.filhos:
            print(f"[DEBUG] No: '{no.chave}' — Verificando aresta '{chave}' com prefixo '{prefixo}'")

            if prefixo.startswith(chave):
                # Continua descendo
                print(f"[DEBUG] '{prefixo}' começa com '{chave}' — descendo com '{prefixo[len(chave):]}'")
                resultado.extend(self._buscar(filho, prefixo[len(chave):]))

            elif chave.startswith(prefixo):
                # Encontrou onde o prefixo termina no meio da aresta
                print(f"[DEBUG] '{chave}' começa com '{prefixo}' — coletando tudo abaixo")
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
