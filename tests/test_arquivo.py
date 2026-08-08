from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from carcara.modelos import Arquivo


class TestArquivo(unittest.TestCase):
    def test_nao_permite_alterar_snapshot_depois_de_criado(
        self,
    ) -> None:
        arquivo = Arquivo(
            caminho=Path("/tmp/amostra.bin"),
            nome="amostra.bin",
            extensao=".bin",
            tamanho=128,
            sha256="abc123",
            tipo_real="ELF",
        )

        with self.assertRaises(FrozenInstanceError):
            arquivo.sha256 = "outro-hash"


if __name__ == "__main__":
    unittest.main()
