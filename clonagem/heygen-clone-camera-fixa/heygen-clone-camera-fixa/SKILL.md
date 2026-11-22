---
name: "heygen-clone-camera-fixa"
description: "Criar e usar o clone de câmera fixa da Andreia no HeyGen (e voz no MiniMax) via navegador: referências, avatar, voz, looks, verificação e geração de vídeos falados."
---

# Clone de câmera fixa — HeyGen

Operar pelo navegador da Andreia (Claude in Chrome), na conta dela. O HeyGen muda botões de lugar e varia a interface entre contas. Antes de cada passo, tire um screenshot e procure o equivalente na tela atual. Roteiro e briefing vêm da skill `videos-com-avatar`.

## A. Setup único (primeira vez ou novo avatar)

### A1. Checklist do vídeo de referência (a Andreia grava)
Um único vídeo de 15–30 s gera as três referências: vídeo, foto (print) e voz.
- Gravar já no cenário, com a roupa e o cabelo que o clone terá: escritório, sala etc.
- Câmera FIXA, apoiada, nunca na mão de alguém. Celular é ótimo, mais realista para Reels.
- Luz de frente para uma janela (de manhã), poucas sombras, rosto nítido.
- Enquadramento próximo, meio corpo, terço superior livre.
- Falar como se gravasse um conteúdo real: gestos naturais, mãos aparecendo, expressão viva, sem gaguejar.
- Áudio limpo: microfone ou celular perto, silêncio, sem ruído. Sotaque bem marcado.
- Evitar: andar, ficar longe da câmera, pessoas ou pets no fundo, filtro de pele (maquiagem pode), segurar microfone ou objetos.
- Ideal: gravar 3–8 variações (expressão, empolgação, uso das mãos) e escolher as melhores. Nem todas ficam boas no clone.

### A2. Foto de referência
- Print de um frame do próprio vídeo: rosto bem visível, boca levemente aberta (falando), tela cheia, sem ícones, legendas ou texto.
- Não usar "foto favorita" nem foto gerada por IA: foto com cara de IA gera vídeo com cara de IA.

### A3. Criar o avatar
1. heygen.com > Avatar > Criar avatar > Clonar pessoa real ("se parece, se movimenta e soa como eu"). Contas novas podem abrir em "Clone você mesmo".
2. FOTO (define a aparência) + nome do avatar.
3. VÍDEO de referência: "Carregar", nunca gravar pela webcam. Ele define movimentos de olhos, boca e braços.
4. VOZ: "Clonar voz a partir dessa gravação" > Manter atual > Criar clone de voz. Ouvir as prévias e testar os mecanismos disponíveis (padrão, Fish/Starfish, HeyGen/Radiant Voice, ElevenLabs). Escolher o mais fiel ao sotaque paulistano dela; o HeyGen tende a puxar um sotaque carioca.
5. Não clicar em "Criar visuais com IA" durante a criação: gasta crédito e costuma ficar artificial.
6. Verificação de identidade (aba Movimento/Motion > Verificar agora): obrigatória para usar os movimentos reais. A Andreia faz pelo celular (QR code, lê o número na tela), cerca de 1 min. Sem ela, os movimentos são genéricos de IA.
- Uma conta permite clonar uma pessoa real. Clone de outra pessoa exige a verificação dela, na conta dela.

### A4. Novos looks (roupa e cenário)
Preferir gerar fora do HeyGen e fazer upload:
1. ChatGPT (imagem): sempre um chat NOVO por look, reenviando a foto original.
2. Prompt base, mudando UMA coisa por vez:
   > "[Troque a roupa para X / Coloque-a em Y]. Mantenha toda a estrutura da imagem exatamente igual e a mesma posição. Mantenha 100% de consistência do rosto, textura da pele e cabelo. Foto ultrarrealista estilo iPhone, com objetos e cena reais. Formato 9:16."
3. Conferir rosto, proporção corpo/cabeça e biotipo. Cenário sem pessoas e com câmera estática.
4. HeyGen > Avatar > Aparência > Novo visual > Upload de foto.
- O melhor de tudo é gravar uma referência real em cada cenário desejado.

## B. Produzir um vídeo
1. Ir no AVATAR > "Usar em um vídeo". NÃO usar "Prompt para vídeo": usa outros modelos, gasta mais e bagunça.
2. Escolher o visual (look).
3. Script — escolher a fonte de voz:
   - Áudio real da Andreia (MP3) → mais realista, porque a entonação real guia os movimentos. Melhor opção.
   - Texto + clone de voz do HeyGen → rápido, um pouco mais robótico. Ajustar velocidade, trocar mecanismo, corrigir pronúncia.
   - Áudio do MiniMax (seção C) → quando ela não pode gravar e o sotaque do HeyGen não convence.
4. Avatar: formato retrato 9:16 (ou 16:9), modelo de avatar MAIS RECENTE disponível (Avatar V/5, 6...), 1080p (720p no plano grátis, com marca d'água). Piscar/expressão a critério.
5. Primeiro um TESTE curto (5–10 s). Avaliar e só então gerar o vídeo completo.
6. Editor opcional do HeyGen: legenda (estilo e cor), título, tela dividida, mídia de banco, música, tela verde. Depois, baixar (pedir permissão para o download).
- Custo de referência (curso, nov/2026): Creator US$29/mês ≈ 600 créditos ≈ 30 min no Avatar 5. Avatar 3 não consome créditos.
- Extras: HeyGen também dubla/traduz vídeos.

## C. Voz alternativa — MiniMax Audio (minimax.io)
1. Voice Clone: subir 10–300 s de áudio (aceita vídeo). A melhor fonte é o áudio limpo de um Reels dela. Idioma: Português. Gerar prévias (não gastam crédito) até ficar fiel > salvar a voz com o nome dela.
2. Text to Speech > Voice > My voices > selecionar a voz. Modelo mais novo (HD). Conferir se o idioma está em PORTUGUÊS (às vezes detecta italiano ou espanhol). Velocidade em torno de 1.05.
3. Gerar FRASE A FRASE, regerar as que ficarem ruins e baixar cada MP3 (audio01, audio02...).
4. Juntar os MP3 em ordem. No workspace: `ffmpeg -f concat -safe 0 -i lista.txt -c copy roteiro.mp3`, ou recodificar se os formatos divergirem.
5. Subir o MP3 final no HeyGen (passo B3).
- Plano grátis ≈ 10 mil créditos/mês por conta, até 3 clones de voz. Pago ≈ US$10.

## D. Problemas comuns
- Clone robótico → referência fraca: regravar com mais expressão e luz, ou usar áudio real.
- Marcas de expressão somem → foto mais nítida, mais próxima e bem iluminada.
- Mão deformada → referência segurando objeto: regravar sem nada nas mãos ou trocar o look por foto sem o objeto.
- Sotaque errado → testar outro mecanismo de voz, áudio real ou MiniMax.
- Créditos acabando rápido → testes longos demais: voltar aos testes de 5–10 s.