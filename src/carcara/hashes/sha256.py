"""
Implementação do algoritmo SHA-256.
"""

from hashlib import sha256
from pathlib import Path


TAMANHO_BLOCO = 64 * 1024


def calcular_sha256(caminho: Path) -> str:
    """
    Calcula o SHA-256 de um arquivo.
    """

    hash_arquivo = sha256()

    with caminho.open("rb") as arquivo:
        while bloco := arquivo.read(TAMANHO_BLOCO):
            hash_arquivo.update(bloco)

    return hash_arquivo.hexdigest()
