from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class Arquivo:
    caminho: Path
    nome: str
    extensao: str
    tamanho: int
    sha256: str | None = None
    tipo_real: str | None = None

    @property
    def possui_hash(self) -> bool:
        return self.sha256 is not None

    @property
    def possui_tipo_real(self) -> bool:
        return self.tipo_real is not None

    @property
    def tamanho_kb(self) -> float:
        return self.tamanho / 1024

    @property
    def executavel(self) -> bool:
        tipos_executaveis = {
            "PE",
            "ELF",
        }

        extensoes_executaveis = {
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

        return (
            self.tipo_real in tipos_executaveis
            or self.extensao.lower() in extensoes_executaveis
        )
