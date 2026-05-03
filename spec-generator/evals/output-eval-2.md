# 1. Descrição da Skill
A skill **Changelog Generator** atua como um assistente automatizado de release. Ela se conecta ao repositório GitHub do usuário, extrai o histórico de commits desde a última release (ou de um intervalo de tempo especificado), classifica as mudanças e gera um documento de *Changelog* bem formatado e pronto para ser publicado em plataformas como GitHub Releases, Slack ou documentação interna.

# 2. Requisitos Funcionais
- **Inputs Esperados**: Nome/URL do repositório, opcionalmente a branch, e o critério de intervalo (ex: "últimos 30 dias", "desde a tag v1.0.0").
- **Integração GitHub**: Deve utilizar a API do GitHub (via ferramentas MCP como `github-mcp-server`) para buscar os commits e tags.
- **Processamento/Classificação**: Analisar as mensagens de commit, identificando o tipo de alteração (Features, Bug Fixes, Melhorias de Performance, Chores).
- **Sumarização (NLP)**: Utilizar LLM para agrupar commits similares ou reescrever mensagens puramente técnicas ("fix typo") para uma linguagem voltada a usuário ou negócio, se solicitado.

# 3. Requisitos de Processamento
- **Tipo do Problema**: Integração de API, Classificação de Texto (NLP) e Formatação de Dados.
- **Complexidade**: Intermediária.
- **Natureza do Processamento**: Predominantemente síncrono. Pode exigir paginação em caso de centenas de commits, o que requer processamento iterativo.

# 4. Motor / Tecnologia Recomendada
- **Integração de Dados**: MCP `github-mcp-server` para ler dados diretamente sem a necessidade de gerenciar tokens e chamadas REST puras.
- **Motor de IA**: LLM para analisar semântica das mensagens de commit e classificá-las caso não utilizem um formato padronizado como Conventional Commits.
- **Formatação**: Templates Markdown para estruturação da saída final.

# 5. Arquitetura Sugerida
1. **Interpretação do Input**: Extrair repositório e intervalo.
2. **Recuperação de Dados**: 
   - Consultar as últimas tags via API.
   - Listar todos os commits no intervalo desejado (ex: da penúltima tag até a HEAD).
3. **Pré-processamento**: Filtrar merges automáticos e commits vazios/irrelevantes.
4. **Enriquecimento com IA**: Enviar o lote de mensagens ao LLM para agrupamento (ex: separar bugs de features) e reescrita de mensagens pouco claras.
5. **Geração**: Aplicar os dados processados em um template Markdown predefinido.
6. **Entrega**: Apresentar o changelog ao usuário ou escrevê-lo em um arquivo (ex: `CHANGELOG.md`).

# 6. Estratégias de Resiliência
- **Fallbacks para API**: Em caso de limite de requisições excedido no GitHub, informar ao usuário que precisará esperar, ou tentar usar paginação cuidadosa.
- **Commits Mal Formatados**: Se os commits forem todos mensagens como "update" ou "fix", a skill deve alertar o usuário que a qualidade do changelog será baixa e sugerir olhar os diffs (embora custoso).
- **Sem Tags Anteriores**: Se o repositório não possuir tags, assumir por padrão os commits dos últimos 14 dias ou solicitar a janela de tempo ao usuário.

# 7. Formato de Entrada
Um prompt textual ou briefing como:
`Gere um changelog para o repositório org/repo desde a tag v1.2.0. Agrupe em 'Novidades' e 'Correções'.`
Variáveis extraídas:
- `owner`: org
- `repo`: repo
- `since`: tag v1.2.0

# 8. Formato de Saída
Um artefato ou texto em formato Markdown estruturado:
```markdown
## [Versão/Data]

### ✨ Novidades
- Sumário de nova feature 1 ([hash])
- Sumário de nova feature 2 ([hash])

### 🐛 Correções
- Sumário do bug resolvido ([hash])
```

# 9. Considerações de Escalabilidade
- Repositórios com alto volume de commits entre releases (ex: 500+ commits) podem estourar a janela de contexto ou os limites de paginação. Nesses casos, a skill deve limitar a análise aos 100 commits mais recentes ou processá-los em lotes (chunks) menores antes de fazer a consolidação final.

# 10. Possíveis Extensões Futuras
- **Integração com Issues**: Adicionar o link automático para as issues fechadas no respectivo período.
- **Formatos Múltiplos**: Exportar não apenas para Markdown, mas para formato JSON (para sistemas de release automatizados) ou texto condensado para Slack/Discord.
- **Análise de Diffs**: Ao invés de apenas ler as mensagens de commit, analisar os diffs do código para descrever a real mudança técnica (útil quando mensagens de commit são pobres).
