from __future__ import annotations

import unittest
from pathlib import Path

from carcara.evidencias import ColetorDeEvidencias
from carcara.modelos import Arquivo


class TestColetorDeEvidencias(unittest.TestCase):
    def setUp(self) -> None:
        self.coletor = ColetorDeEvidencias()

    def _arquivo(self, tipo_real: str) -> Arquivo:
        return Arquivo(
            caminho=Path("/tmp/amostra"),
            nome="amostra",
            extensao="",
            tamanho=0,
            sha256=None,
            tipo_real=tipo_real,
        )

    def test_produz_evidencia_para_elf(self) -> None:
        evidencias = self.coletor.coletar(
            self._arquivo("ELF")
        )

        self.assertEqual(len(evidencias), 1)

        evidencia = evidencias[0]

        self.assertEqual(evidencia.codigo, "E001")
        self.assertEqual(
            evidencia.descricao,
            "O arquivo possui formato ELF.",
        )
        self.assertEqual(evidencia.severidade, "INFO")

    def test_produz_evidencia_para_pe(self) -> None:
        evidencias = self.coletor.coletar(
            self._arquivo("PE")
        )

        self.assertEqual(len(evidencias), 1)

        evidencia = evidencias[0]

        self.assertEqual(evidencia.codigo, "E002")
        self.assertEqual(
            evidencia.descricao,
            "O arquivo possui formato PE.",
        )
        self.assertEqual(evidencia.severidade, "INFO")

    def test_nao_inventa_evidencia_para_tipo_desconhecido(
        self,
    ) -> None:
        evidencias = self.coletor.coletar(
            self._arquivo("DESCONHECIDO")
        )

        self.assertEqual(evidencias, [])


if __name__ == "__main__":
    unittest.main()
