"""Orquestra a geração de um treinamento: material -> Claude -> PPTX."""

from __future__ import annotations

from pathlib import Path

from ..cliente_claude import ClienteClaude
from ..config import Config
from ..ingestao import ler_caminho, ler_normas
from ..modelos import Treinamento
from ..prompts import INSTRUCOES_TREINAMENTO
from .pptx_builder import gerar_pptx


def gerar_treinamento(
    *,
    material: Path,
    tema: str,
    publico: str = "operadores, sinaleiros e amarradores",
    saida: Path | None = None,
    config: Config | None = None,
    cliente: ClienteClaude | None = None,
) -> tuple[Treinamento, Path]:
    """Gera o treinamento estruturado e o arquivo .pptx.

    Devolve a tupla (modelo, caminho_do_pptx).
    """
    config = config or Config()
    cliente = cliente or ClienteClaude(config)

    texto_material = ler_caminho(material)
    normas = ler_normas(config.dir_normas)

    tarefa = (
        f"Gere um treinamento de içamento de carga sobre: {tema}.\n"
        f"Público-alvo: {publico}.\n"
        "Estruture em módulos e slides conforme as diretrizes."
    )

    treinamento = cliente.gerar(
        instrucoes=INSTRUCOES_TREINAMENTO,
        normas=normas,
        material=texto_material,
        tarefa=tarefa,
        modelo_saida=Treinamento,
    )

    if saida is None:
        config.garantir_saidas()
        saida = config.dir_saidas / "treinamento_icamento.pptx"

    caminho = gerar_pptx(treinamento, saida)
    return treinamento, caminho
