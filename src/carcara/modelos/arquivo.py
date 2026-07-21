"""
Modelo que representa um arquivo analisado pelo CarcaráAV.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Arquivo:
    caminho: Path
    nome: str
    extensao: str
    tamanho: int
    sha256: str | None = None

    @property
    def possui_hash(self) -> bool:
        return self.sha256 is not None

    @property
    def tamanho_kb(self) -> float:
        return self.tamanho / 1024

    @property
    def executavel(self) -> bool:
        return self.extensao.lower() in {
            ".exe",
            ".dll",
            ".msi",
            ".bat",
            ".cmd",
            ".com",
            ".scr",
            ".ps1",
            ".sh",
        }
