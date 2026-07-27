"""
Modelo de domínio para evidências encontradas durante uma análise.
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Evidencia:
    codigo: str
    descricao: str
    severidade: str = "INFO"
