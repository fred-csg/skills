---
name: resume-screener
description: Triagem eficiente de currículos em relação aos requisitos da vaga, com pontuação estruturada, identificação de sinais de alerta e recomendações de entrevista
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Triagem de Currículos

> Avaliar sistematicamente currículos em relação aos requisitos da vaga para identificar candidatos qualificados, sinalizar preocupações e priorizar entrevistas.

## Quando Usar Esta Skill

- Triagem de candidaturas em alto volume
- Criação de critérios de triagem
- Construção de rubricas de avaliação
- Treinamento de gestores de contratação
- Auditoria de consistência na triagem

## Fundamentação Metodológica

Baseada em **pesquisa sobre entrevistas estruturadas** e **diretrizes da EEOC**, combinando:
- Apenas critérios relacionados ao cargo
- Rubricas de pontuação objetivas
- Avaliação consciente de vieses
- Requisitos de documentação

## O Que o Claude Faz vs. O Que Você Decide

| Claude Faz | Você Decide |
|-------------|----------|
| Cria rubricas de triagem | Decisões de contratação |
| Pontua com base nos critérios | Avaliação de fit cultural |
| Identifica sinais positivos/negativos | Convite para entrevista |
| Resume qualificações | Seleção final |
| Sinaliza possíveis preocupações | Tratamento de exceções |

## Instruções

### Etapa 1: Definir os Critérios da Vaga

**Obrigatórios vs. Desejáveis:**
| Categoria | Obrigatório | Desejável |
|----------|-----------|--------------|
| Formação | Grau mínimo | Formação avançada |
| Experiência | X anos em Y | Setor específico |
| Habilidades | Técnicas essenciais | Habilidades adjacentes |
| Certificações | Licenças exigidas | Certificações preferenciais |

**Peso da Pontuação:**
| Critério | Peso | Justificativa |
|-----------|--------|-----------|
| Experiência obrigatória | 40% | Capacidade essencial |
| Habilidades obrigatórias | 30% | Impacto desde o primeiro dia |
| Formação | 15% | Base |
| Qualificações desejáveis | 15% | Potencial de crescimento |

### Etapa 2: Criar a Rubrica de Triagem

**Escala de Pontuação:**
| Pontuação | Definição |
|-------|------------|
| 4 | Supera significativamente o requisito |
| 3 | Atende plenamente ao requisito |
| 2 | Atende parcialmente ao requisito |
| 1 | Não atende ao requisito |
| 0 | Não é possível avaliar pelo currículo |

### Etapa 3: Avaliar o Currículo

**Framework de Avaliação:**
1. Verificar os requisitos obrigatórios (aprovado/reprovado binário)
2. Pontuar cada critério (escala de 1 a 4)
3. Calcular o total ponderado
4. Identificar sinais (positivos e negativos)
5. Fazer a recomendação

### Etapa 4: Documentar os Resultados

**Para Cada Currículo:**
- Pontuação geral
- Checklist de requisitos obrigatórios
- Pontuações por critério
- Sinais e preocupações
- Recomendação com justificativa

### Etapa 5: Priorizar Candidatos

**Matriz de Prioridade:**
| Faixa de Pontuação | Ação |
|-------------|--------|
| 80-100% | Entrevista prioritária |
| 60-79% | Análise padrão |
| 40-59% | Em espera condicional |
| <40% | Não qualificado |

## Exemplos

### Exemplo 1: Triagem Completa de Currículo

**Entrada:**
```
Vaga: Gerente de Produto Sênior

Requisitos:
- 5+ anos de experiência em gestão de produto
- Experiência obrigatória em B2B SaaS
- Formação técnica ou experiência equivalente
- Experiência com metodologias Ágeis
- Desejável: MBA ou similar

Currículo:
Jane Smith
Product Manager na TechCorp (3 anos)
- Liderou o roadmap de produto de uma plataforma de analytics B2B
- Gerenciou equipe de 4 designers e engenheiros
- Aumentou a retenção de usuários em 35%

Associate PM na StartupXYZ (2 anos)
- Aplicativo mobile B2C
- Lançou 3 grandes funcionalidades

Formação: Bacharelado em Ciência da Computação, Stanford
Certificações: CSPO, SAFe Agilist
```

**Saída:**
```
## Triagem de Currículo: Jane Smith

### Resumo Rápido
**Vaga:** Gerente de Produto Sênior
**Candidata:** Jane Smith
**Pontuação:** 78/100 - ANÁLISE PADRÃO

---

### Requisitos Obrigatórios

| Requisito | Status | Evidência |
|-------------|--------|----------|
| 5+ anos de experiência em PM | ✅ APROVADO | 3 + 2 = 5 anos no total |
| Experiência em B2B SaaS | ✅ APROVADO | TechCorp analytics B2B |
| Formação técnica/equivalente | ✅ APROVADO | Bacharelado CC Stanford |
| Experiência com Ágil | ✅ APROVADO | Certificações CSPO, SAFe |

**Resultado dos Obrigatórios:** APROVADO (4/4)

---

### Pontuação Detalhada

| Critério | Peso | Pontuação | Ponderado | Observações |
|-----------|--------|-------|----------|-------|
| Anos de Experiência | 40% | 3/4 | 30/40 | Atende exatamente ao mínimo |
| B2B SaaS | 30% | 3/4 | 22.5/30 | 3 anos, não o tempo integral |
| Formação Técnica | 15% | 4/4 | 15/15 | Stanford CC |
| Desejável (MBA) | 15% | 2/4 | 7.5/15 | Tem certificações, não tem MBA |

**Pontuação Total: 75/100**

---

### Sinais Positivos

| Sinal | Evidência | Relevância |
|------|----------|--------------|
| Impacto quantificado | "aumento de 35% na retenção" | Orientada a resultados |
| Experiência em gestão | "Equipe de 4 pessoas" | Pronta para liderar |
| Certificações relevantes | CSPO, SAFe | Comprometimento com Ágil |
| Formação de ponta | Stanford CC | Base técnica sólida |

---

### Sinais de Atenção

| Sinal | Preocupação | Mitigação |
|------|---------|------------|
| Experiência exatamente no mínimo | Atinge exatamente 5 anos | Aprofundar na entrevista |
| B2B/B2C misto | 2 anos em B2C | Entender a transição para B2B |
| Sem MBA | Qualificação desejável | Certificações podem compensar |

---

### Sinais Negativos

Nenhum identificado.

---

### Recomendação de Entrevista

**Decisão:** RECOMENDADA PARA ENTREVISTA

**Justificativa:**
- Atende a todos os requisitos obrigatórios
- Forte experiência em B2B SaaS na TechCorp
- Formação técnica supera as expectativas
- Conquistas quantificadas demonstram impacto

**Pontos a Explorar na Entrevista:**
1. Profundidade da experiência em estratégia de produto B2B
2. Transição de B2C para contexto B2B
3. Escala dos produtos gerenciados (ARR, usuários)
4. Exemplos de liderança multifuncional

---

### Notas de Comparação

Candidata é sólida, mas não excepcional. Atende aos requisitos sem
superá-los significativamente. Considerar junto a candidatos mais
fortes, se disponíveis.
```

### Exemplo 2: Resumo de Triagem em Lote

**Entrada:**
```
Faça a triagem destes 5 candidatos para Gerente de Marketing:
Requisitos: 3+ anos de marketing, experiência em B2B, habilidades em analytics

1. Alice: 5 anos em marketing B2B, certificada em Google Analytics
2. Bob: 2 anos de marketing, apenas B2C, forte em analytics
3. Carol: 4 anos, B2B/B2C misto, Excel básico
4. David: 6 anos em B2B, é dono de uma ferramenta de marketing analytics
5. Eve: 3 anos em B2B, certificada em HubSpot
```

**Saída:**
```
## Resumo de Triagem em Lote: Gerente de Marketing

### Ranking Rápido

| Posição | Candidato | Pontuação | Recomendação |
|------|-----------|-------|----------------|
| 1 | David | 95% | Entrevista prioritária |
| 2 | Alice | 85% | Entrevista prioritária |
| 3 | Eve | 75% | Análise padrão |
| 4 | Carol | 55% | Em espera condicional |
| 5 | Bob | 40% | Não qualificado |

---

### Resumos Individuais

#### 1. David (95%) - ENTREVISTA PRIORITÁRIA

| Requisito | Status | Pontuação |
|-------------|--------|-------|
| 3+ anos | ✅ 6 anos | 4/4 |
| Experiência em B2B | ✅ Tempo integral | 4/4 |
| Habilidades em analytics | ✅ Dono da ferramenta | 4/4 |

**Destaque:** Profundidade excepcional em analytics - é dono de uma ferramenta de marketing analytics
**Entrevista:** Imediatamente

---

#### 2. Alice (85%) - ENTREVISTA PRIORITÁRIA

| Requisito | Status | Pontuação |
|-------------|--------|-------|
| 3+ anos | ✅ 5 anos | 4/4 |
| Experiência em B2B | ✅ Tempo integral | 4/4 |
| Habilidades em analytics | ✅ Certificada em GA | 3/4 |

**Destaque:** Sólida no geral, certificação em Google Analytics
**Entrevista:** Nesta semana

---

#### 3. Eve (75%) - ANÁLISE PADRÃO

| Requisito | Status | Pontuação |
|-------------|--------|-------|
| 3+ anos | ✅ Exatamente 3 | 3/4 |
| Experiência em B2B | ✅ Tempo integral | 4/4 |
| Habilidades em analytics | ⚠️ Apenas HubSpot | 2/4 |

**Preocupação:** HubSpot é automação, não analytics
**Entrevista:** Aprofundar em habilidades de analytics

---

#### 4. Carol (55%) - EM ESPERA CONDICIONAL

| Requisito | Status | Pontuação |
|-------------|--------|-------|
| 3+ anos | ✅ 4 anos | 3/4 |
| Experiência em B2B | ⚠️ Mista | 2/4 |
| Habilidades em analytics | ❌ Excel básico | 1/4 |

**Preocupação:** Base fraca em analytics
**Espera:** Considerar se os melhores candidatos recusarem

---

#### 5. Bob (40%) - NÃO QUALIFICADO

| Requisito | Status | Pontuação |
|-------------|--------|-------|
| 3+ anos | ❌ 2 anos | 1/4 |
| Experiência em B2B | ❌ Apenas B2C | 1/4 |
| Habilidades em analytics | ✅ Forte | 3/4 |

**Desqualificado:** Não atende aos requisitos de experiência ou B2B
**Ação:** Rejeitar com observação positiva sobre habilidades em analytics

---

### Ações de Triagem

| Ação | Candidatos |
|--------|------------|
| Agendar entrevistas | David, Alice |
| Fila padrão | Eve |
| Arquivo em espera | Carol |
| E-mail de rejeição | Bob |
```

## Limites da Skill

### O Que Esta Skill Faz Bem
- Estruturar critérios de avaliação
- Aplicar pontuação de forma consistente
- Identificar sinais relevantes
- Documentar decisões

### O Que Esta Skill Não Pode Fazer
- Avaliar fit cultural
- Verificar a veracidade das informações
- Realizar verificações de antecedentes
- Substituir o julgamento humano

### Notas Importantes de Conformidade
- Focar apenas em critérios relacionados ao cargo
- Evitar considerações sobre classes protegidas
- Documentar todas as decisões
- Aplicar os critérios de forma consistente

## Guia de Iteração

**Prompts de Continuidade:**
- "Crie perguntas de entrevista com base nesta triagem"
- "O que devo explorar mais a fundo com [candidato]?"
- "Compare os 3 melhores candidatos lado a lado"
- "Redija o e-mail de rejeição para [candidato]"

## Referências

- SHRM Structured Interviewing Guidelines
- EEOC Uniform Guidelines on Employee Selection
- Google re:Work Hiring Practices
- Lever Recruiting Best Practices

## Skills Relacionadas

- `interview-scheduler` - Coordenar entrevistas
- `onboarding-guide` - Integração pós-contratação
- `job-description-writer` - Criar requisitos

## Metadados da Skill

- **Domínio**: Operações de RH
- **Complexidade**: Intermediária
- **Modo**: centaur
- **Tempo até o Valor**: 10-15 min por currículo
- **Pré-requisitos**: Requisitos da vaga, currículos
