---
name: revisor-hemingway
description: Skill de analise e revisao de textos inspirada no Hemingway Editor, focando em clareza, concisao e legibilidade para o portugues do Brasil.
---

# Skill Revisor Hemingway

Especificacao de Referencia: [revisor_hemingway_spec.md](references/revisor_hemingway_spec.md)

Esta skill capacita o agente a analisar a legibilidade, clareza e estilo de textos em portugues do Brasil, aplicando os principios de escrita simplificada do Hemingway Editor.

## Quando Ativar esta Skill
Esta skill deve ser ativada sempre que o usuario solicitar:
*   Revisao de textos, artigos, e-mails ou documentacoes.
*   Melhoria de clareza, concisao ou legibilidade.
*   Uso de termos como "revisao Hemingway", "analise de legibilidade" ou "simplificar escrita".

## Instrucoes de Analise

Ao receber um texto para revisao, siga rigorosamente os passos abaixo para gerar o relatorio:

### 1. Metricas Gerais e Legibilidade
*   **Contagem:** Calcule a quantidade total de palavras, frases e paragrafos.
*   **Calculo IFLF:** Calcule o indice aproximado de Facilidade de Leitura de Flesch (IFLF) para o portugues utilizando a formula:
    $$IFLF = 248.835 - (1.015 \times \text{media de palavras por frase}) - (84.6 \times \text{media de silabas por palavra})$$
*   **Classificacao do Indice:**
    *   **75 a 100:** Muito Facil (Ate 4a serie / Ensino Fundamental I)
    *   **50 a 75:** Facil (5a a 8a serie / Ensino Fundamental II)
    *   **25 a 50:** Dificil (Ensino Medio ou Universitario)
    *   **0 a 25:** Muito Dificil (Academico)

### 2. Analise de Estilo (Metricas Hemingway)
Avalie o texto segundo as 5 categorias de estilo. O limite recomendado e calculado proporcionalmente ao tamanho do texto (T = total de palavras):

1.  **Adverbios e Enfraquecedores (Destaque Azul 🟦):**
    *   Limite recomendado: No maximo $T / 150$ adverbios.
    *   Ocorrencia: Adverbios terminados em "-mente" ou termos redundantes (muito, realmente, bastante, excessivamente).
    *   Solucao: Remover ou trocar por verbos mais expressivos.
2.  **Voz Passiva (Destaque Verde 🟩):**
    *   Limite recomendado: No maximo $T / 150$ ocorrencias.
    *   Ocorrencia: Verbo auxiliar + participio + agente da passiva (ex: "foi definido por", "sao enviados pelo").
    *   Solucao: Alterar para voz ativa.
3.  **Alternativas Simples (Destaque Roxo 🟪):**
    *   Ocorrencia: Palavras rebuscadas ou prolixas (ex: "utilizar", "viabilizar", "efetuar", "posteriormente").
    *   Solucao: Oferecer sinonimos simples (ex: "usar", "fazer", "depois").
4.  **Frases Dificeis de Ler (Destaque Amarelo 🟨):**
    *   Limite recomendado: Menos de 15% das frases do texto.
    *   Ocorrencia: Frases longas, com 20 a 30 palavras, que necessitam de atencao redobrada.
    *   Solucao: Dividir ou simplificar oracoes.
5.  **Frases Muito Dificeis de Ler (Destaque Vermelho 🟥):**
    *   Limite recomendado: 0 frases.
    *   Ocorrencia: Frases com mais de 30 palavras ou com sintaxe confusa e multiplas subordinacoes.
    *   Solucao: Reescrever na ordem direta (Sujeito + Verbo + Objeto).

---

## Formato de Saida do Relatorio

A resposta da skill deve seguir este formato em Markdown:

### 📊 Painel de Legibilidade e Metricas
*   **Indice Flesch (IFLF):** `[Valor do Score]` - **`[Classificacao]`**
*   **Total de Palavras:** `[Contagem]` | **Frases:** `[Contagem]` | **Paragrafos:** `[Contagem]`

| Categoria | Encontrado | Meta Recomendada | Status |
| :--- | :---: | :---: | :---: |
| 🟦 Adverbios | `[Qtd]` | `[Meta]` ou menos | `[OK / Ajustar]` |
| 🟩 Voz Passiva | `[Qtd]` | `[Meta]` ou menos | `[OK / Ajustar]` |
| 🟪 Alternativas Simples | `[Qtd]` | - | `[Ajustar se > 0]` |
| 🟨 Frases Dificeis | `[Qtd]` | `[Meta]` ou menos | `[OK / Ajustar]` |
| 🟥 Frases Muito Dificeis | `[Qtd]` | 0 | `[OK / Ajustar]` |

### 🔍 Texto Mapeado (Marcacoes Visuais)
Exiba o texto original aplicando os emojis de cores correspondentes imediatamente antes ou contornando os termos identificados.
*   Use `==texto== 🟨` para frases dificeis.
*   Use `***texto*** 🟥` para frases muito dificeis.
*   Use `**termo** 🟩` para voz passiva.
*   Use `*termo* 🟦` para adverbios.
*   Use `~~termo~~ 🟪` para palavras complexas.

### 💡 Recomendacoes de Melhoria
Apresente uma lista com as correcoes recomendadas divididas pelas categorias identificadas no texto.

### ✍️ Sugestao de Reescrita (Versao Hemingway)
Apresente a versao totalmente reescrita e otimizada do texto, aplicando todas as correcoes de clareza, concisao e legibilidade. Recalcule o novo Indice Flesch para demonstrar a evolucao.
