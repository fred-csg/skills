# Estado da sessão

Usar JSON para permitir pausa, retomada e validação.

```json
{
  "session": {
    "id": "maya-2026-08-19-001",
    "expert": "Especialista",
    "area": "Área",
    "goal": "Documentar o método principal",
    "mode": "live",
    "status": "in_progress",
    "question_target": 23,
    "required_domains": ["PC", "CE", "IP", "DF", "AU", "CT", "RE", "OT", "PB"],
    "privacy_boundaries": ["Anonimizar clientes"]
  },
  "context": {
    "experience_years": 10,
    "proven_result": "Resultado com origem",
    "audience": "Público",
    "intended_product": "Curso",
    "desired_transformation": "Transformação"
  },
  "answers": [
    {
      "question_id": "PC1_01",
      "question": "Descreva seu processo principal.",
      "answer": "Resposta do especialista.",
      "source": "meeting-01 00:05:20",
      "confidence": "expert_confirmed",
      "mapped_insights": ["INS-001"],
      "probes": []
    }
  ],
  "insights": [
    {
      "id": "INS-001",
      "type": "explicit",
      "statement": "Descrição do insight",
      "source_question_ids": ["PC1_01"],
      "status": "confirmed"
    }
  ],
  "gaps": ["Critério de conclusão da etapa 2"],
  "checkpoints": []
}
```

Valores permitidos:

- `mode`: `live`, `async`, `material`, `focused`.
- `status`: `in_progress`, `paused`, `needs_validation`, `completed`.
- `confidence`: `expert_confirmed`, `transcript_clear`, `uncertain`.
- tipo de insight: `explicit`, `tacit`, `inference`, `hypothesis`.
- status de insight: `confirmed`, `needs_confirmation`, `contradicted`.

Perguntas de sondagem livres podem ficar em `probes`. Usar `question_id` do banco para as perguntas principais e não criar IDs canônicos inexistentes.
