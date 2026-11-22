---
name: "clone-em-acao-wan-seedance"
description: "Gerar vídeos do clone da Andreia em ação (movimento, produto na mão, UGC, tour, vários ambientes) com Wan/Seedance/Veo via Kairogen, Syntex ou wan.video."
---

# Clone em ação — Wan / Seedance / Veo

Para vídeos em que o clone anda, segura produto, muda de ambiente ou a câmera se move. Aqui não existe avatar salvo: a cada geração vão as referências (imagem + áudio) e um prompt. Operar pelo navegador da Andreia (Claude in Chrome). Roteiro e briefing vêm de `videos-com-avatar`.

## 1. Modelo e ferramenta
- Modelo ≠ ferramenta. O modelo precisa aceitar imagem + ÁUDIO de referência para clonar a voz.
- Wan 3.0 ou superior: padrão. Bem mais barato (≈48 créditos por 20 s na Kairogen, contra ≈271 no Seedance 2.5) e tão bom quanto.
- Seedance 2.x: física e consistência excelentes. Mais caro, às vezes erra palavras ou ignora o apresentador.
- Veo 3.1 (Google Flow): cenas de 8 s, vozes padrão (trocar depois no ElevenLabs Voice Changer). Lite ≈ 10 créditos, Quality ≈ 100.
- Onde usar: Kairogen (brasileira, cartão nacional, tem Wan e Seedance), Syntex (agregador amplo), Higgsfield, wan.video (só Wan). Agregadores são práticos para testar, mas cobram mais por geração e demoram mais.
- Use sempre a versão mais nova do modelo disponível.

## 2. Referências
### 2.1 Ficha de personagem (uma vez por pessoa ou figurino)
No ChatGPT, com fotos dela de frente, de lado e em pé (boa luz):
> "Crie uma folha de personagem ultrarrealista 16:9 usando todas as fotos enviadas como referência. Preserve fielmente rosto, proporções, cabelo, textura real da pele e características únicas. Organize 4 vistas: rosto de frente, perfil esquerdo 90°, perfil direito 90° e corpo inteiro de frente, cortado do pescoço para cima, sem mostrar a cabeça. Mantenha roupas e aparência idênticas nas 4 vistas. Fundo cinza-claro uniforme, iluminação profissional de estúdio, nitidez máxima. Sem textos."
- Sem foto em pé, remova a parte do corpo inteiro.
- Confira o BIOTIPO com atenção: a IA tende a alterar o corpo, e isso incomoda. Se mudar, regere reforçando o biotipo.

### 2.2 Áudio de voz
- ~12–14 s, NUNCA acima de 15 s (as ferramentas rejeitam). Gravado com a entonação desejada no vídeo: animada, não lenta.
- Serve só de base de voz. O texto falado vai no prompt.

### 2.3 Outras imagens
Produto, fachada, cômodos, loja, roupa. Uma imagem por elemento. Fotos reais e nítidas.

## 3. Prompt de ação (método clone-prompt do curso)

### 3.1 Briefing mínimo
Leia o pedido e os anexos antes de perguntar. Pergunte só o que faltar, em até 3 perguntas agrupadas:
1. Estilo do vídeo (selfie, unboxing, provador, demonstração, apresentando um lugar) e qual produto ou local.
2. Quais referências vão ser usadas: pessoa, produto, ambiente, áudio.
3. Duração, e se ela já tem a fala ou se eu escrevo.
- Se ela delegar as escolhas: 15 s, 9:16, PT-BR, e aviso em uma linha.
- Pergunte o tom só se a ambiguidade mudar o resultado (por exemplo, tour contemplativo versus anúncio).
- Não faça o prompt final com lacunas.

### 3.2 Mapa de referências
- @img1, @img2... na ordem em que vão ser anexadas; @audio1 e @video1 por modalidade. Cada uma com função explícita: pessoa, produto, fachada, sala...
- Distinga o que foi RECEBIDO do que está PLANEJADO. Nunca diga que analisei um arquivo que ainda não vi. Não invente anexos.
- Produto, objeto ou imóvel: pedir máxima fidelidade de forma, proporções, materiais, cores e disposição. Não inventar, remover ou deslocar detalhes, nem presumir ligação entre cômodos.
- Várias fotos da mesma pessoa: declarar que são a mesma identidade.

### 3.3 Roteiro e interpretação
1. Escolha o formato pela intenção (lista na seção 5) e a reação que quer provocar. Abertura com motivo para continuar → desenvolvimento que cumpre a promessa → convite coerente. Não preencher tempo com "essa é a sala, essa é a varanda".
2. Use apenas fatos fornecidos ou visíveis. Com poucos fatos, convide o espectador a observar, escolher ou imaginar ("Já imaginou como você organizaria esse espaço?"). Nunca invente metragem, benefício, desconto, depoimento ou escassez.
3. Escreva a fala PRIMEIRO e depois reparta os tempos. Conte as palavras pronunciadas (números e siglas por extenso) no total E em cada trecho, usando as faixas de `videos-com-avatar`.
4. Fala curta demais: enriqueça com conteúdo pertinente ou encurte a janela de fala e deixe imagem e som no resto. NUNCA mande "falar devagar" para preencher. Fala longa demais: edite (com aval), redistribua ou divida em mais cenas.
5. Em vídeo comercial, a fala começa junto com a ação e flui nos cortes. Nada de 1–2 s de pose ou respiração em toda abertura.
6. Direção vocal: intenção, energia e ritmo do vídeo, mais uma mudança de intenção por trecho e 1–2 palavras de ênfase. Tudo FORA das aspas. Sem tags tipo [excited], sem SSML, sem exclamação em todas as frases.
7. Timbre ≠ interpretação: @audio1 define timbre, identidade e sotaque; o roteiro define ritmo e emoção. Não escreva "copie a cadência de @audio1". Se @audio1 for a GRAVAÇÃO FINAL, respeite as palavras e o tempo dela e não prometa reentoná-la.
8. Câmera fisicamente possível: defina quem filma (celular apoiado, selfie com uma mão livre, outra pessoa filmando, POV). Uma ação principal por momento. Abrir caixa com as duas mãos exige celular apoiado ou corte.

### 3.4 Modelo de prompt (copiável)
```text
Vídeo vertical 9:16, [N] segundos, aparência de gravação real de celular para redes sociais.
REFERÊNCIAS: @img1: [pessoa]. @img2: [produto/lugar]. @audio1: referência de identidade vocal. [recebidos/planejados]
CENÁRIO E CÂMERA: [lugar, luz, quem filma, altura, enquadramento, cortes declarados].
DIREÇÃO VOCAL: Português brasileiro. [energia, ritmo, curva emocional]. Preserve timbre e sotaque de @audio1; a interpretação segue esta direção. A fala começa junto da ação e flui nos cortes. Não alongar sílabas. Não gritar.
AÇÃO E FALA:
0–X s: [ação + intenção + ênfase]. Fala: "..."
X–Y s: [...]. Fala: "..."
ÁUDIO: Uma pessoa falando em português brasileiro, boca sincronizada. @audio1 orienta identidade vocal; intenção e ritmo seguem esta direção. Som ambiente discreto, sem música e sem legendas incorporadas.
CONTINUIDADE: aparência e roupa coerentes com a referência. Produtos e ambientes mantêm formato, proporções, materiais, cores e disposição. Pele e movimentos naturais, gestos ligados à mensagem, objetos com trajetória física coerente. Sem texto na imagem.
```
- Escolha 3–5 pistas de realismo coerentes (luz lateral de janela, fios soltos, dobras da roupa, olhar alternando lente/objeto, som de contato), não todas.
- NÃO citar nomes de modelos ou plataformas dentro do prompt.
- Entregue: uma linha de resumo (estilo, duração, formato, interpretação) + mapa de referências + UM prompt. No máximo duas observações. Contagem de palavras só na revisão interna.

### 3.5 Revisão antes de entregar
- Os @ batem com o mapa e a ordem? Planejado não foi tratado como recebido?
- A abertura dá motivo para assistir? Cada trecho acrescenta algo? Há algum fato inventado?
- As palavras por trecho cabem na janela? O CTA não está atropelado nem esticado?
- Os tempos não se sobrepõem nem deixam buracos? A câmera tem operador plausível e mãos suficientes?
- Sem nome de modelo, sem parâmetros inventados, sem campos pendentes.
- Se ela disser "ficou lento/monótono": revisar densidade por trecho, direção ("sem pressa", "pausado"), queda de entonação repetida, pausas de montagem e a amostra de voz. Não basta pedir "mais rápido".

## 4. Gerar (Kairogen / Syntex)
1. Aba Vídeo > modelo (Wan 3.0+ ou Seedance 2.x).
2. Referências (não "first frame"): subir UMA imagem por vez, na ordem do prompt (a ordem vira @img1, @img2...). Subir o áudio de referência (no Seedance vira @audio1).
3. Colar o prompt e REMARCAR cada @ manualmente: texto colado não cria a marcação. Conferir se @img3 e @img4 não ficaram trocados.
4. Duração = a do roteiro. Proporção 9:16 (Reels/TikTok) ou 16:9. Áudio ligado.
5. TESTE em 480p e 4–5 s. Depois 720p/1080p para a versão final (Seedance: modo Fast em 720p economiza).
6. Informar o custo estimado antes da geração final.
7. Vídeos longos: gerar cena a cena (ou blocos de 30 s) e juntar no workspace com ffmpeg, ou no CapCut/Edits.

## 5. Casos prontos
Formatos disponíveis (escolha pela intenção): falando para a câmera; selfie testemunhal (só com experiência confirmada); unboxing (caixa já destravada, celular apoiado); provador (peça já vestida, giro de um quarto); "este gadget me salvou"; demonstração prática; antes/depois funcional (mesmo ângulo e luz, sem promessa estética/médica); rotina/GRWM; review com detalhe; resposta a dúvida; walk-and-talk (poucos passos, um ambiente por tomada); tour de loja; apresentação de imóvel; bastidores do negócio; POV com voz em off; lifestyle.
Duração como orçamento: 6–8 s = uma mensagem e uma ação; 10–15 s = abertura, demonstração e fecho; 20–30 s = dois ou três momentos; 45–60 s = dividir em tomadas com continuidade.
Variações: mude UMA variável por vez (gancho, situação de uso, câmera ou CTA).

Exemplo do curso (imobiliário, 20 s, ~55 palavras):
0–5 s fachada (@img2): "Você escolheria um imóvel só pela fachada? Vem ver o que tem por aqui." / 5–11 s sala (@img3): "Essa é a sala. Já imaginou como você organizaria esse espaço no seu dia a dia?" / 11–15,5 s varanda (@img4): "E agora, vem ver a varanda. Qual desses ambientes combina mais com você?" / 15,5–20 s olhando para a lente: "Me chama e vamos marcar uma visita pra você conhecer tudo pessoalmente."

- UGC de produto: foto dela + foto do produto + áudio. Explicar o produto (pesquisar benefícios), cenário coerente, takes (mostra, aplica/usa, close na textura), CTA.
- Tour/apresentação de espaço: foto dela + fachada + 2–3 ambientes + áudio. Um corte por ambiente, personagem andando pouco para não deformar o espaço.
- Personagem fictício (influencer de IA): definir rosto, pele, olhos, sobrancelhas, nariz, lábios e expressão. Beleza real vende mais que perfeita.

## 6. Problemas comuns
- Geração falhou ou foi barrada → perguntar a uma IA de texto "o que neste prompt pode ser barrado?", simplificar e reenviar.
- Fala errada → o Seedance às vezes troca palavras: regerar, encurtar a fala ou trocar a voz no ElevenLabs Voice Changer.
- Voz genérica → faltou o áudio de referência, ou ele passou de 15 s.
- Rosto mudou → melhorar a ficha, reforçar "manter total consistência do rosto da @img1".
- Início sem som ou travado → cortar os primeiros frames na edição.
- Imagem "não elegível" (Higgsfield/Seedance) → trocar a imagem: sem menores, sem logotipos de terceiros, sem conteúdo sensível.