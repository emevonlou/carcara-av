"""
Ponto de entrada do CarcaráAV.
"""

import sys
from pathlib import Path

DIRETORIO_SRC = Path(__file__).parent / "src"
sys.path.insert(0, str(DIRETORIO_SRC))

from carcara.scanner import AnalisadorDeArquivo, ErroDeAnalise


def main() -> None:
    print("CarcaráAV")
    print("Segurança transparente. Sistema limpo.")
    print()

    if len(sys.argv) < 2:
        print("Uso: python3 main.py <caminho-do-arquivo>")
        return

    analisador = AnalisadorDeArquivo()

    try:
        arquivo = analisador.analisar(sys.argv[1])
    except ErroDeAnalise as erro:
        print(f"Erro: {erro}")
        return

    print(f"Arquivo: {arquivo.nome}")
    print(f"Caminho: {arquivo.caminho}")
    print(f"Extensão: {arquivo.extensao or 'sem extensão'}")
    print(f"Tamanho: {arquivo.tamanho} bytes")
    print(f"Tamanho em KB: {arquivo.tamanho_kb:.2f}")
    print(f"Executável: {'sim' if arquivo.executavel else 'não'}")
    print(f"SHA-256: {arquivo.sha256}")
    print(f"Tipo real: {arquivo.tipo_real}")


if __name__ == "__main__":
    main()

