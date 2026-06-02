"""Orquestra a geração de um plano de içamento: material -> Claude -> Word."""

from __future__ import annotations

from pathlib import Path

from ..cliente_claude import ClienteClaude
from ..config import Config
from ..ingestao import ler_caminho, ler_normas
from ..modelos import PlanoIcamento
from ..prompts import INSTRUCOES_PLANO
from .docx_builder import gerar_docx_plano


def gerar_plano(
    *,
    operacao: str,
    material: Path | None = None,
    obra: str = "",
    saida: Path | None = None,
    config: Config | None = None,
    cliente: ClienteClaude | None = None,
) -> tuple[PlanoIcamento, Path]:
    """Gera o plano de içamento estruturado e o arquivo .docx.

    Devolve a tupla (modelo, caminho_do_docx).
    """
    config = config or Config()
    cliente = cliente or ClienteClaude(config)

    texto_material = ler_caminho(material) if material else "(Sem material adicional fornecido.)"
    normas = ler_normas(config.dir_normas)

    tarefa = (
        f"Elabore o plano de içamento para a operação: {operacao}.\n"
        f"Obra/local: {obra or 'não especificado'}.\n"
        "Preencha os campos conforme as diretrizes."
    )

    plano = cliente.gerar(
        instrucoes=INSTRUCOES_PLANO,
        normas=normas,
        material=texto_material,
        tarefa=tarefa,
        modelo_saida=PlanoIcamento,
    )

    if saida is None:
        config.garantir_saidas()
        saida = config.dir_saidas / "plano_icamento.docx"

    caminho = gerar_docx_plano(plano, saida)
    return plano, caminho
