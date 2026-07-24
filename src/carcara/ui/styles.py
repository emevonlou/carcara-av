ESTILO_GLOBAL = """
QWidget {
    background-color: #121517;
    color: #F2EDE3;
    font-family: "Alegreya Sans", "Noto Sans", sans-serif;
    font-size: 15px;
}

QMainWindow {
    background-color: #121517;
}

QFrame#cabecalho {
    background-color: #191D20;
    border: 1px solid #2B3135;
    border-radius: 22px;
}

QFrame#cartao {
    background-color: #1A1F22;
    border: 1px solid #30373C;
    border-radius: 20px;
}

QFrame#comentario {
    background-color: #171B1D;
    border: 1px solid #4A3D26;
    border-radius: 17px;
}

QLabel#marca {
    color: #D1A34A;
    font-family: "Alegreya Sans SC", "Alegreya Sans", sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 4px;
}

QLabel#titulo {
    color: #FFF9EC;
    font-family: "Alegreya Sans SC", "Alegreya Sans", sans-serif;
    font-size: 40px;
    font-weight: 800;
    letter-spacing: 2px;
}

QLabel#slogan {
    color: #CAC3B8;
    font-size: 18px;
    font-style: italic;
    font-weight: 400;
}

QLabel#estadoPrincipal {
    color: #FFF9EC;
    font-size: 26px;
    font-weight: 700;
}

QLabel#textoSecundario {
    color: #A8A39B;
    font-size: 15px;
}

QLabel#rotulo {
    color: #9A958D;
    font-family: "Alegreya Sans SC", "Alegreya Sans", sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
}

QLabel#valor {
    color: #ECE7DE;
    font-size: 16px;
}

QLabel#hash {
    color: #DCB968;
    font-family: "JetBrains Mono", "DejaVu Sans Mono", monospace;
    font-size: 12px;
}

QLabel#falaCarcara {
    color: #DED8CF;
    font-size: 17px;
    font-style: italic;
}

QLabel#statusPronto {
    background-color: #20392E;
    color: #82D2A5;
    border: 1px solid #315E49;
    border-radius: 12px;
    padding: 6px 14px;
    font-family: "Alegreya Sans SC", "Alegreya Sans", sans-serif;
    font-weight: 700;
}

QLabel#statusAnalisando {
    background-color: #40351F;
    color: #E8C36E;
    border: 1px solid #68572D;
    border-radius: 12px;
    padding: 6px 14px;
    font-family: "Alegreya Sans SC", "Alegreya Sans", sans-serif;
    font-weight: 700;
}

QLabel#statusErro {
    background-color: #412528;
    color: #EF9298;
    border: 1px solid #74393E;
    border-radius: 12px;
    padding: 6px 14px;
    font-family: "Alegreya Sans SC", "Alegreya Sans", sans-serif;
    font-weight: 700;
}

QPushButton {
    min-height: 46px;
    padding: 0 24px;
    border-radius: 13px;
    font-size: 16px;
    font-weight: 700;
}

QPushButton#primario {
    background-color: #D0A348;
    color: #18130A;
    border: 1px solid #E0B75F;
}

QPushButton#primario:hover {
    background-color: #DFB75F;
}

QPushButton#primario:pressed {
    background-color: #B98C35;
}

QPushButton#secundario {
    background-color: #252B2F;
    color: #EEE9DF;
    border: 1px solid #41494E;
}

QPushButton#secundario:hover {
    background-color: #30373B;
    border-color: #666F74;
}

QPushButton:disabled {
    background-color: #25282A;
    color: #686D70;
    border: 1px solid #303436;
}

QProgressBar {
    min-height: 9px;
    max-height: 9px;
    background-color: #292F32;
    border: none;
    border-radius: 4px;
    color: transparent;
}

QProgressBar::chunk {
    background-color: #D0A348;
    border-radius: 4px;
}

QMessageBox {
    background-color: #191D20;
}

QToolTip {
    background-color: #252A2E;
    color: #F4EFE5;
    border: 1px solid #4A5156;
    padding: 7px;
}
"""
