"""Configuração central do agente (chave de API, modelo, caminhos)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# Carrega variáveis de um arquivo .env, se existir.
# override=True: o .env tem prioridade sobre variáveis de ambiente já definidas
# (inclusive uma ANTHROPIC_API_KEY vazia herdada do shell), que é o que o usuário espera.
load_dotenv(override=True)

# Raiz do projeto = duas pastas acima de src/rigger/config.py
RAIZ_PROJETO = Path(__file__).resolve().parents[2]


@dataclass
class Config:
    """Reúne as configurações usadas pelo agente."""

    api_key: str | None = field(
        default_factory=lambda: (os.getenv("ANTHROPIC_API_KEY") or "").strip() or None
    )
    modelo: str = field(default_factory=lambda: os.getenv("RIGGER_MODELO", "claude-opus-4-8"))

    raiz: Path = RAIZ_PROJETO
    dir_normas: Path = RAIZ_PROJETO / "base_conhecimento" / "normas"
    dir_cursos: Path = RAIZ_PROJETO / "base_conhecimento" / "cursos"
    dir_saidas: Path = RAIZ_PROJETO / "saidas"

    def validar(self) -> None:
        """Garante que a chave de API está presente antes de chamar a API."""
        if not self.api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY não encontrada. Copie .env.example para .env "
                "e preencha a chave, ou exporte a variável de ambiente."
            )

    def garantir_saidas(self) -> Path:
        """Cria a pasta de saídas se necessário e devolve o caminho."""
        self.dir_saidas.mkdir(parents=True, exist_ok=True)
        return self.dir_saidas
