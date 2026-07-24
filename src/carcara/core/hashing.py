from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Callable


TAMANHO_BLOCO = 1024 * 1024


def calcular_sha256(
    caminho: str | Path,
    progresso: Callable[[int], None] | None = None,
) -> str:
    """
    Calcula o SHA-256 de um arquivo sem carregá-lo inteiro na memória.

    O arquivo é lido em blocos de 1 MiB, permitindo analisar arquivos
    grandes com baixo consumo de memória.
    """
    caminho_arquivo = Path(caminho).expanduser().resolve()

    if not caminho_arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    if not caminho_arquivo.is_file():
        raise ValueError(f"O caminho não representa um arquivo: {caminho_arquivo}")

    tamanho_total = caminho_arquivo.stat().st_size
    bytes_lidos = 0
    sha256 = hashlib.sha256()

    with caminho_arquivo.open("rb") as arquivo:
        while bloco := arquivo.read(TAMANHO_BLOCO):
            sha256.update(bloco)
            bytes_lidos += len(bloco)

            if progresso is not None:
                percentual = (
                    100
                    if tamanho_total == 0
                    else int(bytes_lidos * 100 / tamanho_total)
                )
                progresso(percentual)

    if progresso is not None:
        progresso(100)

    return sha256.hexdigest()
