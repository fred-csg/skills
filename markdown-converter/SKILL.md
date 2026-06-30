---
name: markdown-converter
description: Use esta skill sempre que o usuário pedir para extrair texto de documentos ou PDFs, limpar erros de OCR, converter arquivos ricos para Markdown, ou preparar documentos para sistemas de RAG (Retrieval-Augmented Generation). Ela processa arquivos usando marker-pdf ou docling, limpa formatações indesejadas e usa LLM para corrigir OCR e remover tabelas/bibliografias.
---

# Markdown Converter para RAG

Esta skill automatiza a extração de texto de documentos (como PDFs) e os converte em arquivos Markdown limpos, bem estruturados e semanticamente otimizados para sistemas RAG. Ela atua como um filtro de ruídos para garantir que apenas contexto de alto valor seja vetorizado.

## Formato de Entrada e Acionamento

A skill deve ser ativada quando o usuário quiser processar um documento para RAG, limpar texto extraído via OCR ou gerar um markdown limpo a partir de um PDF/documento.

O seu objetivo principal será entender as opções pedidas pelo usuário, orquestrar a extração do texto bruto, limpar esse texto e devolver os metadados do processamento.

## Passo a Passo da Execução

### 1. Validação da Entrada e Planejamento
Identifique o caminho do arquivo alvo. Entenda quais opções de limpeza o usuário solicitou (ex: remover tabelas, corrigir OCR, remover referências). Se as opções não forem explícitas, assuma o padrão: realizar correção de OCR e remover seções inúteis para inferência de RAG (como bibliografias).

### 2. Parsing Nativo
Execute o parsing do documento usando comandos no terminal. 
Se a ferramenta for `marker-pdf` (marker_single) ou `docling`, rode o comando apropriado para extrair o Markdown bruto. 

*Estratégia de Resiliência:* Se ocorrerem erros na extração nativa (ex: falta de VRAM ou binário não encontrado), tente usar métodos de extração em Python (como `pymupdf` ou pdfminer) instalando dependências temporárias se necessário. Avise o usuário caso o documento seja puramente escaneado e dependa muito da precisão do motor de visão do OCR.

### 3. Chunking e Pipeline de Purificação (Filtro Semântico)
Leia o conteúdo Markdown gerado. Se o documento for longo, processe-o em partes (chunks moderados, ex: 2.000 a 3.000 palavras por vez).

- **Fase A (Rápida - Opcional via Script):**
  Se preferir, escreva e execute um pequeno script Python usando Regex para remover paginações soltas, números repetidos ou cabeçalhos fixos óbvios do documento.
  
- **Fase B (Limpeza Semântica com o seu LLM):**
  Você mesmo fará o papel do corretor. Aplique seu modelo para corrigir pequenos erros de OCR, omita tabelas numéricas desconexas e ignore bibliografias ou índices irrelevantes, devolvendo apenas a informação de alto valor. Concentre-se em padronizar os títulos e a semântica.

### 4. Reconstrução
Junte as partes do documento processado de volta em um único arquivo de saída.

### 5. Formato de Saída
Salve o arquivo final em um diretório especificado pelo usuário (ex: `./tmp/doc_limpo.md`) ou com um sufixo `_clean.md` ao lado do arquivo original.

Seu retorno (a última mensagem que você vai gerar no chat) DEVE ser OBRIGATORIAMENTE um bloco JSON contendo os metadados do processamento, conforme a estrutura abaixo:

```json
{
  "status": "success",
  "original_file": "documento.pdf",
  "output_file": "/tmp/processado/documento_clean_v1.md",
  "metadata": {
    "words_extracted": 3450,
    "processing_time_sec": 45
  }
}
```

Evite explicações verbosas após imprimir o JSON final.
