from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from carcara.orquestracao import MotorDeAnalise, ResultadoAnalise
from carcara.scanner import ErroDeAnalise
from carcara.core.messages import (
    mensagem_analisando,
    mensagem_concluida,
    mensagem_erro,
    mensagem_inicial,
)


def formatar_tamanho(tamanho: int) -> str:
    unidades = ("B", "KiB", "MiB", "GiB", "TiB")
    valor = float(tamanho)

    for unidade in unidades:
        if valor < 1024 or unidade == unidades[-1]:
            if unidade == "B":
                return f"{int(valor)} {unidade}"

            return f"{valor:.2f} {unidade}"

        valor /= 1024

    return f"{tamanho} B"

class TrabalhadorAnalise(QThread):
    progresso = Signal(int)
    concluido = Signal(object)
    falhou = Signal(str)

    def __init__(self, caminho: Path) -> None:
        super().__init__()
        self.caminho = caminho

    def run(self) -> None:
        try:
            motor = MotorDeAnalise()

            resultado = motor.analisar(
                self.caminho,
                progresso=self.progresso.emit,
            )

            self.concluido.emit(resultado)

        except (ErroDeAnalise, OSError, ValueError) as erro:
            self.falhou.emit(str(erro))

        except Exception as erro:
            self.falhou.emit(
                f"Falha inesperada durante a análise: {erro}"
            )

class JanelaPrincipal(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.caminho_selecionado: Path | None = None
        self.trabalhador: TrabalhadorAnalise | None = None

        self.setWindowTitle("CarcaráAV")
        self.setMinimumSize(880, 650)
        self.resize(1040, 760)

        self._construir_interface()
        self._definir_estado_pronto()

    def _construir_interface(self) -> None:
        conteudo = QWidget()
        layout_principal = QVBoxLayout(conteudo)
        layout_principal.setContentsMargins(34, 30, 34, 30)
        layout_principal.setSpacing(18)

        layout_principal.addWidget(self._criar_cabecalho())
        layout_principal.addWidget(self._criar_area_principal(), 1)
        layout_principal.addWidget(self._criar_comentario())

        self.setCentralWidget(conteudo)

    def _criar_cabecalho(self) -> QFrame:
        quadro = QFrame()
        quadro.setObjectName("cabecalho")

        layout = QHBoxLayout(quadro)
        layout.setContentsMargins(28, 22, 28, 22)
        layout.setSpacing(16)

        caminho_logo = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "carcara.svg"
        )

        logo = QSvgWidget(str(caminho_logo))
        logo.setFixedSize(72, 72)

        layout.addWidget(logo)

        textos = QVBoxLayout()
        textos.setSpacing(3)

        marca = QLabel("OBSERVAÇÃO • INTEGRIDADE • ESCOLHA")
        marca.setObjectName("marca")

        titulo = QLabel("CarcaráAV")
        titulo.setObjectName("titulo")

        slogan = QLabel("Aqui, quem decide é você.")
        slogan.setObjectName("slogan")

        textos.addWidget(marca)
        textos.addWidget(titulo)
        textos.addWidget(slogan)

        layout.addLayout(textos)
        layout.addStretch()

        self.rotulo_status = QLabel("Pronto")
        self.rotulo_status.setObjectName("statusPronto")
        layout.addWidget(self.rotulo_status)

        return quadro

    def _criar_area_principal(self) -> QFrame:
        quadro = QFrame()
        quadro.setObjectName("cartao")

        layout = QVBoxLayout(quadro)
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(18)

        self.estado_principal = QLabel("O horizonte está à sua espera.")
        self.estado_principal.setObjectName("estadoPrincipal")

        self.instrucao = QLabel(
            "Selecione um arquivo para calcular seu SHA-256 "
            "e conhecer seus primeiros detalhes."
        )
        self.instrucao.setObjectName("textoSecundario")
        self.instrucao.setWordWrap(True)

        layout.addWidget(self.estado_principal)
        layout.addWidget(self.instrucao)

        botoes = QHBoxLayout()
        botoes.setSpacing(12)

        self.botao_selecionar = QPushButton("Selecionar arquivo")
        self.botao_selecionar.setObjectName("secundario")
        self.botao_selecionar.clicked.connect(self._selecionar_arquivo)

        self.botao_observar = QPushButton("Observar")
        self.botao_observar.setObjectName("primario")
        self.botao_observar.setEnabled(False)
        self.botao_observar.clicked.connect(self._iniciar_analise)

        botoes.addWidget(self.botao_selecionar)
        botoes.addWidget(self.botao_observar)
        botoes.addStretch()

        layout.addLayout(botoes)

        self.progresso = QProgressBar()
        self.progresso.setRange(0, 100)
        self.progresso.setValue(0)

        layout.addWidget(self.progresso)

        linha = QFrame()
        linha.setFrameShape(QFrame.Shape.HLine)
        linha.setStyleSheet("color: #30363D;")

        layout.addWidget(linha)
        layout.addLayout(self._criar_linha_detalhe("Arquivo", "arquivo"))
        layout.addLayout(self._criar_linha_detalhe("Caminho", "caminho"))
        layout.addLayout(self._criar_linha_detalhe("Tamanho", "tamanho"))
        layout.addLayout(self._criar_linha_detalhe("SHA-256", "sha256"))
        layout.addLayout(
            self._criar_linha_detalhe("Tipo real", "tipo_real")
        )
        layout.addLayout(
            self._criar_linha_detalhe("Evidências", "evidencias")
        )

        layout.addStretch()

        return quadro

    def _criar_linha_detalhe(
        self,
        texto_rotulo: str,
        atributo: str,
    ) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(18)

        rotulo = QLabel(texto_rotulo.upper())
        rotulo.setObjectName("rotulo")
        rotulo.setFixedWidth(95)

        valor = QLabel("—")
        valor.setObjectName("hash" if atributo == "sha256" else "valor")
        valor.setWordWrap(True)
        valor.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        setattr(self, f"valor_{atributo}", valor)

        layout.addWidget(rotulo)
        layout.addWidget(valor, 1)

        return layout

    def _criar_comentario(self) -> QFrame:
        quadro = QFrame()
        quadro.setObjectName("comentario")

        layout = QHBoxLayout(quadro)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)

        marcador = QLabel("CARCARÁ")
        marcador.setObjectName("marca")

        self.fala_caracara = QLabel(f"“{mensagem_inicial()}”")
        self.fala_caracara.setObjectName("falaCarcara")
        self.fala_caracara.setWordWrap(True)

        layout.addWidget(marcador)
        layout.addWidget(self.fala_caracara, 1)

        return quadro

    def _selecionar_arquivo(self) -> None:
        caminho, _ = QFileDialog.getOpenFileName(
            self,
            "Selecione um arquivo para observar",
            str(Path.home()),
            "Todos os arquivos (*)",
        )

        if not caminho:
            return

        self.caminho_selecionado = Path(caminho).resolve()
        tamanho = self.caminho_selecionado.stat().st_size

        self.valor_arquivo.setText(self.caminho_selecionado.name)
        self.valor_caminho.setText(str(self.caminho_selecionado))
        self.valor_tamanho.setText(formatar_tamanho(tamanho))
        self.valor_sha256.setText("Aguardando análise")
        self.valor_tipo_real.setText("Aguardando análise")
        self.valor_evidencias.setText("Aguardando análise")

        self.estado_principal.setText("Arquivo selecionado.")
        self.instrucao.setText(
            "O Carcará está pronto para calcular a identidade "
            "criptográfica deste arquivo."
        )
        self.progresso.setValue(0)
        self.botao_observar.setEnabled(True)

        self._definir_estado_pronto()
        self.fala_caracara.setText(
            "“Este arquivo resolveu chamar atenção.”"
        )

    def _iniciar_analise(self) -> None:
        if self.caminho_selecionado is None:
            return

        self.botao_selecionar.setEnabled(False)
        self.botao_observar.setEnabled(False)
        self.progresso.setValue(0)
        self.valor_sha256.setText("Calculando...")
        self.valor_tipo_real.setText("Identificando...")
        self.valor_evidencias.setText("Coletando...")

        self.estado_principal.setText("Observação em andamento.")
        self.instrucao.setText(
            "Lendo o arquivo em blocos para preservar memória "
            "e manter a interface responsiva."
        )
        self.fala_caracara.setText(f"“{mensagem_analisando()}”")

        self._definir_status("Observando", "statusAnalisando")

        self.trabalhador = TrabalhadorAnalise(
            self.caminho_selecionado
        )
        self.trabalhador.progresso.connect(self.progresso.setValue)
        self.trabalhador.concluido.connect(self._analise_concluida)
        self.trabalhador.falhou.connect(self._analise_falhou)
        self.trabalhador.finished.connect(
            self.trabalhador.deleteLater
        )
        self.trabalhador.start()

    def _analise_concluida(
        self,
        resultado: ResultadoAnalise,
    ) -> None:
        arquivo = resultado.arquivo

        self.valor_sha256.setText(
            arquivo.sha256 or "Não calculado"
        )
        self.valor_tipo_real.setText(
            arquivo.tipo_real or "DESCONHECIDO"
        )

        if resultado.possui_evidencias:
            texto_evidencias = "\n".join(
                f"[{evidencia.severidade}] "
                f"{evidencia.codigo}: "
                f"{evidencia.descricao}"
                for evidencia in resultado.evidencias
            )
        else:
            texto_evidencias = "Nenhuma evidência encontrada."

        self.valor_evidencias.setText(texto_evidencias)
        self.progresso.setValue(100)

        self.estado_principal.setText("Observação concluída.")
        self.instrucao.setText(
            "A identidade criptográfica, o tipo real e as "
            "evidências do arquivo foram reunidos."
        )
        self.fala_caracara.setText(
            f"“{mensagem_concluida()}”"
        )

        self.botao_selecionar.setEnabled(True)
        self.botao_observar.setEnabled(True)
        self._definir_estado_pronto()

        self.trabalhador = None


    def _analise_falhou(self, descricao: str) -> None:
        self.progresso.setValue(0)
        self.valor_sha256.setText("Não calculado")
        self.valor_tipo_real.setText("Não identificado")
        self.valor_evidencias.setText("Não coletadas")

        self.estado_principal.setText("A observação foi interrompida.")
        self.instrucao.setText(descricao)
        self.fala_caracara.setText(f"“{mensagem_erro()}”")

        self.botao_selecionar.setEnabled(True)
        self.botao_observar.setEnabled(True)
        self._definir_status("Atenção", "statusErro")

        QMessageBox.warning(
            self,
            "CarcaráAV",
            descricao,
        )

        self.trabalhador = None

    def _definir_estado_pronto(self) -> None:
        self._definir_status("Pronto", "statusPronto")

    def _definir_status(
        self,
        texto: str,
        nome_objeto: str,
    ) -> None:
        self.rotulo_status.setText(texto)
        self.rotulo_status.setObjectName(nome_objeto)

        self.rotulo_status.style().unpolish(self.rotulo_status)
        self.rotulo_status.style().polish(self.rotulo_status)
        self.rotulo_status.update()
