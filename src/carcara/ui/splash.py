from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import QColor
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class SplashCarcara(QWidget):
    concluida = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("splashCarcara")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.SplashScreen
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True,
        )

        self.setFixedSize(620, 440)
        self.setWindowOpacity(0.0)

        self._construir_interface()
        self._criar_animacoes()

    def _construir_interface(self) -> None:
        painel = QWidget()
        painel.setObjectName("painelSplash")
        painel.setStyleSheet(
            """
            QWidget#painelSplash {
                background-color: #121517;
                border: 1px solid #4A3D26;
                border-radius: 28px;
            }

            QLabel#marcaSplash {
                color: #D3A84D;
                font-family: "Alegreya Sans SC";
                font-size: 38px;
                font-weight: 800;
                letter-spacing: 4px;
            }

            QLabel#conceitosSplash {
                color: #AFA79A;
                font-family: "Alegreya Sans SC";
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 3px;
            }

            QLabel#sloganSplash {
                color: #F2EDE3;
                font-family: "Alegreya Sans";
                font-size: 18px;
                font-style: italic;
            }

            QLabel#versaoSplash {
                color: #746B5D;
                font-family: "Alegreya Sans";
                font-size: 13px;
            }

            QLabel#estadoSplash {
                color: #C8B17D;
                font-family: "Alegreya Sans";
                font-size: 14px;
            }
            """
        )

        sombra = QGraphicsDropShadowEffect(self)
        sombra.setBlurRadius(48)
        sombra.setOffset(0, 10)
        sombra.setColor(QColor(0, 0, 0, 165))
        painel.setGraphicsEffect(sombra)

        caminho_logo = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "carcara.svg"
        )

        logo = QSvgWidget(str(caminho_logo))
        logo.setFixedSize(128, 128)

        linha_logo = QHBoxLayout()
        linha_logo.addStretch()
        linha_logo.addWidget(logo)
        linha_logo.addStretch()

        titulo = QLabel("CARCARÁAV")
        titulo.setObjectName("marcaSplash")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        conceitos = QLabel("OBSERVAÇÃO • INTEGRIDADE • ESCOLHA")
        conceitos.setObjectName("conceitosSplash")
        conceitos.setAlignment(Qt.AlignmentFlag.AlignCenter)

        slogan = QLabel("Aqui, quem decide é você.")
        slogan.setObjectName("sloganSplash")
        slogan.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.estado = QLabel("Preparando o primeiro voo...")
        self.estado.setObjectName("estadoSplash")
        self.estado.setAlignment(Qt.AlignmentFlag.AlignCenter)

        versao = QLabel("v0.1 — Primeiro Voo")
        versao.setObjectName("versaoSplash")
        versao.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout_painel = QVBoxLayout(painel)
        layout_painel.setContentsMargins(48, 36, 48, 34)
        layout_painel.setSpacing(9)

        layout_painel.addLayout(linha_logo)
        layout_painel.addSpacing(4)
        layout_painel.addWidget(titulo)
        layout_painel.addWidget(conceitos)
        layout_painel.addSpacing(14)
        layout_painel.addWidget(slogan)
        layout_painel.addStretch()
        layout_painel.addWidget(self.estado)
        layout_painel.addWidget(versao)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.addWidget(painel)

    def _criar_animacoes(self) -> None:
        self.animacao_entrada = QPropertyAnimation(
            self,
            b"windowOpacity",
        )
        self.animacao_entrada.setDuration(650)
        self.animacao_entrada.setStartValue(0.0)
        self.animacao_entrada.setEndValue(1.0)
        self.animacao_entrada.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        self.animacao_saida = QPropertyAnimation(
            self,
            b"windowOpacity",
        )
        self.animacao_saida.setDuration(550)
        self.animacao_saida.setStartValue(1.0)
        self.animacao_saida.setEndValue(0.0)
        self.animacao_saida.setEasingCurve(
            QEasingCurve.Type.InCubic
        )
        self.animacao_saida.finished.connect(
            self._finalizar
        )

        self.grupo = QSequentialAnimationGroup(self)
        self.grupo.addAnimation(self.animacao_entrada)

    def iniciar(self) -> None:
        self.show()

        tela = self.screen()

        if tela is not None:
            centro = tela.availableGeometry().center()
            geometria = self.frameGeometry()
            geometria.moveCenter(centro)
            self.move(geometria.topLeft())

        self.grupo.start()

        QTimer.singleShot(
            700,
            lambda: self.estado.setText(
                "Inicializando mecanismos..."
            ),
        )

        QTimer.singleShot(
            1250,
            lambda: self.estado.setText(
                "Observando o horizonte..."
            ),
        )

        QTimer.singleShot(
            1900,
            self.animacao_saida.start,
        )

    def _finalizar(self) -> None:
        self.hide()
        self.concluida.emit()
