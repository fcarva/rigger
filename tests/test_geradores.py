"""Testes dos geradores de arquivo (não exigem API).

Validam que, dados modelos preenchidos, os arquivos .pptx e .docx são criados.
"""

from __future__ import annotations

from pathlib import Path

from rigger.modelos import (
    Acessorio,
    ApreciacaoRisco,
    ChecklistInspecao,
    ItemChecklist,
    ItemRisco,
    Modulo,
    PlanoIcamento,
    Responsavel,
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


def _plano_exemplo() -> PlanoIcamento:
    return PlanoIcamento(
        obra="Obra X",
        descricao_carga="Viga metálica",
        peso_carga="12 t",
        equipamento="Guindaste móvel 50 t",
        acessorios=[Acessorio(tipo="Cinta têxtil", capacidade="5 t", quantidade="2")],
        sequencia_operacao=["Isolar área", "Inspecionar acessórios", "Içar"],
        riscos_criticos=["Queda da carga"],
        criterios_seguranca=["Vento máx. 10 m/s"],
        responsaveis=[Responsavel(funcao="Operador", atribuicao="Operar o guindaste")],
        normas_referencia=["NR-11", "ABNT NBR 16270"],
    )


def _checklist_exemplo() -> ChecklistInspecao:
    return ChecklistInspecao(
        acessorio="Cabo de aço",
        periodicidade="Pré-uso e periódica",
        itens=[
            ItemChecklist(
                item="Rompimento de pernas/fios",
                criterio="Dentro do limite da norma",
                referencia="ABNT NBR ISO 4309",
            )
        ],
        criterios_descarte=["Amassamento severo"],
        normas_referencia=["ABNT NBR ISO 4309"],
    )


def test_gerar_docx_plano(tmp_path: Path) -> None:
    from rigger.geradores.docx_builder import gerar_docx_plano

    caminho = gerar_docx_plano(_plano_exemplo(), tmp_path / "plano.docx")
    assert caminho.exists() and caminho.stat().st_size > 0


def test_gerar_docx_checklist(tmp_path: Path) -> None:
    from rigger.geradores.docx_builder import gerar_docx_checklist

    caminho = gerar_docx_checklist(_checklist_exemplo(), tmp_path / "checklist.docx")
    assert caminho.exists() and caminho.stat().st_size > 0
