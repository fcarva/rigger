"""Cliente da API da Claude com saída estruturada e cache de prompt.

A base de normas é enviada como bloco de sistema com `cache_control`, de modo que
chamadas repetidas (vários treinamentos/APRs na mesma sessão) reaproveitem o cache
e fiquem mais baratas.
"""

from __future__ import annotations

from typing import TypeVar

import anthropic
from pydantic import BaseModel

from .config import Config
from .prompts import PERSONA

T = TypeVar("T", bound=BaseModel)


class ClienteClaude:
    """Encapsula as chamadas à API da Anthropic para o agente."""

    def __init__(self, config: Config | None = None) -> None:
        self.config = config or Config()
        self.config.validar()
        self._client = anthropic.Anthropic(api_key=self.config.api_key)

    def gerar(
        self,
        *,
        instrucoes: str,
        normas: str,
        material: str,
        tarefa: str,
        modelo_saida: type[T],
        max_tokens: int = 16000,
    ) -> T:
        """Gera uma saída estruturada (instância de `modelo_saida`).

        - `instrucoes`: instrução específica da tarefa (treinamento ou APR).
        - `normas`: texto da base de conhecimento (vai em bloco com cache).
        - `material`: material de curso fornecido pelo usuário.
        - `tarefa`: pedido final (ex.: tema, foco, público).
        """
        # Bloco estável (persona + normas) — fica em cache entre chamadas.
        bloco_estavel = PERSONA
        if normas.strip():
            bloco_estavel += "\n\n# Base de conhecimento — normas de referência\n\n" + normas

        system = [
            {"type": "text", "text": bloco_estavel, "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": instrucoes},
        ]

        conteudo_usuario = (
            f"# Material de curso fornecido\n\n{material}\n\n"
            f"# Pedido\n\n{tarefa}"
        )

        resposta = self._client.messages.parse(
            model=self.config.modelo,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": conteudo_usuario}],
            output_format=modelo_saida,
        )

        if resposta.parsed_output is None:
            motivo = resposta.stop_reason
            raise RuntimeError(
                f"A Claude não devolveu uma saída válida (stop_reason={motivo!r}). "
                "Tente reduzir o material, revisar o pedido ou aumentar max_tokens."
            )
        return resposta.parsed_output
