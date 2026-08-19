# Entrega e manifesto

## Documento Master

1. **Sumário executivo**: categoria, público, problema, método e estágio de validação.
2. **Origem**: rota DC ou Contexto, arquivos e limitações.
3. **Tese da categoria**: âncora, twist, definição, fronteiras e alternativas.
4. **Naming**: finalistas, scorecard, decisão e status de busca.
5. **Metodologia**: filosofia, mecanismos, pilares, progressão e critérios.
6. **Ativos**: glossário, ferramentas, diagnósticos, templates e métricas.
7. **Evidência**: ciência, casos, dados, comparações e alegações permitidas.
8. **Aplicação**: pré-requisitos, implementação, exceções e adaptações.
9. **Validação**: testes de compreensão, demanda, entrega e resultado.
10. **Roadmap**: gaps, responsáveis e próxima versão.

## Manifesto JSON mínimo

```json
{
  "project": {"name": "Nome do projeto", "owner": "Especialista"},
  "route": "dc",
  "inputs": [{"type": "download_cerebral", "source": "dc.md", "status": "provided"}],
  "phases": [
    {
      "id": 1,
      "name": "Singularidade e categoria",
      "status": "approved",
      "outputs": ["fase-1.md"],
      "evidence": ["dc.md"],
      "assumptions": [],
      "checkpoint": "approved",
      "approved_by": "usuario",
      "approved_at": "2026-08-19"
    }
  ],
  "category": {
    "reference_category": "Categoria existente",
    "twist": "Diferença operacional",
    "twist_source": "dc.md#secao",
    "candidate_name": "Nome candidato",
    "definition": "Definição em uma frase",
    "registration_status": "unsearched"
  },
  "methodology": {"mechanism_count": 3, "pillar_count": 3},
  "claims": [
    {"claim": "Alegação", "status": "hypothesis", "source": ""}
  ]
}
```

Rotas válidas: `dc` e `context`. A rota `dc` exige fases 1–4; `context`, fases 1–5.

Status de fase: `not_started`, `in_progress`, `review`, `approved`. Checkpoint: `pending`, `approved`, `changes_requested`, `paused`.

Status de registro: `unsearched`, `preliminary_search`, `legal_review_required`, `registered`. Se `registered`, registrar jurisdição, órgão e número do registro.
