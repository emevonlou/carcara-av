from __future__ import annotations

import random


MENSAGENS_INICIAIS = (
    "Cada detalhe conta.",
    "O horizonte está calmo. Podemos começar.",
    "Pronto para uma segunda olhada.",
    "Nenhum byte passa despercebido.",
)

MENSAGENS_ANALISE = (
    "Sobrevoando os bytes...",
    "Este arquivo resolveu chamar atenção.",
    "Observando cada detalhe.",
    "Um hash por vez. Sem alarde.",
)

MENSAGENS_CONCLUSAO = (
    "Observação concluída.",
    "Agora conhecemos melhor este arquivo.",
    "Nada além dos fatos. A decisão é sua.",
    "O arquivo contou sua história.",
)

MENSAGENS_ERRO = (
    "Algo interrompeu o voo.",
    "Este caminho merece outra tentativa.",
    "Nem todo arquivo gosta de colaborar.",
)


def mensagem_inicial() -> str:
    return random.choice(MENSAGENS_INICIAIS)


def mensagem_analisando() -> str:
    return random.choice(MENSAGENS_ANALISE)


def mensagem_concluida() -> str:
    return random.choice(MENSAGENS_CONCLUSAO)


def mensagem_erro() -> str:
    return random.choice(MENSAGENS_ERRO)
