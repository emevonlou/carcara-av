"""
Resultado consolidado produzido pelo motor de análise.
"""

from dataclasses import dataclass

from carcara.evidencias.evidencia import Evidencia
from carcara.modelos.arquivo import Arquivo


@dataclass(slots=True, frozen=True)
class ResultadoAnalise:
    """
    Reúne os dados observados durante a análise de um arquivo.
    """

    arquivo: Arquivo
    evidencias: tuple[Evidencia, ...]

    @property
    def possui_evidencias(self) -> bool:
        return bool(self.evidencias)

    @property
    def quantidade_evidencias(self) -> int:
        return len(self.evidencias)
