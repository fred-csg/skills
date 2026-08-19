---
name: criar-provis
description: Cria PROVIs — experimentos, demonstrações e analogias visuais — para eventos, webinars, CPLs, aulas, apresentações, lançamentos e conteúdos, com roteiro, materiais, variações online/presencial, acessibilidade, ensaio e plano B. Use quando o usuário pedir prova visual instantânea, experimento ao vivo, demonstração física, momento AHA, metáfora visual, arsenal de PROVIs ou experiência memorável; distinguir ilustração de evidência e aplicar protocolo de segurança.
---

# Criar PROVIs

Transformar conceitos abstratos em experiências visuais claras e memoráveis. Usar “PROVI” como nome do formato, não como licença para chamar qualquer encenação de prova.

## Coletar o contexto

1. Ler [references/briefing.md](references/briefing.md).
2. Extrair produto, método, transformação, preço, público, objeções, evento, duração, recursos, conceitos, drivers, local e limitações técnicas.
3. Perguntar em uma única rodada pelos campos críticos ausentes. Não criar experimentos físicos sem conhecer ambiente, público e recursos.
4. Confirmar quantidade desejada. Se não houver preferência, propor de cinco a dez PROVIs; criar de dez a vinte somente quando existirem conceitos distintos suficientes.

## Classificar antes de criar

Ler [references/evidence-model.md](references/evidence-model.md). Classificar cada ideia:

- **Experimento**: testa uma relação observável com procedimento, variável e resultado.
- **Demonstração**: mostra como algo funciona em condições definidas.
- **Analogia visual**: ilustra uma ideia por semelhança; não prova a ideia aplicada ao produto ou à vida.

Declarar a classificação no roteiro. Nunca apresentar balde furado, vela, semente, GPS, receita, martelo ou quebra-cabeça como evidência de ROI, comportamento humano ou eficácia do produto.

## Preservar integridade

- Não prometer “provar qualquer conceito”, destruir objeções ou tornar compra inevitável.
- Não usar dramatização para esconder ausência de dados, causalidade ou condições.
- Não inventar perdas, estatísticas, urgência, cases, reação da audiência ou resultado esperado.
- Usar `[FONTE NECESSÁRIA]` para claims pendentes e mostrar limitações.
- Não fabricar falha, reação de voluntário ou resultado do experimento.
- Não gravar ou reutilizar reação como depoimento sem consentimento específico.
- Não pressionar voluntários, ridicularizar erros ou revelar informações pessoais.
- Permitir que a audiência tire conclusões, mas corrigir inferências que excedam o que a demonstração sustenta.
- Tratar objeções legítimas com informação adicional; um visual não invalida restrições reais de tempo, dinheiro, risco ou adequação.

## Aplicar segurança e acessibilidade

Ler [references/safety.md](references/safety.md) antes de propor materiais ou participação.

- Preferir objetos cotidianos, estáveis, não tóxicos, não cortantes, não inflamáveis e sem ingestão.
- Não criar instruções de alto risco envolvendo chama aberta, explosão, alta tensão, químicos perigosos, vidro quebrável, pressão, armas, animais ou contato corporal.
- Para risco moderado, exigir avaliação do local, responsável técnico, barreira, equipamento de proteção e alternativa gravada.
- Obter consentimento de voluntários e oferecer participação opcional sem constrangimento.
- Fornecer descrição verbal, contraste suficiente, escala visual, legendas e alternativa não visual.
- Considerar alergias, mobilidade, neurodiversidade, epilepsia fotossensível, ruído, odores e distância do público.

## Criar cada PROVI

Ler [references/provi-framework.md](references/provi-framework.md). Para cada conceito, produzir:

- nome, classificação, claim e limite do claim;
- prioridade, momento e objetivo educacional;
- setup, execução, observação-chave e bridge;
- duração e lista exata de materiais;
- fonte ou evidência relacionada;
- versões online, presencial e grande público;
- plano B e versão gravada;
- riscos, mitigação, consentimento e acessibilidade;
- frases de introdução, observação e síntese;
- checklist de ensaio e critério de sucesso.

O momento “AHA” deve ser uma compreensão demonstrável, não reação emocional presumida.

## Orquestrar o conjunto

1. Priorizar conceitos críticos, importantes e de apoio.
2. Ordenar por compreensão: diagnóstico → mecanismo → aplicação → evidência → decisão.
3. Alternar demonstração e explicação; evitar saturação visual.
4. Limitar PROVIs próximos à oferta aos que esclarecem método, adequação ou prova real. Não usar urgência visual artificial.
5. Criar transições e callbacks que acrescentem informação.
6. Consolidar materiais, responsáveis, tempo de montagem, descarte e contingências.

## Validar e entregar

1. Estruturar o arsenal em JSON quando possível.
2. Executar `scripts/validate_provis.py`.
3. Corrigir classificação, claims, campos, riscos e acessibilidade.
4. Ler [references/report-template.md](references/report-template.md) e gerar o arquivo no caminho solicitado; sem caminho, usar `provis.md` no diretório de trabalho.
5. Ensaiar cada PROVI no ambiente real e filmar um backup quando a falha comprometer a apresentação.

Medir compreensão, lembrança correta, execução, tempo, falhas, acessibilidade e percepção de credibilidade. Não usar intensidade emocional como substituto de aprendizado.
