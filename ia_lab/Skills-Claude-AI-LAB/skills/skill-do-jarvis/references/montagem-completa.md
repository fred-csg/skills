# Montagem completa (o vídeo inteiro, sem abrir Premiere/CapCut)

O usuário manda o material bruto — takes de vídeo, locução, áudio, trilha, imagens — e a skill decupa, escolhe os melhores takes e monta o vídeo inteiro. Depois aplica motion, legenda e sonorização se o usuário quiser.

> Status: fluxo descrito a partir das peças já validadas (transcrição por palavra, cortes por silêncio, EDL, render no Remotion). A escolha automática de "melhor take" entre várias tentativas ainda não foi testada num projeto real: no primeiro uso, mostrar a decisão em tabela antes de renderizar.

## 1. Inventário
- Listar tudo com `ffprobe`: duração, resolução, fps, HDR, se tem áudio. Separar por tipo: **takes de câmera**, **B-roll**, **locução** (voz limpa), **trilha**, **imagens/logos**.
- Converter HDR do iPhone para SDR (filtro da seção 4 das Regras de ouro). Normalizar tudo para o fps do projeto.

## 2. Decupagem
- Transcrever cada take e a locução por palavra (`assets/legenda-template/scripts/transcrever.py`).
- `decupagem.md`: arquivo | trecho | fala | qualidade (fluência, gaguejo, erro, energia) | uso.
- **Takes repetidos da mesma fala:** agrupar pela similaridade do texto; escolher o melhor por: frase completa sem erro > menos gaguejo/repetição > maior confiança média do whisper > energia/volume estável > enquadramento. Mostrar a escolha ao usuário na primeira vez.

## 3. Corte e montagem
- Se há **locução separada**, ela manda: a timeline segue a voz e cada frase recebe o take/B-roll que mostra o que é dito.
- Se é **vídeo falado**, cortar silêncios > 0,35 s, gaguejos e repetições (seção 2 do SKILL.md); hook forte nos primeiros 1,5 s.
- Montar a EDL (`edl.json`: arquivo, entrada, saída, posição na timeline, faixa). Crossfade de áudio de 10 ms nos cortes de voz.
- **Trilha:** detectar batidas (onsets) e alinhar cortes de B-roll e transições à batida mais próxima (±3 frames); ducking da trilha sob a voz (−12 a −18 dB); fade no fim.
- Renderizar no Remotion com `<Sequence>` + `<OffthreadVideo startFrom/endAt>` por item da EDL (preview na timeline do Studio).

## 4. Acabamento (opcional, conforme o pedido)
Motion (`references/plano-motion.md`), legenda com tracking (`references/legendas-criativas.md`), sonorização (`references/sfx-codigo.md`), correção de cor simples (exposição/contraste/saturação iguais entre takes).

## 5. Entrega
MP4 final + `decupagem.md` + EDL + SRT + XML do Premiere (FCP7 xmeml) para quem quiser ajustar fora. O usuário não precisa abrir nenhum editor.
