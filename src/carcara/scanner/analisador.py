"""
Coleta informações básicas de arquivos para análise.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from carcara.hashes import calcular_sha256
from carcara.identificacao import IdentificadorDeArquivo
from carcara.modelos import Arquivo


class ErroDeAnalise(Exception):
    """Erro ocorrido durante a coleta de informações de um arquivo."""


class AnalisadorDeArquivo:
    """
    Analisa um arquivo e retorna suas informações básicas.

    Nesta etapa, o analisador coleta:

    - caminho;
    - nome;
    - extensão;
    - tamanho;
    - hash SHA-256;
    - tipo real do arquivo.
    """

    def __init__(self) -> None:
        self.identificador = IdentificadorDeArquivo()

    def analisar(
        self,
        caminho: str | Path,
        progresso: Callable[[int], None] | None = None,
    ) -> Arquivo:
        caminho_arquivo = Path(caminho).expanduser().resolve()

        self._validar(caminho_arquivo)

        estado_inicial = caminho_arquivo.stat()

        hash_sha256 = calcular_sha256(
            caminho_arquivo,
            progresso=progresso,
        )

        tipo_real = self.identificador.identificar(
            caminho_arquivo
        )

        estado_final = caminho_arquivo.stat()

        assinatura_inicial = (
            estado_inicial.st_dev,
            estado_inicial.st_ino,
            estado_inicial.st_size,
            estado_inicial.st_mtime_ns,
            estado_inicial.st_ctime_ns,
        )

        assinatura_final = (
            estado_final.st_dev,
            estado_final.st_ino,
            estado_final.st_size,
            estado_final.st_mtime_ns,
            estado_final.st_ctime_ns,
        )

        if assinatura_inicial != assinatura_final:
            raise ErroDeAnalise(
                "O arquivo foi alterado durante a análise: "
                f"{caminho_arquivo}"
            )

        return Arquivo(
            caminho=caminho_arquivo,
            nome=caminho_arquivo.name,
            extensao=caminho_arquivo.suffix.lower(),
            tamanho=estado_inicial.st_size,
            sha256=hash_sha256,
            tipo_real=tipo_real,
        )

    def _validar(self, caminho: Path) -> None:
        if not caminho.exists():
            raise ErroDeAnalise(
                f"O caminho informado não existe: {caminho}"
            )

        if not caminho.is_file():
            raise ErroDeAnalise(
                "O caminho informado não representa um arquivo: "
                f"{caminho}"
            )
