---
name: "videos-com-avatar"
description: "Ponto de partida para produzir vídeos da Andreia com avatar/clone de IA: briefing, escolha do tipo de clone, roteiro cronometrado, divisão de tarefas, controle de qualidade e entrega."
---

# Vídeos com avatar — orquestração

Use esta skill sempre que a Andreia pedir um vídeo com o avatar/clone dela (Reels, anúncio, UGC, aula, conteúdo de marca). Ela coordena o trabalho e chama as skills de execução:
- `heygen-clone-camera-fixa` → vídeo falando para a câmera parada (Reels do dia a dia, anúncios falados, aulas).
- `clone-em-acao-wan-seedance` → vídeo com movimento, produto na mão, troca de ambientes, UGC, tour.

Método baseado no curso "Clone Digital de IA" (André Peterson, Hotmart, versão de nov/2026). As ferramentas mudam de tela com frequência: confira sempre a interface atual antes de seguir um passo literal.

## 1. Briefing (pergunte só o que faltar)
1. Objetivo e canal: Reels/TikTok (9:16), LinkedIn/YouTube (16:9), anúncio, aula.
2. Mensagem central, público e CTA.
3. Duração alvo.
4. Tipo de vídeo (ver seção 2).
5. Voz: (a) a Andreia grava o áudio do roteiro — opção mais realista; (b) clone de voz do HeyGen; (c) clone de voz no MiniMax.
6. Visual/look: qual cenário e roupa do avatar.
7. Se envolver marcas da empresa, liste os nomes por extenso conforme as preferências dela.

## 2. Escolha do tipo de clone
| Situação | Tipo | Ferramenta |
|---|---|---|
| Falando para a câmera, câmera parada, meio corpo | Câmera fixa | HeyGen (modelo Avatar mais recente) |
| Precisa andar, segurar produto, mudar de ambiente, câmera em movimento | Clone em ação | Wan 3.0+ (mais barato) ou Seedance 2.x, via Kairogen, Syntex, Higgsfield ou wan.video |
| Rascunho longo sem gastar crédito | Câmera fixa econômica | HeyGen Avatar 3 (ilimitado, mais travado) |
| Sem vídeo de referência ou sem verificação de identidade | Foto para vídeo | HeyGen > Criação rápida > Foto para vídeo |

Regra: no HeyGen, nada nas mãos (microfone e objetos somem ou deformam). Para mostrar produto, use o clone em ação.

## 3. Roteiro cronometrado
- Escreva no tom de voz da Andreia (consulte o tom de voz registrado na memória, se houver) e em PT-BR falado, com frases curtas e naturais.
- Orçamento de fala: T = duração total; V = trechos só de imagem/som; F = T − V (janela de fala); N = palavras pronunciadas (números e siglas por extenso). Velocidade = 60 × N / F palavras por minuto. Confira o total E cada trecho.
- Faixas iniciais por formato (estimativas editoriais do material do curso; validar no teste):
  - Anúncio ágil, gadget: 170–195 ppm
  - Imobiliário comercial, tour de loja, provador: 160–185 ppm
  - Review, antes/depois: 155–180 ppm
  - Unboxing, rotina, bastidores: 150–175 ppm
  - Selfie testemunhal, especialista explicando: 145–170 ppm
  - Luxo contemplativo/íntimo: 115–145 ppm, ou sem fala
- Referência rápida para anúncio falado ágil: 8 s ≈ 21–24 palavras; 10 s ≈ 27–30; 15 s ≈ 41–46; 20 s ≈ 54–60; 30 s ≈ 81–90. Não vale para unboxing com silêncio, áudio final gravado ou vídeo contemplativo.
- Fala curta demais: enriquecer com conteúdo útil ou deixar imagem/som no resto. NUNCA esticar a fala ("fale devagar"), que fica robótico. Fala longa demais: editar, redistribuir ou dividir. Não acelerar sem limite.
- Texto obrigatório curto (por exemplo, só "Conheça este imóvel"): manter, falar no tempo natural e completar com imagem.
- Com áudio final gravado, a duração medida do arquivo prevalece sobre qualquer contagem.
- Gancho ligado ao que vai ser entregue (escolha, critério, ação, curiosidade cumprida, problema real). Nada de "o segredo que ninguém conta" sem segredo de verdade. Sem adjetivos vazios em sequência ("imperdível, sensacional").
- Estrutura: gancho visual e falado nos 2 primeiros segundos → desenvolvimento → CTA.
- Câmera fixa: deixe o terço superior livre para título e legenda na edição.
- Clone em ação: divida em cenas/takes com tempo ("0–5 s fachada, 5–10 s sala..."). Limites por geração: Veo 3 = 8 s; Seedance ≈ 12–15 s; Wan ≈ até 30 s. Cenas mais longas: gere em partes e junte.
- Entregue o roteiro para aprovação antes de gastar créditos.

## 4. O que só a Andreia pode fazer (nunca simular)
- Login em contas, senhas e códigos de verificação.
- Assinar planos ou comprar créditos. Recomende o plano mensal; o anual cobra 12 meses de uma vez.
- Gravar o vídeo de referência, os áudios e a verificação de identidade (QR code + leitura de número na câmera).
- Aprovar downloads para o computador dela (peça permissão informando arquivo, origem e tamanho).

## 5. Regra de ouro dos créditos
1. Teste com 5–10 s (ou 480p no clone em ação) antes do vídeo inteiro.
2. Só gere a versão final depois que o teste ficar bom.
3. Antes de gerar, informe à Andreia a estimativa de custo/créditos e peça o ok quando o gasto for relevante.

## 6. Controle de qualidade (antes de entregar)
Não consigo ouvir áudio diretamente. Por isso:
- Imagem: extraia frames do vídeo baixado (ffmpeg no workspace) e verifique mãos, dentes, olhos, objetos que somem, corpo e proporção, fundo travado ou com pessoas, marca d'água.
- Áudio: meça volume e silêncios (`ffmpeg -af ebur128` e `silencedetect`). Se for possível instalar o Whisper, transcreva e compare com o roteiro palavra a palavra: erros de fala, sotaque e palavras inventadas.
- Diga claramente o que verifiquei e peça que a Andreia ouça a entonação e o sotaque, que eu não consigo avaliar.
- Lembre o "paradoxo do espelho": o clone precisa de cerca de 90% de fidelidade. Vale mais um bom roteiro do que perfeição.

## 7. Entrega
- Nome do arquivo: `AAAA-MM-DD_tema_formato_v1.mp4`.
- Entregue o MP4 com uma linha de contexto, mais o roteiro final e as configurações usadas (ferramenta, modelo, resolução, créditos).
- Nunca publique online, nem em links públicos, vídeos, páginas ou artefatos com nomes da empresa, das marcas ou de pessoas.
- Edição básica: legendas, título, tela dividida e música no editor do HeyGen, ou no CapCut/Edits pela Andreia.