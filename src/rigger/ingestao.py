"""Leitura de materiais de curso e normas da base de conhecimento.

Formatos suportados: .md, .txt, .pdf, .docx
"""

from __future__ import annotations

from pathlib import Path

EXTENSOES_SUPORTADAS = {".md", ".txt", ".pdf", ".docx"}


def _ler_pdf(caminho: Path) -> str:
    from pypdf import PdfReader

    leitor = PdfReader(str(caminho))
    paginas = [(pagina.extract_text() or "") for pagina in leitor.pages]
    return "\n".join(paginas)


def _ler_docx(caminho: Path) -> str:
    from docx import Document

    documento = Document(str(caminho))
    return "\n".join(paragrafo.text for paragrafo in documento.paragraphs)


def ler_arquivo(caminho: Path) -> str:
    """Lê um único arquivo e devolve seu texto."""
    sufixo = caminho.suffix.lower()
    if sufixo in {".md", ".txt"}:
        return caminho.read_text(encoding="utf-8", errors="ignore")
    if sufixo == ".pdf":
        return _ler_pdf(caminho)
    if sufixo == ".docx":
        return _ler_docx(caminho)
    raise ValueError(f"Formato não suportado: {caminho.name}")


def ler_caminho(caminho: Path) -> str:
    """Lê um arquivo ou todos os arquivos suportados de um diretório (recursivo).

    Cada arquivo é precedido por um cabeçalho com seu nome, para o modelo saber a origem.
    """
    if caminho.is_file():
        return f"### Arquivo: {caminho.name}\n\n{ler_arquivo(caminho)}"

    if not caminho.exists():
        raise FileNotFoundError(f"Caminho não encontrado: {caminho}")

    partes: list[str] = []
    for arquivo in sorted(caminho.rglob("*")):
        if arquivo.is_file() and arquivo.suffix.lower() in EXTENSOES_SUPORTADAS:
            try:
                texto = ler_arquivo(arquivo)
            except Exception as erro:  # noqa: BLE001 - registra e segue
                texto = f"[Falha ao ler {arquivo.name}: {erro}]"
            partes.append(f"### Arquivo: {arquivo.relative_to(caminho)}\n\n{texto}")

    if not partes:
        raise FileNotFoundError(
            f"Nenhum arquivo suportado ({', '.join(sorted(EXTENSOES_SUPORTADAS))}) "
            f"encontrado em: {caminho}"
        )
    return "\n\n---\n\n".join(partes)


def ler_normas(dir_normas: Path) -> str:
    """Lê toda a pasta de normas. Devolve string vazia se a pasta não existir/estiver vazia."""
    try:
        return ler_caminho(dir_normas)
    except FileNotFoundError:
        return ""
