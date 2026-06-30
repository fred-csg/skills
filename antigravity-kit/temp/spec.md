# 1. Descrição da Skill
A skill **"Markdown Converter para RAG"** tem como objetivo processar documentos (especialmente PDFs e formatos ricos) e convertê-los em arquivos Markdown limpos, bem estruturados e semanticamente otimizados para sistemas de RAG (*Retrieval-Augmented Generation*). Ela automatiza a extração inicial de texto, aplica correção em erros de OCR e atua como um filtro de ruídos — removendo referências bibliográficas, tabelas e cabeçalhos não essenciais — para garantir que apenas o contexto de alto valor seja vetorizado e consumido pela IA.

# 2. Requisitos Funcionais
- **Extração de Texto Bruto**: Utilizar motores avançados como `marker-pdf` ou `docling` para ler a estrutura do arquivo original e gerar o Markdown inicial preservando os cabeçalhos.
- **Enriquecimento e Limpeza**:
  - Identificar e corrigir possíveis "alucinações" e falhas de OCR (reconhecimento de caracteres).
  - Silenciar/remover seções inúteis para inferência (ex: bibliografia, índices, marcações de copyright, tabelas numéricas desconexas ou irrelevantes).
- **Armazenamento**: Gravar o arquivo final processado diretamente em um diretório temporário do projeto (ex: `.tmp/` ou `/tmp/`).
- **Padronização Semântica**: Consolidar títulos e quebras de linha para garantir que o *chunking* futuro durante a fase de RAG seja o mais preciso possível.

# 3. Requisitos de Processamento
- **Tipo do Problema**: Extração de Dados, Processamento de Linguagem Natural (NLP) e Conversão de Documentos.
- **Complexidade**: Intermediária-Avançada. A integração de ferramentas como `marker-pdf` com fases adicionais de validação por IA exige bom gerenciamento de recursos.
- **Processamento**: Deve ser preferencialmente **assíncrono**, já que o tempo de processamento de um livro ou paper científico pode levar desde alguns segundos até minutos, dependendo do hardware e uso de modelos para a limpeza do OCR.

# 4. Motor / Tecnologia Recomendada
- **Motores de Extração**: 
  - `marker-pdf` (excelente para PDFs acadêmicos e fórmulas).
  - `docling` (forte competidor para múltiplos formatos corporativos e layouts mistos).
- **Limpeza de OCR / Filtro Semântico**: 
  - Uso direcionado de um LLM rápido e barato (como Gemini 1.5 Flash ou Claude 3.5 Haiku) focado em tarefas de revisão de texto em lotes.
- **Scripts Nativos**: Regras simples de Regex (Python) para eliminação óbvia de cabeçalhos repetitivos sem gastar tokens de LLM.

# 5. Arquitetura Sugerida
1. **Ingestão**: A skill recebe o arquivo ou caminho de origem.
2. **Parsing Nativo**: Executa o `docling` ou `marker-pdf` criando um arquivo de Markdown bruto e um arquivo de metadados de layout.
3. **Chunking Temporário**: Divide o Markdown bruto em blocos de tamanho moderado (ex: 2.000 tokens) para evitar limite de contexto.
4. **Pipeline de Purificação**:
   - Fase A (Rápida): Expressões Regulares removem paginação solta e formatações indesejadas.
   - Fase B (Semântica): Passa os blocos pelo LLM com um prompt estrito: *"Corrija erros de OCR. Omita tabelas ou lista de referências. Retorne apenas o Markdown limpo"*.
5. **Reconstrução**: Concatena todos os blocos limpos, restaurando o documento.
6. **Entrega**: Salva o artefato final (`.md`) na pasta temporária.

# 6. Estratégias de Resiliência
- **Fallback de Motor**: Se `marker-pdf` falhar (devido a falta de VRAM ou falha no binário), realizar fallback imediato para o `docling` ou mesmo para o PyMuPDF para extração de texto básico sem formatação.
- **Fallback de LLM**: Se a API de correção de OCR der *timeout* ou falhar em um chunk específico, manter o texto original do OCR do chunk em questão para não interromper todo o documento.
- **Validação de Entrada**: Se um PDF for escaneado e consistir apenas em imagens sem OCR nativo, avisar o usuário proativamente que a qualidade dependerá integralmente do motor de visão computacional da extração.

# 7. Formato de Entrada
- Espera-se receber um JSON contendo, no mínimo, o caminho do arquivo:
```json
{
  "file_path": "/caminho/absoluto/ou/relativo/documento.pdf",
  "options": {
    "remove_tables": true,
    "fix_ocr": true
  }
}
```

# 8. Formato de Saída
- O processamento principal ocorre em disco, então o arquivo final será gravado fisicamente em (exemplo) `./tmp/doc_limpo.md`.
- O retorno (resposta) da skill para o agente chamador deve ser:
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

# 9. Considerações de Escalabilidade
- **Gestão de Memória**: Ferramentas como o `marker` podem exigir bastante VRAM em arquivos grandes. A skill deve processar um documento de forma serial (por lote de páginas) caso identifique um arquivo gigantesco (centenas de páginas).
- **Cache de Processamento**: Gerar um `hash` (MD5/SHA256) do arquivo fonte. Se o mesmo arquivo for solicitado novamente com as mesmas configurações, pular a extração pesada e retornar a cópia temporária do cache, caso ainda exista.

# 10. Possíveis Extensões Futuras
- **Suporte Nativo a Imagens**: Utilizar Modelos de Visão (VLM) para extrair o significado de gráficos presentes no documento e inserir no Markdown a descrição gerada (alt text enriquecido).
- **Frontmatter RAG**: Inserir metadados automáticos no topo do `.md` gerado (via formato YAML/Frontmatter) incluindo título extraído, resumo de 3 linhas e tipo de documento.
- **Limpeza Fina de Equações**: Converter equações mal formatadas para LaTeX limpo, ideal para RAG em base científica.
