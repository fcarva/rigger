"""Orquestra a geração de uma apreciação de risco: material -> Claude -> Word."""

from __future__ import annotations

from pathlib import Path

from ..cliente_claude import ClienteClaude
from ..config import Config
from ..ingestao import ler_caminho, ler_normas
from ..modelos import ApreciacaoRisco
from ..prompts import INSTRUCOES_APRECIACAO
from .docx_builder import gerar_docx


def gerar_apreciacao(
    *,
    atividade: str,
    material: Path | None = None,
    local: str = "",
    saida: Path | None = None,
    config: Config | None = None,
    cliente: ClienteClaude | None = None,
) -> tuple[ApreciacaoRisco, Path]:
    """Gera a apreciação de risco estruturada e o arquivo .docx.

    Devolve a tupla (modelo, caminho_do_docx).
    """
    config = config or Config()
    cliente = cliente or ClienteClaude(config)

    texto_material = ler_caminho(material) if material else "(Sem material adicional fornecido.)"
    normas = ler_normas(config.dir_normas)

    tarefa = (
        f"Elabore a apreciação de risco da atividade: {atividade}.\n"
        f"Local/contexto: {local or 'não especificado'}.\n"
        "Decomponha em etapas e preencha os itens conforme as diretrizes."
    )

    apr = cliente.gerar(
        instrucoes=INSTRUCOES_APRECIACAO,
        normas=normas,
        material=texto_material,
        tarefa=tarefa,
        modelo_saida=ApreciacaoRisco,
    )

    if saida is None:
        config.garantir_saidas()
        saida = config.dir_saidas / "apreciacao_risco_icamento.docx"

    caminho = gerar_docx(apr, saida)
    return apr, caminho
