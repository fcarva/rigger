"""Orquestra a geração de um checklist de inspeção: -> Claude -> Word."""

from __future__ import annotations

from pathlib import Path

from ..cliente_claude import ClienteClaude
from ..config import Config
from ..ingestao import ler_caminho, ler_normas
from ..modelos import ChecklistInspecao
from ..prompts import INSTRUCOES_CHECKLIST
from .docx_builder import gerar_docx_checklist


def gerar_checklist(
    *,
    acessorio: str,
    material: Path | None = None,
    saida: Path | None = None,
    config: Config | None = None,
    cliente: ClienteClaude | None = None,
) -> tuple[ChecklistInspecao, Path]:
    """Gera o checklist de inspeção estruturado e o arquivo .docx.

    Devolve a tupla (modelo, caminho_do_docx).
    """
    config = config or Config()
    cliente = cliente or ClienteClaude(config)

    texto_material = ler_caminho(material) if material else "(Sem material adicional fornecido.)"
    normas = ler_normas(config.dir_normas)

    tarefa = (
        f"Elabore o checklist de inspeção para o acessório: {acessorio}.\n"
        "Liste os pontos de inspeção, critérios e referências conforme as diretrizes."
    )

    checklist = cliente.gerar(
        instrucoes=INSTRUCOES_CHECKLIST,
        normas=normas,
        material=texto_material,
        tarefa=tarefa,
        modelo_saida=ChecklistInspecao,
    )

    if saida is None:
        config.garantir_saidas()
        nome = "checklist_" + acessorio.lower().replace(" ", "_")[:30] + ".docx"
        saida = config.dir_saidas / nome

    caminho = gerar_docx_checklist(checklist, saida)
    return checklist, caminho
