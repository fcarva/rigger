"""Testes dos geradores de arquivo (não exigem API).

Validam que, dados modelos preenchidos, os arquivos .pptx e .docx são criados.
"""

from __future__ import annotations

from pathlib import Path

from rigger.modelos import (
    ApreciacaoRisco,
    ItemRisco,
    Modulo,
    Slide,
    Treinamento,
)


def _treinamento_exemplo() -> Treinamento:
    return Treinamento(
        titulo="Içamento Seguro de Cargas",
        publico_alvo="Operadores e sinaleiros",
        carga_horaria="8 horas",
        objetivos=["Operar com segurança", "Inspecionar acessórios"],
        normas_referencia=["NR-11", "ABNT NBR ISO 12100"],
        modulos=[
            Modulo(
                titulo="Fundamentos",
                objetivo="Entender conceitos básicos",
                slides=[
                    Slide(
                        titulo="O que é içamento",
                        topicos=["Definição", "Equipamentos", "Riscos"],
                        notas_apresentador="Explicar com exemplos do dia a dia.",
                    )
                ],
            )
        ],
        avaliacao=["Cite três acessórios de içamento."],
    )


def _apr_exemplo() -> ApreciacaoRisco:
    return ApreciacaoRisco(
        atividade="Içamento de viga metálica",
        local="Obra X",
        equipe=["Operador", "Sinaleiro"],
        normas_referencia=["NR-11", "NR-12"],
        itens=[
            ItemRisco(
                etapa="Lingada",
                perigo="Queda da carga",
                danos_possiveis=["Lesão grave", "Morte"],
                probabilidade=3,
                severidade=5,
                medidas_controle=["Inspecionar cintas", "Isolar área"],
                responsavel="Supervisor",
            )
        ],
        recomendacoes_gerais=["Verificar previsão de vento."],
    )


def test_classificacao_risco() -> None:
    item = _apr_exemplo().itens[0]
    assert item.risco == 15
    assert item.classificacao == "Crítico"


def test_gerar_pptx(tmp_path: Path) -> None:
    from rigger.geradores.pptx_builder import gerar_pptx

    destino = tmp_path / "treino.pptx"
    caminho = gerar_pptx(_treinamento_exemplo(), destino)
    assert caminho.exists()
    assert caminho.stat().st_size > 0


def test_gerar_docx(tmp_path: Path) -> None:
    from rigger.geradores.docx_builder import gerar_docx

    destino = tmp_path / "apr.docx"
    caminho = gerar_docx(_apr_exemplo(), destino)
    assert caminho.exists()
    assert caminho.stat().st_size > 0
