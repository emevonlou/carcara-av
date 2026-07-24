from __future__ import annotations

import sys
from pathlib import Path


RAIZ_PROJETO = Path(__file__).resolve().parent
DIRETORIO_SRC = RAIZ_PROJETO / "src"

if str(DIRETORIO_SRC) not in sys.path:
    sys.path.insert(0, str(DIRETORIO_SRC))

from carcara.app import executar


if __name__ == "__main__":
    raise SystemExit(executar())
