"""
Compatibilidade temporária para o cálculo de SHA-256.

A implementação oficial está em carcara.hashes.sha256.
"""

from carcara.hashes.sha256 import (
    TAMANHO_BLOCO,
    calcular_sha256,
)

__all__ = [
    "TAMANHO_BLOCO",
    "calcular_sha256",
]
