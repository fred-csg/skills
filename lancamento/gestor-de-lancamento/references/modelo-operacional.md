# Modelo operacional

## Papel

Atuar como PMO leve do lançamento. O gestor controla o sistema de trabalho; as skills especialistas produzem os artefatos.

## Trilhas

1. **Fundação:** expertise, método e propriedade intelectual.
2. **Pesquisa:** público, mercado, voz e objeções.
3. **Estratégia:** oportunidade, posicionamento, categoria e Big Idea.
4. **Produto e oferta:** jornada, escopo, preço, termos e capacidade.
5. **Evento e conversão:** CPLs, PROVIs, pré-pitch, pitch e follow-up.
6. **Aquecimento:** calendário e peças orgânicas.
7. **Mídia:** criativos, canais, orçamento e testes.
8. **Operação:** páginas, checkout, CRM, automações, tracking, suporte e contingência.
9. **Medição:** plano, dashboard, monitoramento e retrospectiva.
10. **Autoridade:** livro e ativos complementares, quando fizerem parte do escopo.

Nem toda trilha é obrigatória. Selecionar por tipo de lançamento, maturidade e ativos existentes.

## Cadência

- **Checkpoint de fase:** aprovar artefato e liberar dependências.
- **Revisão semanal:** progresso, riscos, decisões e próximas ações.
- **Revisão diária na janela crítica:** operação, métricas, incidentes e capacidade.
- **Retrospectiva:** resultado, causa provável, aprendizados e mudanças futuras.

## Fonte de verdade

Usar `_lancamento/project.json` como estado canônico. Derivar:

- `status.md` para leitura rápida;
- `roadmap.md` para sequência e marcos;
- `decisions.md` para decisões imutáveis;
- `risks.md` para exposição e mitigação;
- `evidence-ledger.md` e `claims-ledger.md` para sustentação;
- `change-log.md` para mudanças;
- `handoffs/` para contratos entre skills.

## Saúde do projeto

Classificar:

- **verde:** sem bloqueio crítico; próximo marco plausível;
- **amarelo:** risco relevante ou atraso absorvível;
- **vermelho:** data, legalidade, oferta, operação ou prova crítica comprometida;
- **cinza:** dados insuficientes para diagnóstico.

Nunca calcular saúde apenas pela porcentagem de tarefas concluídas.
