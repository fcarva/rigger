# Base de conhecimento

Esta pasta é o "cérebro" do agente. Tudo o que você colocar aqui é lido e usado
para gerar os treinamentos e as apreciações de risco.

## Estrutura

```
base_conhecimento/
├── cursos/    → material bruto do curso (PDF, DOCX, TXT, MD)
└── normas/    → resumos/textos das NRs e ABNT aplicáveis (MD ou TXT)
```

## Como alimentar

1. **`cursos/`** — jogue aqui as apostilas, slides, manuais e anotações do curso de
   içamento de carga. Formatos lidos automaticamente: `.md`, `.txt`, `.pdf`, `.docx`.
2. **`normas/`** — mantenha aqui resumos das normas. O arquivo
   [`normas/icamento_carga.md`](normas/icamento_carga.md) já vem com um índice inicial
   das NRs e ABNT mais relevantes. Expanda-o conforme necessário (cole trechos,
   adicione novas normas, etc.).

> O agente trata o conteúdo de `normas/` como referência estável (fica em cache para
> baratear chamadas repetidas) e o conteúdo de `cursos/` como a entrada da geração.

## Boas práticas

- Prefira texto pesquisável (PDFs "de verdade", não imagens escaneadas).
- Um assunto por arquivo facilita a curadoria.
- Cite a fonte no topo de cada arquivo (norma, edição, ano).
