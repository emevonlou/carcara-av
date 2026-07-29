"""
Implementação do cálculo de hash SHA-256.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from pathlib import Path


TAMANHO_BLOCO = 1024 * 1024


def calcular_sha256(
    caminho: str | Path,
    progresso: Callable[[int], None] | None = None,
) -> str:
    """
    Calcula o SHA-256 de um arquivo sem carregá-lo inteiro na memória.

    O arquivo é lido em blocos de 1 MiB. Quando fornecida, a função
    de progresso recebe valores inteiros entre 0 e 100.
    """

    caminho_arquivo = Path(caminho).expanduser().resolve()

    if not caminho_arquivo.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho_arquivo}"
        )

    if not caminho_arquivo.is_file():
        raise ValueError(
            f"O caminho não representa um arquivo: {caminho_arquivo}"
        )

    tamanho_total = caminho_arquivo.stat().st_size
    bytes_lidos = 0
    ultimo_percentual = -1
    hash_arquivo = hashlib.sha256()

    with caminho_arquivo.open("rb") as arquivo:
        while bloco := arquivo.read(TAMANHO_BLOCO):
            hash_arquivo.update(bloco)
            bytes_lidos += len(bloco)

            if progresso is not None:
                percentual = min(
                    100,
                    int(bytes_lidos * 100 / tamanho_total),
                )

                if percentual != ultimo_percentual:
                    progresso(percentual)
                    ultimo_percentual = percentual

    if progresso is not None and ultimo_percentual < 100:
        progresso(100)

    return hash_arquivo.hexdigest()
