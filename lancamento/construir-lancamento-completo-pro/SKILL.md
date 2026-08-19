---
name: construir-lancamento-completo-pro
description: Orquestra a construção completa de um lançamento digital em nove fases, da oportunidade de mercado ao arsenal de anúncios, com briefing, pesquisa, posicionamento, Big Idea, produto, oferta, evento, mensagem central, calendário de 84 conteúdos e 100 criativos. Use quando o usuário pedir lançamento completo, estratégia de lançamento ponta a ponta, plano de campanha Pro, documento mestre de lançamento ou integração dos artefatos de pesquisa, avatar, oferta, evento e mídia. Também use para retomar, auditar ou expandir uma fase de um lançamento criado por esta skill.
---

# Construção de Lançamento Completo — Versão Pro

## Objetivo

Construir um sistema de lançamento específico, executável e rastreável em nove fases. Trabalhar de forma sequencial, reaproveitar pesquisas e artefatos existentes e obter aprovação explícita nos checkpoints antes de avançar.

Não tratar persuasão como licença para fabricar fatos, explorar vulnerabilidades ou retirar autonomia. Criar demanda por clareza de valor, evidência, relevância e adequação. Recusar pedidos de fraude publicitária — como depoimentos fictícios apresentados como reais, alegações inventadas ou escassez falsa — e oferecer uma alternativa honesta e executável.

## Roteamento inicial

1. Identificar se o pedido é para:
   - iniciar um lançamento completo;
   - retomar uma fase;
   - revisar um documento mestre existente;
   - produzir um artefato específico dentro do lançamento.
2. Ler `references/briefing.md`.
3. Inventariar os arquivos fornecidos e marcar cada item como `fornecido`, `parcial`, `ausente` ou `não aplicável`.
4. Se faltar contexto indispensável, orientar o usuário sobre como usar a skill e solicitar apenas as informações mínimas da próxima fase. Não preencher lacunas com suposições apresentadas como fatos.
   - Antes de concluir que não há pesquisa, aproveitar evidências informais disponíveis, como entrevistas, atendimentos, mensagens, dúvidas de vendas e feedback de clientes, registrando suas limitações.
5. Se houver material suficiente, criar ou atualizar o manifesto do projeto conforme `references/artifact-contracts.md`.

## Como orientar quando não houver pesquisa

Explicar de forma curta:

> Para usar esta skill, envie o que tiver de: briefing do especialista, avatar ou respostas de pesquisa, pesquisa de mercado, produto atual, histórico de lançamentos e recursos disponíveis. Se ainda não houver pesquisa, posso começar com um briefing mínimo e separar claramente hipóteses de fatos; antes de fechar posicionamento, promessa e mídia, será necessário validar essas hipóteses com clientes ou dados reais.

Em seguida, perguntar somente pelo bloco mínimo descrito em `references/briefing.md`. Não pedir os seis arquivos novamente se parte das informações já estiver na conversa.

## Fluxo obrigatório

Ler `references/pipeline.md` antes de produzir qualquer fase. Executar na ordem:

1. oportunidade lucrativa e lacuna de mercado;
2. posicionamento e categoria;
3. Big Idea, promessa e mecanismo;
4. arquitetura do produto;
5. oferta e redução de risco;
6. evento principal;
7. mensagem central integrada;
8. aquecimento editorial de 28 dias e 84 conteúdos;
9. sistema de anúncios e 100 criativos.

Em cada fase:

1. Confirmar entradas e dependências.
2. Separar `evidências`, `inferências`, `hipóteses` e `decisões`.
3. Produzir o artefato no contrato indicado.
4. Aplicar as regras de `references/integrity.md`.
5. Registrar limitações, riscos, responsáveis e próximo teste.
6. Apresentar o checkpoint com opções: aprovar, revisar, aprofundar ou pausar.
7. Aguardar aprovação explícita antes da fase seguinte, salvo se o usuário tiver solicitado expressamente uma auditoria sem alterações.

## Integração com skills especializadas

Quando disponíveis no mesmo conjunto de skills, usar os artefatos abaixo como módulos especializados, sem exigir que o usuário os execute novamente:

- `extrair-perfil-aspiracional`: perfil psicográfico agregado e linguagem da audiência;
- `construir-sistema-anti-objecao`: mapa de objeções e respostas;
- `criar-ancoras-emocionais`: drivers éticos e memoráveis;
- `criar-provis`: demonstrações visuais verificáveis;
- `estruturar-pre-pitch`: transição entre conteúdo e oferta;
- `planejar-aquecimento-aspiracional` ou `planejar-aquecimento-indignacao`: plano editorial;
- `analisar-aula`: auditoria das aulas e do pitch.

Se uma skill não estiver disponível, executar o contrato mínimo correspondente descrito em `references/artifact-contracts.md`. Não bloquear o lançamento por ausência de um módulo auxiliar.

## Regras de produção

- Adaptar profundidade ao material recebido; não inflar páginas para atingir volume artificial.
- Citar a origem de números, pesquisas, depoimentos e comparações.
- Rotular exemplos fictícios como exemplos e nunca como prova.
- Produzir calendários e anúncios em lotes revisáveis para evitar repetição e inconsistência.
- Na fase 8, validar primeiro uma semana-modelo; depois completar os 28 dias.
- Na fase 9, apresentar um mapa das categorias e um primeiro lote de 10; produzir os demais em lotes de 10 após aprovação.
- Manter IDs estáveis: `F1-*` a `F9-*`, `C001` a `C084` para conteúdos e `AD001` a `AD100` para anúncios.
- Se o usuário fornecer metas conflitantes, registrar o conflito e pedir decisão no checkpoint pertinente.

## Validação

Antes de declarar o lançamento completo:

1. Salvar ou montar um manifesto JSON conforme `references/artifact-contracts.md`.
2. Executar:

```powershell
python scripts/validate_launch.py caminho\launch-manifest.json
```

3. Corrigir erros; apresentar avisos relevantes ao usuário.
4. Verificar manualmente coerência entre avatar, promessa, mecanismo, produto, oferta, evento, conteúdo e anúncios.
5. Entregar sumário executivo, índice de artefatos, cronograma, riscos, decisões pendentes e plano de medição.

## Formato da resposta por checkpoint

Usar esta ordem:

1. **Decisão proposta** — síntese objetiva.
2. **Base** — evidências e hipóteses usadas.
3. **Artefato da fase** — conteúdo estruturado.
4. **Riscos e validações** — o que ainda precisa ser provado.
5. **Checkpoint** — `Aprovar`, `Revisar`, `Aprofundar` ou `Pausar`.

Nunca anunciar conclusão total enquanto houver fase obrigatória sem aprovação ou erro no manifesto.
