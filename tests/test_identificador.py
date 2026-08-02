from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from carcara.identificacao import IdentificadorDeArquivo


class TestIdentificadorDeArquivo(unittest.TestCase):
    def setUp(self) -> None:
        self.identificador = IdentificadorDeArquivo()

    def _identificar(self, conteudo: bytes) -> str:
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "amostra.bin"
            caminho.write_bytes(conteudo)

            return self.identificador.identificar(caminho)

    def test_identifica_formatos_conhecidos(self) -> None:
        casos = (
            (b"%PDF-1.7\n", "PDF"),
            (b"\x89PNG\r\n\x1a\nrestante", "PNG"),
            (b"\xff\xd8\xffrestante", "JPEG"),
            (b"PK\x03\x04restante", "ZIP"),
            (b"MZrestante", "PE"),
            (b"\x7fELFrestante", "ELF"),
        )

        for conteudo, esperado in casos:
            with self.subTest(tipo=esperado):
                resultado = self._identificar(conteudo)

                self.assertEqual(resultado, esperado)

    def test_retorna_desconhecido_para_assinatura_nao_reconhecida(
        self,
    ) -> None:
        resultado = self._identificar(
            b"conteudo sem assinatura conhecida"
        )

        self.assertEqual(resultado, "DESCONHECIDO")

    def test_retorna_desconhecido_para_arquivo_vazio(self) -> None:
        resultado = self._identificar(b"")

        self.assertEqual(resultado, "DESCONHECIDO")


if __name__ == "__main__":
    unittest.main()
