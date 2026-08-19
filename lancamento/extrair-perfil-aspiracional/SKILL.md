---
name: extrair-perfil-aspiracional
description: Extrai perfis aspiracionais de pesquisas de leads, entrevistas, formulários, respostas abertas, planilhas e documentos, mapeando sonhos, objetivos, linguagem, tensões, barreiras, níveis de consciência e oportunidades de comunicação. Use quando o usuário pedir perfil psicológico aspiracional, avatar, persona, voz do cliente, arqueologia da alma, análise de pesquisa, segmentação motivacional ou dossiê de leads; se nenhuma pesquisa ou resposta for fornecida, orientar exatamente como preparar e enviar os dados.
---

# Extrair perfil aspiracional

Transformar pesquisa de leads em um mapa aspiracional baseado em evidências. Usar linguagem elevada e empática sem apresentar metáforas como diagnóstico psicológico.

## Verificar os insumos

1. Procurar respostas de pesquisa no pedido, nos anexos e nos arquivos indicados.
2. Considerar pesquisa válida qualquer conjunto legível de respostas reais: CSV, JSON, TXT, Markdown, documento, planilha ou conteúdo colado.
3. Se não houver respostas, não gerar perfil. Ler [references/intake-guide.md](references/intake-guide.md), orientar o usuário e encerrar aguardando os dados.
4. Se houver respostas, iniciar a análise mesmo que produto, perguntas originais, quantidade ou dados demográficos estejam ausentes. Registrar essas lacunas e pedir contexto apenas se ele for indispensável para interpretar os dados.

## Preparar os dados

1. Inventariar arquivos, formatos, número de respostas, perguntas e campos disponíveis.
2. Preservar o texto original em citações; normalizar somente cópias usadas para contagem.
3. Remover ou mascarar nomes completos, emails, telefones, documentos, endereços e outros identificadores no relatório.
4. Quando houver CSV, JSON ou TXT, executar `scripts/summarize_survey.py` para produzir um panorama reprodutível. Para XLSX, usar uma ferramenta de planilha disponível ou solicitar exportação em CSV.
5. Separar respostas vazias, duplicadas, inválidas e fora de escopo antes de calcular percentuais. Informar o denominador de cada métrica.

## Preservar integridade psicológica

- Tratar “alma”, “potencial adormecido” e “arquétipo” como linguagem narrativa, não como fatos clínicos ou espirituais.
- Não diagnosticar transtornos, traumas, síndrome do impostor, autossabotagem ou crenças inconscientes sem declaração explícita. Preferir “indício”, “hipótese” ou a linguagem literal do respondente.
- Não inferir atributos sensíveis, estado mental, orientação, religião, saúde, renda ou identidade a partir de pistas indiretas.
- Trabalhar preferencialmente no nível agregado. Não criar perfis psicológicos individualizados para exploração ou pressão comercial.
- Não recomendar medo, vergonha, culpa, vulnerabilidade ou dados sensíveis como alavancas de manipulação.
- Diferenciar **observado**, **inferência fundamentada** e **não verificável**. Associar conclusões importantes a contagem, citação anonimizada ou padrão recorrente.
- Não inventar citações, percentuais, segmentos, motivações ou “verdades ocultas”.

## Analisar a pesquisa

Ler [references/analysis-framework.md](references/analysis-framework.md) e executar o fluxo:

1. Descrever a amostra e suas limitações.
2. Extrair objetivos, aspirações, estados desejados e critérios de sucesso.
3. Mapear o gap entre situação atual e futuro desejado.
4. Identificar barreiras declaradas, tensões, tentativas anteriores e resistências.
5. Extrair a voz do cliente: palavras, frases, metáforas, contrastes e referências.
6. Agrupar padrões por motivação, estágio de consciência ou necessidade, não por atributos protegidos.
7. Construir de um a três perfis somente quando houver contraste suficiente entre grupos.
8. Traduzir achados em comunicação, conteúdo, oferta e próximos testes sem ultrapassar a evidência.

Para cada tema, registrar frequência, cobertura da amostra, exemplos anonimizados, variações e confiança. Diferenciar intensidade da linguagem de prevalência: uma resposta dramática não representa necessariamente o grupo.

## Produzir o dossiê

Ler [references/report-template.md](references/report-template.md). Adaptar o tom aspiracional ao vocabulário real da pesquisa; evitar floreio que esconda incerteza.

Incluir obrigatoriamente:

- material analisado, método, amostra e limitações;
- resumo executivo com achados prioritários;
- perfil ou perfis aspiracionais fundamentados;
- sonhos, objetivos, chamados e visão de futuro;
- barreiras e batalhas na linguagem dos respondentes;
- banco de voz do cliente com citações anonimizadas;
- segmentação e critérios observáveis;
- recomendações de comunicação, conteúdo, oferta e pesquisa adicional;
- matriz de evidências e confiança.

Encerrar com um próximo passo específico, escolhido a partir da maior lacuna ou oportunidade encontrada.
