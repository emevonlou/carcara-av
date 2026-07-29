"""
Orquestra os componentes responsáveis pela análise de arquivos.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from carcara.evidencias.coletor import ColetorDeEvidencias
from carcara.orquestracao.resultado import ResultadoAnalise
from carcara.scanner.analisador import AnalisadorDeArquivo


class MotorDeAnalise:
    """
    Coordena a coleta de informações e evidências de um arquivo.
    """

    def __init__(self) -> None:
        self.analisador = AnalisadorDeArquivo()
        self.coletor = ColetorDeEvidencias()

    def analisar(
        self,
        caminho: str | Path,
        progresso: Callable[[int], None] | None = None,
    ) -> ResultadoAnalise:
        arquivo = self.analisador.analisar(
            caminho,
            progresso=progresso,
        )

        evidencias = self.coletor.coletar(arquivo)

        return ResultadoAnalise(
            arquivo=arquivo,
            evidencias=tuple(evidencias),
        )
