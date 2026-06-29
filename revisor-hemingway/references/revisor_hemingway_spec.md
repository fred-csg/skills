---
projeto: laboratorio
documento: references/revisor_hemingway_spec.md
status: rascunho
versao: 1.0.0
---

# Especificação Funcional: Skill Revisor Hemingway

Este documento define os requisitos e regras de funcionamento para a skill `revisor-hemingway`. O objetivo é adaptar as diretrizes de escrita clara e concisa do Hemingway Editor para o português do Brasil.

## 1. Regras de Estilo (Categorias Hemingway)

A análise do texto deve avaliar cinco aspectos estilísticos fundamentais, oferecendo melhorias diretas para cada um:

### 1.1. Voz Passiva (Destaque Verde)
*   **Problema:** A voz passiva afasta o sujeito da ação, tornando a leitura mais indireta e o texto mais longo.
*   **Regra:** Identificar construções como "foi feito por", "foram analisados", "será realizado".
*   **Meta:** O número máximo de ocorrências de voz passiva não deve exceder um limite proporcional ao tamanho do texto (aproximadamente 1 para cada 150 palavras).
*   **Solução:** Sugerir a macronversão para a voz ativa correspondente.

### 1.2. Advérbios e Enfraquecedores (Destaque Azul)
*   **Problema:** Advérbios (especialmente os terminados em "-mente") ou enfraquecedores (como "realmente", "muito", "extremamente") costumam camuflar verbos fracos.
*   **Regra:** Identificar advérbios desnecessários ou redundantes.
*   **Meta:** O número máximo de advérbios não deve exceder 1 para cada 150 palavras.
*   **Solução:** Sugerir a eliminação do advérbio ou a substituição do conjunto por um verbo mais forte (ex: "correr muito rapidamente" -> "disparar").

### 1.3. Alternativas Mais Simples (Destaque Roxo)
*   **Problema:** Uso de palavras prolixas, formais ou jargões desnecessários que dificultam a compreensão rápida.
*   **Regra:** Identificar palavras complexas que possuam equivalentes comuns e mais curtos.
*   **Exemplos de mapeamento:**
    *   "utilizar" / "viabilizar" -> "usar"
    *   "efetuar" / "realizar" -> "fazer"
    *   "adquirir" -> "comprar"
    *   "posteriormente" -> "depois"
    *   "adicionalmente" -> "além disso"
    *   "solicitar" -> "pedir"
    *   "inicializar" -> "iniciar" / "começar"
*   **Solução:** Sugerir a alternativa mais simples diretamente.

### 1.4. Frases Difíceis de Ler (Destaque Amarelo)
*   **Problema:** Frases longas que contêm explicações intermediárias e podem causar fadiga ao leitor.
*   **Regra:** Identificar frases que contêm entre 20 e 30 palavras.
*   **Solução:** Sugerir a divisão da frase em duas partes ou a simplificação de termos.

### 1.5. Frases Muito Difíceis de Ler (Destaque Vermelho)
*   **Problema:** Frases excessivamente longas (mais de 30 palavras) ou com estruturas gramaticais excessivamente complexas (múltiplas orações coordenadas e subordinadas misturadas).
*   **Regra:** Identificar frases com mais de 30 palavras ou lógica confusa.
*   **Solução:** Propor uma reescrita completa da frase, priorizando a ordem direta (Sujeito + Verbo + Objeto).

---

## 2. Cálculo de Legibilidade

Para determinar o nível de legibilidade no português do Brasil, utilizaremos a fórmula adaptada do **Índice de Facilidade de Leitura de Flesch (IFLF)**:

$$\text{IFLF} = 248.835 - (1.015 \times \text{média de palavras por frase}) - (84.6 \times \text{média de sílabas por palavra})$$

### Classificação do IFLF para o Português:
*   **75 a 100:** Muito Fácil (Nível de leitura: Ensino Fundamental I / Até a 4ª série). Ideal para qualquer leitor.
*   **50 a 75:** Fácil (Nível de leitura: Ensino Fundamental II / 5ª a 8ª série). Linguagem cotidiana padrão.
*   **25 a 50:** Difícil (Nível de leitura: Ensino Médio ou Universitário). Textos acadêmicos ou especializados.
*   **0 a 25:** Muito Difícil (Nível de leitura: Acadêmico / Pós-graduação). Textos extremamente técnicos ou herméticos.

A meta para textos de consumo geral é obter um índice **acima de 60** (equivalente a uma leitura de fácil compreensão).

---

## 3. Estrutura do Relatório da Skill

Ao analisar um texto, a skill deve retornar as informações de forma estruturada:

1.  **Resumo de Legibilidade e Métricas:** Uma tabela contendo estatísticas (palavras, frases, parágrafos) e o score IFLF obtido.
2.  **Painel de Estilo (Contagem e Metas):** Comparação entre os limites recomendados baseados no tamanho do texto e os encontrados.
3.  **Texto Mapeado com Anotações:** O texto original com as anotações visuais (usando marcas de formatação em markdown para legendar os pontos críticos).
4.  **Lista de Recomendações:** Detalhamento individual de cada alteração recomendada.
5.  **Versão Sugerida Reescrita:** O texto revisado de acordo com as regras Hemingway para comparação direta.
