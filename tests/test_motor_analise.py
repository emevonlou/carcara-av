from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from carcara.orquestracao import (
    MotorDeAnalise,
    ResultadoAnalise,
)


class TestMotorDeAnalise(unittest.TestCase):
    def setUp(self) -> None:
        self.motor = MotorDeAnalise()

    def test_reune_arquivo_e_evidencias(self) -> None:
        conteudo = b"\x7fELFconteudo"
        hash_esperado = hashlib.sha256(conteudo).hexdigest()

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "programa.bin"
            caminho.write_bytes(conteudo)

            resultado = self.motor.analisar(caminho)

        self.assertIsInstance(resultado, ResultadoAnalise)

        self.assertEqual(
            resultado.arquivo.sha256,
            hash_esperado,
        )
        self.assertEqual(
            resultado.arquivo.tipo_real,
            "ELF",
        )

        self.assertTrue(resultado.possui_evidencias)
        self.assertEqual(
            resultado.quantidade_evidencias,
            1,
        )

        self.assertIsInstance(
            resultado.evidencias,
            tuple,
        )
        self.assertEqual(
            resultado.evidencias[0].codigo,
            "E001",
        )

    def test_resultado_sem_evidencias_e_explicito(self) -> None:
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "texto.txt"
            caminho.write_bytes(
                b"conteudo sem assinatura conhecida"
            )

            resultado = self.motor.analisar(caminho)

        self.assertFalse(resultado.possui_evidencias)
        self.assertEqual(
            resultado.quantidade_evidencias,
            0,
        )
        self.assertEqual(resultado.evidencias, ())

    def test_encaminha_progresso_ate_cem(self) -> None:
        percentuais: list[int] = []

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "arquivo.bin"
            caminho.write_bytes(b"A" * 2048)

            self.motor.analisar(
                caminho,
                progresso=percentuais.append,
            )

        self.assertTrue(percentuais)
        self.assertEqual(percentuais[-1], 100)


if __name__ == "__main__":
    unittest.main()
