"""
Identifica o tipo real de um arquivo por sua assinatura.
"""

from pathlib import Path

from carcara.identificacao.assinaturas import ASSINATURAS


class IdentificadorDeArquivo:
    """
    Identifica o formato de um arquivo utilizando sua assinatura
    (magic number).
    """

    TAMANHO_MAXIMO_ASSINATURA = max(
        len(assinatura) for assinatura in ASSINATURAS
    )

    def identificar(self, caminho: str | Path) -> str:
        caminho_arquivo = Path(caminho)

        with caminho_arquivo.open("rb") as arquivo:
            cabecalho = arquivo.read(self.TAMANHO_MAXIMO_ASSINATURA)

        for assinatura, tipo in ASSINATURAS.items():
            if cabecalho.startswith(assinatura):
                return tipo

        return "DESCONHECIDO"
