from __future__ import annotations

import sys

from PySide6.QtCore import QEasingCurve, QPropertyAnimation
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from carcara.ui.main_window import JanelaPrincipal
from carcara.ui.splash import SplashCarcara
from carcara.ui.styles import ESTILO_GLOBAL


def executar() -> int:
    aplicativo = QApplication(sys.argv)

    aplicativo.setApplicationName("CarcaráAV")
    aplicativo.setApplicationVersion("0.1.0")
    aplicativo.setOrganizationName("CarcaráAV")

    fonte_principal = QFont("Alegreya Sans")
    fonte_principal.setPointSize(11)

    aplicativo.setFont(fonte_principal)
    aplicativo.setStyleSheet(ESTILO_GLOBAL)

    janela = JanelaPrincipal()
    janela.setWindowOpacity(0.0)

    splash = SplashCarcara()

    def abrir_janela_principal() -> None:
        janela.show()

        animacao = QPropertyAnimation(
            janela,
            b"windowOpacity",
            janela,
        )
        animacao.setDuration(650)
        animacao.setStartValue(0.0)
        animacao.setEndValue(1.0)
        animacao.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )
        animacao.start()

        janela._animacao_abertura = animacao

    splash.concluida.connect(abrir_janela_principal)
    splash.iniciar()

    aplicativo._splash_carcara = splash
    aplicativo._janela_carcara = janela

    return aplicativo.exec()
