---
name: analisar-aula
description: Analisa aulas, CPLs, webinars, lives, workshops, masterclasses, VSLs educacionais e respectivas transcrições para mapear estrutura, narrativa, persuasão, retenção, oferta, objeções, linguagem, ritmo e oportunidades de melhoria. Use quando o usuário pedir análise forense, dissecação minuto a minuto, avaliação de uma aula de lançamento, diagnóstico de conversão, DNA persuasivo, análise de roteiro ou comparação entre apresentações.
---

# Analisar aula

Produzir uma análise rigorosa, útil e baseada em evidências. Tratar cada afirmação como uma hipótese a ser sustentada pelo material, não como leitura mental da audiência.

## Preparar a análise

1. Inventariar os materiais recebidos: transcrição, timestamps, vídeo, áudio, slides, página de oferta, chat e métricas de retenção/conversão.
2. Identificar o formato e o objetivo provável: aula pura, CPL, webinar, lançamento, workshop ou híbrido.
3. Registrar o contexto fornecido: posição na sequência, temperatura e origem da audiência, produto, preço, estágio do lançamento e evento anterior/posterior.
4. Não interromper o trabalho para pedir contexto opcional. Analisar o que estiver disponível e listar as lacunas que afetam a confiança.
5. Se houver transcrição em arquivo, executar `scripts/analyze_transcript.py` para obter contagens determinísticas. Não substituir leitura qualitativa pelo script.

## Preservar integridade da evidência

- Usar timestamps exatos somente quando existirem no material. Sem timestamps, usar ordem relativa ou estimativas claramente rotuladas.
- Distinguir em todo o relatório: **observado**, **inferência** e **não verificável**.
- Nunca inventar retenção, reação emocional, conversão, intenção do apresentador ou desempenho da audiência.
- Tratar contagens automáticas como indicadores: revisar falsos positivos, flexões, ironia, citações e contexto.
- Citar trechos curtos e timestamps para sustentar conclusões importantes.
- Não chamar um score de “científico”. Explicar que notas são rubricas diagnósticas e mostrar os critérios.
- Sinalizar urgência falsa, escassez artificial, promessas sem prova, exploração de medo/vergonha e outras práticas potencialmente enganosas.

## Executar o protocolo

Ler [references/forensic-rubric.md](references/forensic-rubric.md) antes de analisar. Aplicar as 12 camadas relevantes ao material:

1. Abertura e hook.
2. Arquitetura narrativa.
3. Construção de autoridade.
4. Gestão de objeções.
5. Construção de desejo.
6. Educação versus revelação.
7. Oferta, somente se existir.
8. Linguagem e padrões verbais.
9. Tempo, ritmo e transições.
10. Pontos de maior impacto.
11. Vazamentos e otimizações.
12. Métricas forenses.

Para cada achado relevante, registrar:

- evidência: trecho, evento visual ou timestamp;
- função provável no fluxo;
- efeito esperado, sem afirmar reação não observada;
- confiança: alta, média ou baixa;
- recomendação específica, quando houver.

## Medir a transcrição

Executar:

```bash
python scripts/analyze_transcript.py caminho/para/transcricao.txt
```

Adicionar `--duration-minutes N` quando a duração for conhecida. Ler [references/measurement-rules.md](references/measurement-rules.md) antes de interpretar os resultados. Se Python não estiver disponível, fazer apenas as contagens essenciais com as ferramentas locais e declarar o método.

## Produzir o relatório

Ler [references/report-template.md](references/report-template.md) e adaptar a profundidade ao pedido e ao material. Priorizar densidade sobre volume; não fabricar “15 páginas” quando os dados não sustentarem esse tamanho.

Incluir obrigatoriamente:

- veredicto executivo e estratégia principal;
- mapa cronológico baseado na granularidade real dos dados;
- DNA da conversão e sequência persuasiva;
- forças, vazamentos e recomendações priorizadas;
- quadro de evidências com confiança;
- métricas objetivas disponíveis e limitações;
- scores diagnósticos com justificativas.

Quando houver dados de retenção, chat, cliques ou vendas, cruzá-los com os momentos do roteiro e separar correlação de causalidade. Quando não houver, indicar quais dados confirmariam ou refutariam os principais diagnósticos.

## Encerrar

Entregar o relatório completo no arquivo ou formato solicitado. Encerrar sempre com uma única pergunta objetiva: “Você prefere aprofundar uma das 12 camadas ou investigar os principais pontos cegos e suas correções?”
