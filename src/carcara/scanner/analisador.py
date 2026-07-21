"""
Coleta informações básicas de arquivos para análise.
"""

from hashlib import sha256
from pathlib import Path

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
    - hash SHA-256.
    """

    TAMANHO_BLOCO = 64 * 1024

    def analisar(self, caminho: str | Path) -> Arquivo:
        caminho_arquivo = Path(caminho).expanduser().resolve()

        self._validar(caminho_arquivo)

        return Arquivo(
            caminho=caminho_arquivo,
            nome=caminho_arquivo.name,
            extensao=caminho_arquivo.suffix.lower(),
            tamanho=caminho_arquivo.stat().st_size,
            sha256=self._calcular_sha256(caminho_arquivo),
        )

    def _validar(self, caminho: Path) -> None:
        if not caminho.exists():
            raise ErroDeAnalise(
                f"O caminho informado não existe: {caminho}"
            )

        if not caminho.is_file():
            raise ErroDeAnalise(
                f"O caminho informado não representa um arquivo: {caminho}"
            )

    def _calcular_sha256(self, caminho: Path) -> str:
        hash_arquivo = sha256()

        try:
            with caminho.open("rb") as arquivo:
                while bloco := arquivo.read(self.TAMANHO_BLOCO):
                    hash_arquivo.update(bloco)
        except PermissionError as erro:
            raise ErroDeAnalise(
                f"Permissão negada para ler o arquivo: {caminho}"
            ) from erro
        except OSError as erro:
            raise ErroDeAnalise(
                f"Não foi possível ler o arquivo: {caminho}"
            ) from erro

        return hash_arquivo.hexdigest()
