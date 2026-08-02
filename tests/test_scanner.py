from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from carcara.scanner import AnalisadorDeArquivo, ErroDeAnalise


class TestAnalisadorDeArquivo(unittest.TestCase):
    def setUp(self) -> None:
        self.analisador = AnalisadorDeArquivo()

    def test_coleta_dados_basicos_do_arquivo(self) -> None:
        conteudo = b"\x7fELFconteudo-de-teste"
        hash_esperado = hashlib.sha256(conteudo).hexdigest()

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "amostra.bin"
            caminho.write_bytes(conteudo)

            resultado = self.analisador.analisar(caminho)

            self.assertEqual(resultado.caminho, caminho.resolve())
            self.assertEqual(resultado.nome, "amostra.bin")
            self.assertEqual(resultado.extensao, ".bin")
            self.assertEqual(resultado.tamanho, len(conteudo))
            self.assertEqual(resultado.sha256, hash_esperado)
            self.assertEqual(resultado.tipo_real, "ELF")

    def test_encaminha_progresso_do_hash(self) -> None:
        percentuais: list[int] = []

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "amostra.bin"
            caminho.write_bytes(b"A" * 1024)

            self.analisador.analisar(
                caminho,
                progresso=percentuais.append,
            )

        self.assertTrue(percentuais)
        self.assertEqual(percentuais[-1], 100)

    def test_falha_para_caminho_inexistente(self) -> None:
        caminho = Path(
            "/caminho/que/nao/existe/carcara-amostra.bin"
        )

        with self.assertRaises(ErroDeAnalise):
            self.analisador.analisar(caminho)

    def test_falha_quando_caminho_e_diretorio(self) -> None:
        with tempfile.TemporaryDirectory() as diretorio:
            with self.assertRaises(ErroDeAnalise):
                self.analisador.analisar(Path(diretorio))


if __name__ == "__main__":
    unittest.main()

