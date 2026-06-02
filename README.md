# Rigger 🏗️

Agente que transforma material de curso de **içamento de carga** em **treinamentos**
(slides PowerPoint) e **apreciações de risco** (documentos Word), ancorado nas
**Normas Regulamentadoras** e nas normas **ABNT** aplicáveis.

É a base de um sistema de treinamento: você alimenta o repositório com material de
curso e normas, e o agente (API da Claude) produz os entregáveis.

## Como funciona

```
base_conhecimento/cursos/   ─┐
base_conhecimento/normas/   ─┤──►  Agente (Claude)  ──►  saidas/*.pptx  (treinamento)
   (material que você fornece)                            saidas/*.docx  (apreciação de risco)
```

1. **Base de conhecimento** — coloque apostilas, manuais e normas em
   [`base_conhecimento/`](base_conhecimento/) (`.md`, `.txt`, `.pdf`, `.docx`).
2. **Geração** — o agente lê o material + normas, extrai a estrutura via *structured
   outputs* da Claude e monta o arquivo final.
3. **Saída** — os arquivos ficam em [`saidas/`](saidas/).

## Instalação

Requer Python 3.10+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Configure a chave da API:

```powershell
Copy-Item .env.example .env
# edite o .env e cole sua ANTHROPIC_API_KEY
```

## Uso

```powershell
# Treinamento (gera um .pptx)
rigger treinamento --tema "Operação segura de guindaste móvel"

# Apreciação de risco (gera um .docx)
rigger apreciacao --atividade "Içamento de viga metálica com guindaste de 50 t" --local "Obra X"
```

Opções úteis:

| Comando        | Opção         | Descrição                                            |
|----------------|---------------|------------------------------------------------------|
| `treinamento`  | `--tema`      | Tema/foco do treinamento (obrigatório).              |
| `treinamento`  | `--material`  | Arquivo/pasta de material. Padrão: `cursos/`.        |
| `treinamento`  | `--publico`   | Público-alvo.                                        |
| `apreciacao`   | `--atividade` | Atividade analisada (obrigatório).                   |
| `apreciacao`   | `--material`  | Material de apoio (opcional).                        |
| ambos          | `--saida`     | Caminho do arquivo de saída.                         |

## Estrutura do projeto

```
rigger/
├── base_conhecimento/        # entrada: material de curso + normas
│   ├── cursos/
│   └── normas/icamento_carga.md
├── src/rigger/
│   ├── config.py             # chave de API, modelo, caminhos
│   ├── modelos.py            # esquemas Pydantic (treinamento, APR)
│   ├── prompts.py            # instruções do agente
│   ├── cliente_claude.py     # chamada à API com cache de prompt
│   ├── ingestao.py           # leitura de .md/.txt/.pdf/.docx
│   ├── cli.py                # comandos de linha de comando
│   └── geradores/            # PPTX e Word
├── saidas/                   # arquivos gerados (não versionados)
└── tests/
```

## Roadmap

- [x] Treinamento → PPTX
- [x] Apreciação de risco → Word
- [ ] Plano de içamento (rigging plan) e checklist de inspeção de acessórios
- [ ] Geração de avaliação/prova com gabarito
- [ ] Importar normas oficiais completas para a base

## Aviso

Os entregáveis são **apoio** à elaboração de treinamentos e apreciações de risco.
**Revise sempre** com profissional habilitado (Eng. de Segurança / responsável técnico)
e confirme a redação e a edição vigentes das NRs e normas ABNT antes do uso oficial.
