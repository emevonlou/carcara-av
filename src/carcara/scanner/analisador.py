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

        return Arquivo(
            caminho=caminho_arquivo,
            nome=caminho_arquivo.name,
            extensao=caminho_arquivo.suffix.lower(),
            tamanho=caminho_arquivo.stat().st_size,
            sha256=calcular_sha256(
                caminho_arquivo,
                progresso=progresso,
            ),
            tipo_real=self.identificador.identificar(
                caminho_arquivo
            ),
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
