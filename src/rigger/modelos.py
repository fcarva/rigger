"""Modelos de dados (Pydantic) que estruturam a saída do agente.

Estes esquemas são usados com `messages.parse()` (structured outputs) para garantir
que a Claude devolva os dados no formato que os geradores de PPTX/Word esperam.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Treinamento
# ---------------------------------------------------------------------------


class Slide(BaseModel):
    """Um slide do treinamento."""

    titulo: str = Field(description="Título curto do slide.")
    topicos: list[str] = Field(
        description="Tópicos em bullet points, objetivos e didáticos (3 a 6 itens)."
    )
    notas_apresentador: str = Field(
        default="",
        description="Notas para quem ministra: explicação, exemplos, perguntas para a turma.",
    )


class Modulo(BaseModel):
    """Um módulo (capítulo) do treinamento, composto por slides."""

    titulo: str = Field(description="Título do módulo.")
    objetivo: str = Field(description="Objetivo de aprendizagem do módulo.")
    slides: list[Slide] = Field(description="Slides que compõem o módulo.")


class Treinamento(BaseModel):
    """Estrutura completa de um treinamento de içamento de carga."""

    titulo: str
    publico_alvo: str = Field(description="A quem se destina (ex.: operadores, sinaleiros, riggers).")
    carga_horaria: str = Field(description="Carga horária estimada (ex.: '8 horas').")
    objetivos: list[str] = Field(description="Objetivos gerais do treinamento.")
    pre_requisitos: list[str] = Field(default_factory=list)
    normas_referencia: list[str] = Field(
        description="NRs e normas ABNT citadas (ex.: 'NR-11', 'ABNT NBR ISO 12100')."
    )
    modulos: list[Modulo]
    avaliacao: list[str] = Field(
        default_factory=list,
        description="Perguntas de avaliação/verificação de aprendizagem.",
    )


# ---------------------------------------------------------------------------
# Apreciação de risco
# ---------------------------------------------------------------------------

# Faixas da matriz de risco (probabilidade × severidade, escala 1–5).
_FAIXAS_RISCO = [
    (4, "Baixo"),
    (9, "Médio"),
    (14, "Alto"),
    (25, "Crítico"),
]


class ItemRisco(BaseModel):
    """Uma linha da apreciação de risco: etapa, perigo, avaliação e controles."""

    etapa: str = Field(description="Etapa ou tarefa da operação de içamento.")
    perigo: str = Field(description="Perigo identificado.")
    danos_possiveis: list[str] = Field(description="Danos/consequências possíveis.")
    probabilidade: int = Field(description="Probabilidade de ocorrência, escala de 1 (rara) a 5 (frequente).")
    severidade: int = Field(description="Severidade do dano, escala de 1 (leve) a 5 (catastrófica).")
    medidas_controle: list[str] = Field(
        description="Medidas de controle na hierarquia: eliminação, engenharia, administrativas, EPI."
    )
    responsavel: str = Field(default="", description="Responsável pela implementação do controle.")

    @property
    def risco(self) -> int:
        """Valor do risco = probabilidade × severidade."""
        return self.probabilidade * self.severidade

    @property
    def classificacao(self) -> str:
        """Classificação textual do risco conforme a matriz."""
        valor = self.risco
        for limite, rotulo in _FAIXAS_RISCO:
            if valor <= limite:
                return rotulo
        return "Crítico"


class ApreciacaoRisco(BaseModel):
    """Apreciação de risco (APR) de uma operação de içamento de carga."""

    atividade: str = Field(description="Atividade analisada.")
    local: str = Field(default="", description="Local/obra onde ocorre a operação.")
    equipe: list[str] = Field(
        default_factory=list, description="Funções envolvidas (operador, sinaleiro, amarrador, etc.)."
    )
    normas_referencia: list[str]
    itens: list[ItemRisco]
    recomendacoes_gerais: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Plano de içamento (rigging plan)
# ---------------------------------------------------------------------------


class Acessorio(BaseModel):
    """Um acessório de içamento usado no plano (cinta, cabo, manilha, etc.)."""

    tipo: str = Field(description="Tipo do acessório (cinta têxtil, cabo de aço, manilha, gancho, balancim).")
    capacidade: str = Field(description="Capacidade de carga / WLL (ex.: '5 t').")
    quantidade: str = Field(default="", description="Quantidade utilizada.")
    observacao: str = Field(default="", description="Observações (ângulo, comprimento, proteção de quina).")


class Responsavel(BaseModel):
    """Função e atribuição de um responsável na operação."""

    funcao: str = Field(description="Função (operador, sinaleiro, amarrador, supervisor, resp. técnico).")
    atribuicao: str = Field(description="Atribuição/responsabilidade na operação.")


class PlanoIcamento(BaseModel):
    """Plano de içamento (rigging plan) de uma operação."""

    obra: str = Field(default="", description="Obra/cliente/local.")
    descricao_carga: str = Field(description="Descrição da carga a ser içada.")
    peso_carga: str = Field(description="Peso da carga (ex.: '12 t').")
    dimensoes_carga: str = Field(default="", description="Dimensões aproximadas da carga.")
    centro_gravidade: str = Field(default="", description="Considerações sobre o centro de gravidade.")
    equipamento: str = Field(description="Equipamento de içamento (tipo/modelo do guindaste).")
    capacidade_equipamento: str = Field(default="", description="Capacidade nominal do equipamento.")
    raio_operacao: str = Field(default="", description="Raio de operação previsto.")
    comprimento_lanca: str = Field(default="", description="Comprimento de lança previsto.")
    percentual_utilizacao: str = Field(
        default="", description="Percentual de utilização da tabela de carga (ex.: '75%')."
    )
    acessorios: list[Acessorio] = Field(description="Acessórios de içamento previstos.")
    sequencia_operacao: list[str] = Field(description="Passo a passo da operação, em ordem.")
    riscos_criticos: list[str] = Field(description="Riscos críticos da operação.")
    criterios_seguranca: list[str] = Field(
        description="Critérios/limites de segurança (vento máx., isolamento, solo, redes elétricas)."
    )
    responsaveis: list[Responsavel] = Field(default_factory=list)
    normas_referencia: list[str]


# ---------------------------------------------------------------------------
# Checklist de inspeção de acessórios
# ---------------------------------------------------------------------------


class ItemChecklist(BaseModel):
    """Um item a verificar na inspeção de um acessório."""

    item: str = Field(description="O que verificar (ponto de inspeção).")
    criterio: str = Field(description="Critério de aprovação/rejeição.")
    referencia: str = Field(default="", description="Norma/cláusula de referência, se houver.")


class ChecklistInspecao(BaseModel):
    """Checklist de inspeção de um acessório de içamento."""

    acessorio: str = Field(description="Acessório inspecionado (ex.: cabo de aço, cinta têxtil, manilha).")
    periodicidade: str = Field(default="", description="Quando inspecionar (pré-uso, periódica, etc.).")
    itens: list[ItemChecklist] = Field(description="Pontos de inspeção.")
    criterios_descarte: list[str] = Field(
        default_factory=list, description="Critérios objetivos de descarte do acessório."
    )
    normas_referencia: list[str]
