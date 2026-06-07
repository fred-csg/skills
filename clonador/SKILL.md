---
name: clonador
description: "Executa o processo de clonagem de personalidade de um expert em 4 etapas sequenciais. Mapeia a essência psicológica (DNA), decodifica o padrão de estilo textual (engenharia reversa), cria a modelagem do clone digital e gera o prompt de instruções final para um GPT personalizado em primeira pessoa. Certifique-se de usar esta skill sempre que o usuário mencionar 'clonar o expert', 'criar um clone digital do expert', 'fazer engenharia reversa do estilo do expert', 'gerar prompt para gpt do expert', 'mapear dna do expert' ou realizar análises da base de conhecimento de personalidade do expert."
---

# Skill de Clonagem de Personalidade (Clonador)

Esta skill guia o agente no processo de clonagem da essência psicológica e estilo textual de um expert a partir de um corpus documental fornecido na pasta `base-de-conhecimento/` do projeto. O processo é dividido em 4 etapas sequenciais que devem ser executadas obrigatoriamente nesta ordem, pois cada passo utiliza as análises geradas pelas etapas anteriores.

---

## 📋 Pré-requisitos e Estrutura do Projeto

Antes de iniciar, certifique-se de que a raiz do projeto atual contém a seguinte estrutura básica:
- `base-de-conhecimento/`: Pasta contendo o material bruto do expert (transcrições, textos, livros, etc.).
- `markdown/`: Pasta onde serão salvos os arquivos gerados em cada passo.

---

## 🚀 Fluxo Operacional de Execução

Para cada etapa, você deve seguir este protocolo de execução:

### 1. Preparar os Insumos do Passo
Execute o script utilitário em Python fornecido com esta skill, substituindo `<N>` pelo número do passo atual (1 a 4):
```powershell
python G:\SKILLS\clonador\scripts\preparar_passo.py --passo <N>
```
Este script irá validar a existência dos arquivos necessários e consolidar todas as fontes relevantes (base de conhecimento e relatórios de etapas anteriores) em um único arquivo temporário:
`markdown/insumos_passo_<N>.txt.tmp`

### 2. Ler as Diretrizes e Insumos
1. Abra e leia as diretrizes e regras originais do passo em questão na pasta de referências desta skill:
   - Passo 1: [passo1-extracao.md](file:///G:/SKILLS/clonador/references/passo1-extracao.md)
   - Passo 2: [passo2-padrao-linguistico.md](file:///G:/SKILLS/clonador/references/passo2-padrao-linguistico.md)
   - Passo 3: [passo3-clonagem.md](file:///G:/SKILLS/clonador/references/passo3-clonagem.md)
   - Passo 4: [passo4-prompt-gpt.md](file:///G:/SKILLS/clonador/references/passo4-prompt-gpt.md)
2. Leia o arquivo consolidado temporário `markdown/insumos_passo_<N>.txt.tmp` para obter todo o contexto textual de entrada para a análise.

### 3. Realizar a Análise e Gravar o Resultado
Execute o processamento cognitivo profundo do texto e gere o arquivo markdown de saída especificado para o passo na pasta `markdown/` do projeto atual:
- Passo 1: Salve como `markdown/extracao.md`
- Passo 2: Salve como `markdown/padrao-linguistico.md`
- Passo 3: Salve como `markdown/clone-digital.md`
- Passo 4: Salve como `markdown/prompt-gpt.txt`

### 4. Limpar os Arquivos Temporários
Após a geração do relatório correspondente e confirmação de sua gravação completa, execute o script utilitário com o parâmetro `--limpar` para apagar os arquivos `.tmp` temporários gerados:
```powershell
python G:\SKILLS\clonador\scripts\preparar_passo.py --limpar
```

---

## 🔍 Descrição Detalhada dos Passos

### Passo 1: Extrator de DNA do Expert
- **Objetivo**: Analisar os materiais brutos da `base-de-conhecimento` para mapear a essência psicológica e os padrões comportamentais do expert nos 9 domínios descritos na referência do passo 1.
- **Entrada**: Apenas os arquivos brutos da pasta `base-de-conhecimento/`.
- **Saída**: O arquivo `markdown/extracao.md` (Manual de Personificação).

### Passo 2: Engenharia Reversa Textual
- **Objetivo**: Analisar com precisão nanométrica o estilo de escrita, vocabulário, estruturas frasais, loops abertos, padrões de pontuação e gatilhos de persuasão empregados pelo expert.
- **Entrada**: Arquivos brutos de `base-de-conhecimento/` + arquivo `markdown/extracao.md`.
- **Saída**: O arquivo `markdown/padrao-linguistico.md` (Relatório Forense de Estilo).

### Passo 3: Criação de Clone Digital
- **Objetivo**: Sintetizar o perfil de personalidade, o sistema de crenças e valores, os domínios de conhecimento, motivações e o contexto biográfico para modelar o comportamento reativo e criar exemplos de diálogo consistentes.
- **Entrada**: Arquivos brutos de `base-de-conhecimento/` + `markdown/extracao.md` + `markdown/padrao-linguistico.md`.
- **Saída**: O arquivo `markdown/clone-digital.md` (Modelo do Clone Digital).

### Passo 4: Instruções para GPT Personalizado
- **Objetivo**: Criar um prompt consolidado contendo entre 7.500 e 8.000 caracteres para ser configurado como instruções de um GPT Personalizado do expert. O prompt deve referenciar os arquivos de conhecimento do projeto e ser redigido em primeira pessoa, sob a persona e o nome do próprio expert.
- **Entrada**: Arquivos brutos de `base-de-conhecimento/` + todos os markdowns gerados anteriormente na pasta `markdown/`.
- **Saída**: O arquivo `markdown/prompt-gpt.txt` (Instruções em 1ª Pessoa).
