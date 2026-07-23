"""
Assinaturas conhecidas de formatos de arquivos.
"""

ASSINATURAS = {
    b"%PDF": "PDF",
    b"\x89PNG\r\n\x1a\n": "PNG",
    b"\xff\xd8\xff": "JPEG",
    b"PK\x03\x04": "ZIP",
    b"MZ": "PE",
    b"\x7fELF": "ELF",
}
