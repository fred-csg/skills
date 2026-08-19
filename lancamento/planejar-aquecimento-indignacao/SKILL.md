---
name: planejar-aquecimento-indignacao
description: Planeja campanhas de aquecimento de 30 dias com 90 conteúdos para lançamentos, eventos, CPLs, webinars e aberturas de turma, usando progressão de consciência, indignação fundamentada, mobilização e desejo de mudança. Use quando o usuário pedir aquecimento com indignação, campanha visceral, calendário emocional, 90 conteúdos, jornada pré-lançamento ou preparação de audiência fria; conduzir briefing e checkpoints semanais antes de produzir o calendário completo.
---

# Planejar aquecimento com indignação

Criar uma campanha coordenada de 30 dias e 90 conteúdos que transforme desconhecimento em consciência, consciência em indignação fundamentada e indignação em ação construtiva. Manter a intensidade sem fabricar inimigos, conspirações ou urgência.

## Conduzir o briefing

1. Ler [references/briefing.md](references/briefing.md).
2. Extrair do pedido e dos arquivos tudo o que já estiver disponível.
3. Perguntar apenas pelos campos críticos ausentes, agrupando as perguntas em uma única mensagem curta.
4. Não produzir calendário personalizado antes de conhecer, no mínimo: oferta ou evento, público, problema, mudança desejada, tese central, evidências disponíveis, canais e data.
5. Se o usuário não tiver evidências para uma acusação, reformular a tese como crítica de prática, incentivo, crença ou consequência observável.

## Aplicar limites de integridade

- Direcionar indignação a práticas, incentivos, sistemas verificáveis ou crenças prejudiciais; nunca a características protegidas, pessoas privadas ou grupos vulneráveis.
- Não inventar conspirações, estatísticas, bastidores, vítimas, depoimentos, censura, intenção deliberada ou “verdades que querem esconder”.
- Não acusar pessoa, empresa ou autoridade de fraude, mentira ou dano sem fonte confiável e contexto. Preferir contrastar ideias e práticas.
- Não explorar trauma, medo, vergonha, raiva ou insegurança individual para reduzir autonomia de decisão.
- Não buscar obsessão, vingança, humilhação ou ação drástica. Converter energia emocional em clareza, agência e próximos passos proporcionais.
- Usar urgência e escassez somente quando forem reais, explicáveis e verificáveis.
- Incluir fonte ou marcador `[FONTE NECESSÁRIA]` em alegações factuais que ainda não tenham sustentação.
- Preservar saída livre: permitir discordância, evitar falso dilema e comunicar claramente quando começa a oferta.

## Desenhar a estratégia antes do calendário

Ler [references/campaign-architecture.md](references/campaign-architecture.md). Produzir primeiro:

- tese central e mudança de crença;
- problema ou prática criticada;
- evidências e limites da afirmação;
- narrativa dos quatro estágios;
- papel do especialista e do evento;
- intensidade por semana;
- mix de canais e formatos;
- métricas e critérios de pausa.

Apresentar o conceito da Semana 1 e oferecer as opções: aprovar, ajustar intensidade, modificar formatos ou fazer outro ajuste. Aguardar confirmação antes de detalhar a semana. Repetir o checkpoint para cada semana. Somente depois das quatro aprovações gerar o calendário consolidado de 90 conteúdos.

## Produzir cada conteúdo

Ler [references/content-frameworks.md](references/content-frameworks.md). Criar três peças coordenadas por dia, adaptadas aos canais informados. Para cada peça, registrar:

- ID, dia, estágio, canal e formato;
- emoção pretendida e intensidade de 1 a 10;
- crença atual e mudança de crença;
- hook, roteiro ou estrutura, evidência e CTA;
- conexão com a peça anterior e ponte para a próxima;
- ativo necessário, responsável e status;
- risco de interpretação e mitigação.

Variar formatos e funções. Não repetir o mesmo argumento com embalagem diferente. Tornar cada CTA proporcional ao estágio: reflexão e resposta no início; participação e inscrição perto do evento.

## Validar e entregar

1. Exportar a versão estruturada em JSON quando possível e executar `scripts/validate_campaign.py`.
2. Corrigir erros de cobertura, sequência, intensidade e campos ausentes.
3. Ler [references/deliverable-template.md](references/deliverable-template.md) e gerar o arquivo no local solicitado pelo usuário; se nenhum caminho for informado, usar `aquecimento_indignacao_30dias.md` no diretório de trabalho.
4. Incluir resumo, calendário, frameworks, execução, métricas, fontes e registro das aprovações.
5. Não prometer horários “estratégicos” universais. Recomendar horários com base em dados históricos ou marcá-los como hipóteses de teste.

Após o lançamento, comparar métricas por estágio e registrar o que manter, remover ou testar na próxima campanha.
