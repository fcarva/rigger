"""Monta um documento Word (.docx) a partir de uma `ApreciacaoRisco`."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt

from ..modelos import ApreciacaoRisco, ItemRisco

# Cores de fundo (hex) por classificação de risco.
_CORES_RISCO = {
    "Baixo": "C6EFCE",
    "Médio": "FFEB9C",
    "Alto": "FFC7A0",
    "Crítico": "FF7C80",
}


def _sombrear_celula(celula, cor_hex: str) -> None:
    """Define a cor de fundo de uma célula da tabela."""
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), cor_hex)
    celula._tc.get_or_add_tcPr().append(shd)


def _linha_info(documento, rotulo: str, valor: str) -> None:
    paragrafo = documento.add_paragraph()
    run = paragrafo.add_run(f"{rotulo}: ")
    run.bold = True
    paragrafo.add_run(valor)


def gerar_docx(apr: ApreciacaoRisco, caminho_saida: Path) -> Path:
    """Gera o .docx da apreciação de risco e devolve o caminho do arquivo."""
    documento = Document()

    titulo = documento.add_heading("Apreciação de Risco — Içamento de Carga", level=0)
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Cabeçalho de identificação
    _linha_info(documento, "Atividade", apr.atividade)
    if apr.local:
        _linha_info(documento, "Local", apr.local)
    if apr.equipe:
        _linha_info(documento, "Equipe", ", ".join(apr.equipe))
    if apr.normas_referencia:
        _linha_info(documento, "Normas de referência", ", ".join(apr.normas_referencia))

    documento.add_paragraph()

    # Tabela de riscos
    colunas = [
        "Etapa",
        "Perigo",
        "Danos possíveis",
        "P",
        "S",
        "Risco",
        "Classificação",
        "Medidas de controle",
        "Responsável",
    ]
    tabela = documento.add_table(rows=1, cols=len(colunas))
    tabela.style = "Light Grid Accent 1"

    for celula, texto in zip(tabela.rows[0].cells, colunas):
        celula.paragraphs[0].add_run(texto).bold = True

    for item in apr.itens:
        celulas = tabela.add_row().cells
        celulas[0].text = item.etapa
        celulas[1].text = item.perigo
        celulas[2].text = "\n".join(f"• {d}" for d in item.danos_possiveis)
        celulas[3].text = str(item.probabilidade)
        celulas[4].text = str(item.severidade)
        celulas[5].text = str(item.risco)
        celulas[6].text = item.classificacao
        celulas[7].text = "\n".join(f"• {m}" for m in item.medidas_controle)
        celulas[8].text = item.responsavel
        _sombrear_celula(celulas[6], _CORES_RISCO.get(item.classificacao, "FFFFFF"))

    # Recomendações gerais
    if apr.recomendacoes_gerais:
        documento.add_heading("Recomendações gerais", level=1)
        for rec in apr.recomendacoes_gerais:
            documento.add_paragraph(rec, style="List Bullet")

    # Legenda da matriz de risco
    documento.add_heading("Legenda — Matriz de risco (P × S, escala 1–5)", level=2)
    legenda = (
        "Baixo (1–4) • Médio (5–9) • Alto (10–14) • Crítico (15–25). "
        "P = probabilidade, S = severidade."
    )
    documento.add_paragraph(legenda).runs[0].font.size = Pt(9)

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    documento.save(str(caminho_saida))
    return caminho_saida


__all__ = ["gerar_docx", "ItemRisco"]
