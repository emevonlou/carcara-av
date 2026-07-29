"""
Coleta evidências a partir das características observadas em um arquivo.
"""

from carcara.evidencias.evidencia import Evidencia
from carcara.modelos.arquivo import Arquivo


class ColetorDeEvidencias:
    """
    Produz evidências a partir dos fatos observados em um arquivo.
    """

    def coletar(self, arquivo: Arquivo) -> list[Evidencia]:
        evidencias: list[Evidencia] = []

        if arquivo.tipo_real == "ELF":
            evidencias.append(
                Evidencia(
                    codigo="E001",
                    descricao="O arquivo possui formato ELF.",
                    severidade="INFO",
                )
            )

        if arquivo.tipo_real == "PE":
            evidencias.append(
                Evidencia(
                    codigo="E002",
                    descricao="O arquivo possui formato PE.",
                    severidade="INFO",
                )
            )

        return evidencias
