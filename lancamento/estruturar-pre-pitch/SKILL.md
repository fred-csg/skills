---
name: estruturar-pre-pitch
description: Seleciona e orquestra drivers narrativos em roteiros de pré-pitch para webinars, eventos presenciais, CPLs, desafios, lives, aulas e lançamentos, criando uma ponte coerente entre conteúdo, prova, adequação e oferta. Use quando o usuário pedir pré-pitch invisível, transição conteúdo-venda, sequência de drivers, roteiro antes da oferta, minutagem de pitch, ponte emocional-lógica ou preparação para apresentação comercial; tornar a transição fluida, mas explicitamente comercial.
---

# Estruturar pré-pitch

Criar uma transição narrativa que sintetize o conteúdo, demonstre o mecanismo e prepare uma avaliação informada da oferta. Interpretar “invisível” como fluidez editorial, nunca como venda disfarçada ou influência subliminar.

## Verificar pré-requisitos

1. Ler [references/briefing.md](references/briefing.md).
2. Localizar a lista de drivers, o perfil da audiência, a estrutura do evento, a oferta, a duração e as provas.
3. Se faltarem drivers, pedir o arquivo ou oferecer criar drivers provisórios claramente rotulados como hipóteses. Não inventar psicologia da audiência.
4. Perguntar em uma única rodada pelos campos críticos ausentes.
5. Confirmar formato, duração disponível, intensidade desejada e momento exato da oferta.

## Preservar transparência e autonomia

- Informar claramente quando o conteúdo termina e começa a apresentação da oferta.
- Não usar hipnose, subliminaridade, comandos embutidos, confusão, sobrecarga emocional ou venda “sem a pessoa perceber”.
- Não buscar decisão inevitável, ausência de resistência, ansiedade para comprar ou “zero objeções”.
- Não explorar feridas, trauma, vergonha, medo existencial, inferioridade ou dependência do apresentador.
- Não criar falso dilema entre comprar e aceitar sofrimento. Apresentar alternativas e a possibilidade legítima de não comprar.
- Não afirmar o que a audiência “está sentindo” sem evidência observável. Formular convites e perguntas, não leitura mental.
- Não inventar estatísticas, ROI, resultados, depoimentos ou garantias. Usar `[FONTE NECESSÁRIA]` até validar.
- Não chamar números de irrefutáveis. Mostrar fonte, fórmula, premissas, data e limitações.
- Usar urgência e escassez somente quando reais, explicáveis e verificáveis.
- Tratar objeções como dúvidas ou restrições legítimas. Antecipá-las com informação, não neutralizá-las de modo oculto.

## Selecionar e ordenar os drivers

Ler [references/architecture.md](references/architecture.md). Selecionar de cinco a sete drivers quando houver repertório suficiente, garantindo funções distintas:

1. Consciência do problema ou oportunidade.
2. Consequência verificável.
3. Possibilidade desejada.
4. Mecanismo ou método.
5. Prova e contexto.
6. Adequação, esforço e trade-offs.
7. Próximo passo.

Pontuar cada candidato por relevância, evidência, novidade, clareza e compatibilidade com a oferta. Remover drivers redundantes, agressivos ou sem prova. Apresentar a seleção e a ordem para validação antes do roteiro completo quando o usuário pedir checkpoints.

## Construir o roteiro

Ler [references/script-patterns.md](references/script-patterns.md) e [references/formats.md](references/formats.md). Criar uma sequência com minutagem:

1. Abertura: recuperar a tese e orientar o que será concluído.
2. Problema: sintetizar evidência e consequência sem dramatização excessiva.
3. Possibilidade: mostrar resultado plausível e condições.
4. Mecanismo: explicar como o caminho funciona.
5. Prova: usar dados, casos e demonstração com limitações.
6. Adequação: explicar esforço, risco, objeções, para quem serve e não serve.
7. Transição: declarar que uma oferta será apresentada e permitir escolha consciente.

Para cada segmento, fornecer driver, objetivo, duração, script, evidência, elemento visual, transição, risco e mitigação. Não impor proporção fixa de emoção e lógica; ajustar à audiência, ao formato e à força das provas.

## Adaptar ao formato

- Webinar: usar bloco concentrado próximo à oferta, preservando tempo para perguntas.
- Evento presencial: distribuir sínteses e provas ao longo do evento; fazer a transição comercial em momento definido.
- CPL ou desafio: semear conceitos nas etapas anteriores e consolidar no último conteúdo.
- Lives: entregar valor completo em cada live; não usar sementes subliminares.
- Aula gravada: separar claramente conteúdo, recapitulação e oferta.

Não presumir durações universais. Tratar faixas sugeridas como ponto de partida e ajustar ao total informado.

## Validar e entregar

1. Estruturar o roteiro em JSON quando possível.
2. Executar `scripts/validate_prepitch.py`.
3. Corrigir sobreposição de tempo, ausência de prova, transição comercial ambígua e padrões coercitivos.
4. Ler [references/report-template.md](references/report-template.md) e gerar o arquivo no local solicitado; sem caminho, usar `pre_pitch.md` no diretório de trabalho.
5. Incluir versão completa, versão de ensaio, mapa de slides, fontes e plano de contingência.

Medir atenção, compreensão, perguntas, adequação percebida, intenção declarada, conversão, reembolso e percepção de pressão. Silêncio, concordância física ou emoção no chat não comprovam consentimento nem eficácia.
