# Contratos de artefatos e manifesto

## Dependências

```text
F1 oportunidade
 └─ F2 posicionamento
     └─ F3 Big Idea
         ├─ F4 produto
         │   └─ F5 oferta
         └─ F6 evento ← F5
             └─ F7 mensagem integrada
                 ├─ F8 aquecimento
                 └─ F9 anúncios ← F8
```

Uma fase pode ser explorada antes da anterior, mas não pode ser marcada como concluída se suas dependências ainda estiverem pendentes.

## Contrato comum de fase

Cada fase deve registrar:

- `id`, `name`, `status`: `not_started`, `in_progress`, `review` ou `approved`;
- `inputs`: caminhos, URLs ou IDs dos artefatos usados;
- `outputs`: caminhos ou IDs do que foi produzido;
- `evidence`: fontes e dados que sustentam decisões;
- `assumptions`: hipóteses ainda não confirmadas;
- `risks`: limitações, dependências e mitigação;
- `checkpoint`: `pending`, `approved`, `changes_requested` ou `paused`;
- `approved_by` e `approved_at` quando aprovado.

## Contratos mínimos dos módulos especializados

- **Perfil**: segmentos, padrões agregados, citações anonimizadas, desejos, barreiras, linguagem, limites da amostra.
- **Objeções**: objeção, evidência de frequência, raiz provável, resposta, prova, momento e limite.
- **Drivers**: nome, ideia, emoção legítima, evidência, contexto, frase-âncora e risco de mau uso.
- **PROVI**: conceito, demonstração, materiais, roteiro, segurança, plano B e bridge honesta.
- **Pré-pitch**: objetivo, sequência, transições, prova, objeções, indicação comercial explícita e duração.
- **Conteúdo**: campos definidos na fase 8.
- **Anúncio**: campos definidos na fase 9.

## Manifesto JSON mínimo

```json
{
  "project": {
    "name": "Nome do lançamento",
    "version": "1.0",
    "owner": "Responsável",
    "target_date": "2026-11-01"
  },
  "context": {
    "expert_brief": "provided",
    "avatar_research": "partial",
    "market_research": "provided",
    "current_product": "provided",
    "launch_history": "not_applicable",
    "resources": "provided"
  },
  "phases": [
    {
      "id": 1,
      "name": "Oportunidade",
      "status": "approved",
      "inputs": ["briefing.md"],
      "outputs": ["fase-1-oportunidade.md"],
      "evidence": ["pesquisa.csv"],
      "assumptions": [],
      "risks": [],
      "checkpoint": "approved",
      "approved_by": "usuario",
      "approved_at": "2026-08-19"
    }
  ],
  "inventory": {
    "content_count": 0,
    "ad_count": 0
  },
  "claims": [
    {
      "claim": "Descrição da alegação",
      "source": "Fonte ou arquivo",
      "status": "verified"
    }
  ]
}
```

O array `phases` deve conter exatamente os IDs 1 a 9. `content_count` deve chegar a 84 quando a fase 8 estiver aprovada; `ad_count`, a 100 quando a fase 9 estiver aprovada.
