---
name: extrair-area-de-conhecimento
description: Conduz e estrutura um “download cerebral” de especialistas por entrevista adaptativa, reunião facilitada, respostas assíncronas, transcrições ou áudio, selecionando aproximadamente 20–25 perguntas relevantes entre nove domínios e três níveis de profundidade. Use quando o usuário pedir extração de conhecimento, mapeamento de expertise, entrevista com especialista, captura de conhecimento tácito, documentação de método, preparação de conhecimento para curso ou infoproduto, processamento de uma reunião de descoberta, continuação de uma sessão de extração ou síntese das respostas de um especialista.
---

# Extração de Área de Conhecimento

## Objetivo

Transformar a experiência de um especialista em conhecimento explícito, ensinável e rastreável. Conduzir uma entrevista confortável, seletiva e progressiva; não aplicar o banco inteiro como questionário obrigatório.

## Escolher o modo

Identificar o modo antes de perguntar:

- **Entrevista ao vivo**: fazer uma pergunta principal por vez, ouvir, sondar e resumir.
- **Assíncrono**: enviar blocos de no máximo 3 perguntas, se o usuário preferir responder aos poucos.
- **Processamento de material**: mapear respostas de transcrição, notas, documentos ou áudio para os domínios; perguntar apenas pelos gaps.
- **Extração focada**: priorizar um processo, produto, técnica ou domínio indicado pelo usuário.
- **Retomada**: ler o estado da sessão e continuar da próxima lacuna, sem repetir perguntas já respondidas.

Quando houver áudio e a interface permitir sua leitura/transcrição, processá-lo em segmentos. Marcar trechos incertos e confirmar nomes, números e termos técnicos. Se não for possível acessar o áudio, pedir a transcrição; nunca fingir que ouviu o arquivo.

## Preparar a sessão

1. Ler `references/protocol.md`.
2. Coletar apenas o contexto inicial necessário: especialista, área, experiência, resultado comprovado, diferencial percebido, público, produto imaginado e transformação desejada.
3. Perguntar objetivo, foco, tempo disponível, formato preferido e profundidade.
4. Definir limites: temas que o especialista não quer abordar, casos a anonimizar e propriedade intelectual que não deve ser registrada.
5. Criar um estado de sessão conforme `references/session-schema.md`.

Aceitar “não sei”, “prefiro não responder”, pausa ou mudança de foco sem pressionar. Anonimizar clientes e terceiros por padrão.

## Selecionar perguntas dinamicamente

Ler `references/question-bank.md` antes de conduzir a entrevista. O arquivo contém 120 perguntas canônicas do prompt-base, não as “200+” mencionadas na introdução original.

Usar aproximadamente 20–25 perguntas principais para uma extração completa. Sondagens curtas não precisam entrar nessa contagem. Para uma extração focada, ajustar a quantidade ao escopo e declarar a meta.

Priorizar nesta ordem:

1. processo core e critérios de decisão;
2. lacunas que impedem explicar ou ensinar o método;
3. conhecimento tácito, automatismos e padrões;
4. casos que testam limites e condições;
5. diferenciação verificável;
6. contexto, relacionamento, otimizações e pontos cegos relevantes ao objetivo.

Após cada resposta:

1. Extrair fatos, sequência, decisão, critério, exceção, exemplo, resultado e termo próprio.
2. Avaliar especificidade, novidade, relevância, confiança e lacunas.
3. Escolher entre aprofundar, cruzar com resposta anterior ou avançar.
4. Fazer no máximo 2 sondagens seguidas antes de oferecer avanço, salvo pedido explícito do especialista.
5. Não repetir uma pergunta já respondida implicitamente; registrar o vínculo ao ID correspondente.

## Conduzir cada rodada

Em entrevista ao vivo, usar este formato:

1. uma frase breve conectando a resposta anterior;
2. uma pergunta clara;
3. se útil, explicar em uma frase o tipo de exemplo procurado;
4. aguardar a resposta.

Não responder pela pessoa, completar histórias, sugerir credenciais ou induzir uma conclusão. Se a resposta estiver genérica, pedir exemplo concreto. Se trouxer uma regra absoluta, testar condições e contraexemplos. Se trouxer intuição, pedir sinais observáveis e como diferencia intuição de viés.

A cada 5 perguntas principais, apresentar:

- descobertas confirmadas;
- inferências a confirmar;
- contradições ou lacunas;
- domínios cobertos;
- próximo foco recomendado;
- opções `Continuar`, `Aprofundar`, `Mudar foco` ou `Pausar`.

## Processar material já existente

Ao receber respostas, notas ou transcrição:

1. Preservar a linguagem original em citações curtas, quando autorizado.
2. Mapear cada trecho a domínio, nível e IDs possíveis.
3. Separar conhecimento explícito, tácito, inferido e hipotético.
4. Identificar contradições sem escolher arbitrariamente uma versão.
5. Gerar perguntas somente para gaps de alto impacto.
6. Registrar a origem por arquivo, página, timestamp ou mensagem quando disponível.

Não apresentar lembranças, opiniões ou casos isolados como eficácia comprovada. Diferenciar experiência do especialista, evidência externa e hipótese pedagógica.

## Encerrar e sintetizar

Parar quando ocorrer um destes critérios:

- 20–25 perguntas principais respondidas e os domínios requeridos estão suficientemente cobertos;
- objetivo focal alcançado;
- retornos marginais baixos;
- limite de tempo atingido;
- especialista pedir pausa ou encerramento.

Ler `references/output-template.md` e produzir o Download Cerebral com:

- mapa executivo da expertise;
- método e etapas;
- regras de decisão e critérios de passagem;
- heurísticas, sinais, automatismos e conhecimento tácito;
- casos, exceções, falhas e recuperação;
- diferenciais e condições de validade;
- SOPs, checklists, árvores de decisão ou exemplos ensináveis;
- glossário e linguagem própria;
- matriz de evidências e confiança;
- gaps, contradições e perguntas futuras;
- oportunidades de produto ou ensino, quando solicitadas.

Apresentar a síntese ao especialista para correção. Não considerar um insight inferido como validado sem confirmação.

## Validar o estado

Executar antes de declarar a sessão concluída:

```powershell
python scripts/validate_session.py caminho\session.json
```

Corrigir erros e reportar avisos relevantes. Uma extração pode terminar como `paused` ou `needs_validation`; não forçar o status `completed`.
