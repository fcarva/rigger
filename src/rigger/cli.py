"""Interface de linha de comando do agente Rigger.

Exemplos:
    rigger treinamento --tema "Operação segura de guindaste móvel"
    rigger apreciacao --atividade "Içamento de viga metálica com guindaste de 50 t"
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from .config import Config

app = typer.Typer(
    add_completion=False,
    help="Transforma material de curso de içamento de carga em treinamentos e apreciações de risco.",
)


@app.command()
def treinamento(
    tema: str = typer.Option(..., "--tema", "-t", help="Tema/foco do treinamento."),
    material: Optional[Path] = typer.Option(
        None, "--material", "-m", help="Arquivo ou pasta de material. Padrão: base_conhecimento/cursos."
    ),
    publico: str = typer.Option(
        "operadores, sinaleiros e amarradores", "--publico", "-p", help="Público-alvo."
    ),
    saida: Optional[Path] = typer.Option(None, "--saida", "-o", help="Caminho do .pptx de saída."),
) -> None:
    """Gera um treinamento (.pptx) a partir do material e do tema."""
    from .geradores.treinamento import gerar_treinamento

    config = Config()
    material = material or config.dir_cursos

    typer.echo(f"Gerando treinamento sobre: {tema} ...")
    treino, caminho = gerar_treinamento(
        material=material, tema=tema, publico=publico, saida=saida, config=config
    )
    typer.secho(f"OK: {len(treino.modulos)} módulo(s) gerado(s).", fg=typer.colors.GREEN)
    typer.secho(f"Arquivo: {caminho}", fg=typer.colors.GREEN)


@app.command()
def transcrever(
    material: Path = typer.Option(..., "--material", "-m", help="PPTX de slides em imagem a transcrever."),
    lote: int = typer.Option(6, "--lote", help="Slides por chamada à API (controla custo/velocidade)."),
    saida: Optional[Path] = typer.Option(
        None, "--saida", "-o", help="Caminho do .md de saída. Padrão: ao lado do PPTX."
    ),
) -> None:
    """Transcreve um PPTX de slides-imagem para texto (Markdown) via visão da Claude."""
    from .visao import transcrever_pptx

    config = Config()

    def _progresso(feitos: int, total: int) -> None:
        typer.echo(f"  transcrevendo... {feitos}/{total} slides")

    typer.echo(f"Transcrevendo {material.name} (visão da Claude) ...")
    _, caminho = transcrever_pptx(material, lote=lote, destino=saida, config=config, progresso=_progresso)
    typer.secho(f"Transcrição salva em: {caminho}", fg=typer.colors.GREEN)
    typer.echo("Agora gere o treinamento apontando --material para esse arquivo .md.")


@app.command()
def apreciacao(
    atividade: str = typer.Option(..., "--atividade", "-a", help="Atividade a ser analisada."),
    material: Optional[Path] = typer.Option(
        None, "--material", "-m", help="Arquivo ou pasta de material de apoio (opcional)."
    ),
    local: str = typer.Option("", "--local", "-l", help="Local/contexto da operação."),
    saida: Optional[Path] = typer.Option(None, "--saida", "-o", help="Caminho do .docx de saída."),
) -> None:
    """Gera uma apreciação de risco (.docx) para a atividade informada."""
    from .geradores.apreciacao_risco import gerar_apreciacao

    config = Config()

    typer.echo(f"Gerando apreciação de risco para: {atividade} ...")
    apr, caminho = gerar_apreciacao(
        atividade=atividade, material=material, local=local, saida=saida, config=config
    )
    typer.secho(f"OK: {len(apr.itens)} item(ns) de risco identificado(s).", fg=typer.colors.GREEN)
    typer.secho(f"Arquivo: {caminho}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
