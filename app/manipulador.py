import struct
from typing import Dict, TypedDict

# Prefixo '=' desativa padding / sem alinhamento extra
PAD = '='
class registro(TypedDict):
    identificador: int
    ano: int
    numero: int
    prova: str
    dificuldade: float
    taxa_acerto: float
    texto_long: str
    disciplina: str
    conteudo: str
    topico: str
    discriminacao: float
    acerto_chute: float
# Novo formato: int identificador, int ano, int numero, 10s prova, f dificuldade, 
# f taxa_acerto, 2000s texto_long, 20s disciplina, 20s conteudo, 20s topico, f discriminacao, f acerto_chute
FORMATO_REGISTRO = PAD + 'iii10sff2000s20s20s20sff'
TAMANHO_REGISTRO  = struct.calcsize(FORMATO_REGISTRO)
# Deve ser 2098:
# print("TAMANHO_REGISTRO:", TAMANHO_REGISTRO)

def pad_str(texto: str, tamanho: int) -> bytes:
    b = texto.encode('utf-8', errors='ignore')[:tamanho]
    return b.ljust(tamanho, b'\x00')

def gravar_registro(caminho_arquivo: str, registro: registro) -> int:
    bloco = struct.pack(
        FORMATO_REGISTRO,
        int(registro['identificador']),              # 0: int
        registro['ano'],                             # 1: int
        registro['numero'],                          # 2: int
        pad_str(registro.get('prova',''), 10),       # 3: 10s
        registro.get('dificuldade', 0.0),            # 4: f
        registro.get('taxa_acerto', 0.0),            # 5: f
        pad_str(registro.get('texto_long',''), 2000),# 6: 2000s
        pad_str(registro.get('disciplina',''), 20),  # 7: 20s
        pad_str(registro.get('conteudo',''), 20),    # 8: 20s
        pad_str(registro.get('topico',''), 20),      # 9: 20s
        registro.get('discriminacao', 0.0),          # 10: f
        registro.get('acerto_chute', 0.0),           # 11: f
    )
    assert len(bloco) == TAMANHO_REGISTRO, \
        f"Registro tem {len(bloco)} bytes (esperado {TAMANHO_REGISTRO})"
    with open(caminho_arquivo, 'ab') as f:
        pos = f.tell()
        f.write(bloco)
    return pos

def ler_registro(caminho_arquivo: str, posicao: int) -> registro:
    with open(caminho_arquivo, 'rb') as f:
        f.seek(posicao)
        dados = f.read(TAMANHO_REGISTRO)
    assert len(dados) == TAMANHO_REGISTRO, \
        f"Lido {len(dados)} bytes (esperado {TAMANHO_REGISTRO})"
    u = struct.unpack(FORMATO_REGISTRO, dados)
    return {
        'identificador': u[0],  # já int
        'ano':           u[1],
        'numero':        u[2],
        'prova':         u[3].decode('utf-8', errors='ignore').rstrip('\x00'),
        'dificuldade':   u[4],
        'taxa_acerto':   u[5],
        'texto_long':    u[6].decode('utf-8', errors='ignore').rstrip('\x00'),
        'disciplina':    u[7].decode('utf-8', errors='ignore').rstrip('\x00'),
        'conteudo':      u[8].decode('utf-8', errors='ignore').rstrip('\x00'),
        'topico':        u[9].decode('utf-8', errors='ignore').rstrip('\x00'),
        'discriminacao': u[10],
        'acerto_chute':  u[11],
    }

# Offsets para atualização pontual:
CAMPOS_INFO: Dict[str, tuple[int,str]] = {
    'texto_long':    (4+4+4+10+4+4,      PAD+'2000s'),  # 30
    'disciplina':    (30+2000,           PAD+'20s'),   # 2030
    'conteudo':      (2030+20,           PAD+'20s'),   # 2050
    'topico':        (2050+20,           PAD+'20s'),   # 2070
    'dificuldade':   (4+4+4+10,          PAD+'f'),     # 22
    'taxa_acerto':   (22+4,               PAD+'f'),     # 26
    'discriminacao': (2070+20,           PAD+'f'),     # 2090
    'acerto_chute':  (2090+4,            PAD+'f'),     # 2094
}
def reescrever_registro(caminho_arquivo: str, pos: int, registro: registro) -> None:
    bloco = struct.pack(
        FORMATO_REGISTRO,
        int(registro['identificador']),
        int(registro['ano']),
        int(registro['numero']),
        pad_str(registro.get('prova',''), 10),
        registro.get('dificuldade', 0.0),
        registro.get('taxa_acerto', 0.0),
        pad_str(registro.get('texto_long',''), 2000),
        pad_str(registro.get('disciplina',''), 20),
        pad_str(registro.get('conteudo',''), 20),
        pad_str(registro.get('topico',''), 20),
        registro.get('discriminacao', 0.0),
        registro.get('acerto_chute', 0.0),
    )
    assert len(bloco) == TAMANHO_REGISTRO, \
        f"Tamanho errado: {len(bloco)} (esperado {TAMANHO_REGISTRO})"
    with open(caminho_arquivo, 'r+b') as f:
        f.seek(pos)
        f.write(bloco)
