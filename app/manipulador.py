import struct

TAMANHO_REGISTRO = 248
FORMATO_REGISTRO = '10sii10sff200sff'  # Struct format: str[10], int, int, str[10], float, float, str[200], float, float

def pad_str(texto: str, tamanho: int) -> bytes:
    return texto.encode('utf-8')[:tamanho].ljust(tamanho, b'\x00')

def gravar_registro(caminho_arquivo: str, registro: dict) -> int:
    """
    Grava um registro no final do arquivo binário e retorna a posição
    """
    with open(caminho_arquivo, 'ab') as f:
        pos = f.tell()
        dados = struct.pack(
            FORMATO_REGISTRO,
            pad_str(registro['identificador'], 10),
            registro['ano'],
            registro['numero'],
            pad_str(registro['prova'], 10),
            registro['dificuldade'],
            registro['taxa_acerto'],
            pad_str(registro['texto'], 200),
            registro['discriminacao'],
            registro['acerto_chute'],
        )
        f.write(dados)
        return pos  # Retorna posição onde foi escrito

def ler_registro(caminho_arquivo: str, posicao: int) -> dict:
    """
    Lê um registro a partir de uma posição no arquivo binário
    """
    with open(caminho_arquivo, 'rb') as f:
        f.seek(posicao)
        dados = f.read(TAMANHO_REGISTRO)
        unpacked = struct.unpack(FORMATO_REGISTRO, dados)
        return {
            'identificador': unpacked[0].decode('utf-8').strip('\x00'),
            'ano': unpacked[1],
            'numero': unpacked[2],
            'prova': unpacked[3].decode('utf-8').strip('\x00'),
            'dificuldade': unpacked[4],
            'taxa_acerto': unpacked[5],
            'texto': unpacked[6].decode('utf-8').strip('\x00'),
            'discriminacao': unpacked[7],
            'acerto_chute': unpacked[8],
        }
