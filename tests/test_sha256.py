from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from carcara.hashes import calcular_sha256


class TestCalcularSHA256(unittest.TestCase):
    def test_calcula_hash_conhecido(self) -> None:
        conteudo = b"CarcaraAV"
        esperado = hashlib.sha256(conteudo).hexdigest()

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "arquivo.bin"
            caminho.write_bytes(conteudo)

            resultado = calcular_sha256(caminho)

        self.assertEqual(resultado, esperado)

    def test_calcula_hash_de_arquivo_vazio(self) -> None:
        esperado = hashlib.sha256(b"").hexdigest()

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "vazio.bin"
            caminho.write_bytes(b"")

            resultado = calcular_sha256(caminho)

        self.assertEqual(resultado, esperado)

    def test_progresso_termina_em_cem(self) -> None:
        percentuais: list[int] = []

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "arquivo.bin"
            caminho.write_bytes(b"A" * 1024)

            calcular_sha256(
                caminho,
                progresso=percentuais.append,
            )

        self.assertTrue(percentuais)
        self.assertEqual(percentuais[-1], 100)

    def test_arquivo_vazio_tambem_reporta_cem_por_cento(self) -> None:
        percentuais: list[int] = []

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "vazio.bin"
            caminho.write_bytes(b"")

            calcular_sha256(
                caminho,
                progresso=percentuais.append,
            )

        self.assertEqual(percentuais, [100])

    def test_falha_para_arquivo_inexistente(self) -> None:
        caminho = Path("/caminho/que/nao/existe/carcara.bin")

        with self.assertRaises(FileNotFoundError):
            calcular_sha256(caminho)

    def test_falha_quando_caminho_e_diretorio(self) -> None:
        with tempfile.TemporaryDirectory() as diretorio:
            with self.assertRaises(ValueError):
                calcular_sha256(Path(diretorio))


if __name__ == "__main__":
    unittest.main()
