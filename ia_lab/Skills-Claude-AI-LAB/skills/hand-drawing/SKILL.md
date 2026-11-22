---
name: hand-drawing
description: Cria Reels/TikTok/Shorts verticais no estilo "Hand Drawing" (whiteboard/explainer desenhado) — uma MÃO REAL segurando marcador ou giz escreve a copy falada em letra manuscrita e desenha, traço a traço, ilustrações que explicam cada frase (ícones vetoriais + doodles gerados por IA e vetorizados), prints colados com fita e circulados, legenda em pílula com palavra-chave colorida e câmera que chicoteia de um quadro pro próximo. 3 temas com fundo texturizado: papel off-white + marcador, lousa verde + giz, lousa preta + giz. Tudo em HTML/JS renderizado quadro a quadro, com som de marcador/giz sincronizado a cada traço. Use quando o usuário pedir "hand drawing", "handrawing", "mão desenhando", "vídeo de quadro branco / whiteboard / lousa / giz", "explainer desenhado", "estilo VideoScribe", "doodle animado da copy", ou mandar uma copy/locução pra virar vídeo desenhado.
---

# Hand Drawing

Vídeo 9:16 em que **uma mão desenha a copy falada**: o título da frase é escrito à mão no topo, embaixo
a mão ilustra a ideia (boneco, ícone, print, número em destaque), a legenda em pílula acompanha a fala,
e a cada nova frase a câmera chicoteia pro quadro ao lado. Referência de estilo: `references/estilo.md`.

Exemplo pronto (13 s, tema papel): `exemplos/demo_papel.mp4` — os 3 temas no catálogo · projeto completo do exemplo: `exemplos/projeto-demo/`.

<!-- catalogo -->
## 🧭 Aluno perdido? Mostre o catálogo
Se o usuário não souber qual estilo quer, estiver indeciso entre as skills, ou pedir "um vídeo" sem dizer o estilo: mande o catálogo com os exemplos, **https://skills-claude-ailab.pages.dev/**, e ajude a escolher pelo material que ele tem (vídeo falando, copy em texto ou só o tema), seguindo a skill `escolher-estilo`. Se o estilo certo for outro, diga qual e passe o pedido pronto dele. Nunca comece a produzir sem saber o estilo.

<!-- safe-zone-v2 -->
## ⚠️ Safe zone — OBRIGATÓRIO antes de produzir o visual
Leia `safe-zone/SAFE-ZONE.md`. Canvas 1080×1920: topo livre até y 240 · base a partir de y 1500 ·
laterais 95 px · botões x ≥ 870 de y 800 a 1500. Nesta skill: títulos em y 300–460, ilustração em
y 520–1180 (abaixo de y 800 nada essencial passa de x 870), legenda já centrada em x 482 / y 1395.
Antes do render final: `python safe-zone/safe_zone.py checar <prévia.mp4> --tempos ...`.
A mão pode sair da área (não é conteúdo).

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO (perguntar na 1ª vez, aplicar sempre)
`python marca-dagua/marca_dagua.py status` → se NAO CONFIGURADA, perguntar (@, logo PNG ou nenhuma) e salvar.
Último passo: `python marca-dagua/marca_dagua.py aplicar <sem_marca.mp4> <final.mp4>`. Detalhes: `marca-dagua/LEIA.md`.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO no roteiro
Leia `ganchos/GANCHOS.md`. Quadro 0,0 s já com a mão escrevendo o gancho (3–7 palavras grandes);
nada de quadro vazio no início. Algo novo desenhado a cada 1–2 s. 3 opções de gancho → escolher a mais forte.

## Primeiro uso (uma vez só)
Precisa de Node.js, Python 3 e ffmpeg (o Claude instala o que faltar, pedindo autorização):
```
cd <pasta desta skill>/scripts && npm i && npx playwright-core install chromium-headless-shell
pip install numpy pillow scipy scikit-image faster-whisper
```

## O que pedir ao usuário (só o que faltar)
1. **Copy/roteiro** (ou tema, e eu escrevo). Frases curtas — cada frase vira um quadro.
2. **Tema**: `papel` (marcador preto + destaque laranja-vermelho `#E8452C`), `lousa-verde` (giz branco + amarelo),
   `lousa-preta` (giz branco + verde-limão `#D7FF3A`). Pode fazer mais de um com o mesmo roteiro.
   Cores próprias: `HD.config({ cores: { acc: '#...' } })`.
3. **Locução**: áudio/vídeo do usuário (gravado até no celular — eu transcrevo) **ou**, se ele tiver o
   ElevenLabs conectado, voz gerada a partir da copy (`eleven_v4`, `language="pt"`; perguntar qual voz).
   Sem voz nenhuma também dá: legendas manuais com `legenda()` e só os sons de escrita.
4. Prints/fotos que devem aparecer colados (produto, anúncio, tela) — opcional.

## Pipeline

### 1. Decupar a copy em quadros (beats)
Uma frase = um quadro. Pra cada quadro decidir: **título manuscrito** (2–5 palavras da fala, CAIXA ALTA),
**ilustração** (o que a frase "mostra"), **destaque** (número/palavra em cor de destaque, check, círculo, seta).
Padrões que funcionam:
- Pergunta-gancho no topo + personagem reagindo + número grande em destaque ("10 VEZES").
- Lista que vai ganhando ✓ linha a linha → frase em destaque "E MESMO ASSIM NÃO VENDE".
- Print colado com fita + círculo na informação + anotação à mão ("700 VENDIDOS").
- Conceito com ícone (alvo = "a única saída", lupa = "deixa eu te mostrar", prancheta = "teste").
- CTA: "CLICA EM SAIBA MAIS" + seta pra baixo + ação em destaque.
O quadro **acumula**: título fica, desenho entra, destaque entra por último. Não limpar no meio da frase.

### 2. Ilustrações — híbrido
- **Vetor da biblioteca** (`scripts/doodles.js`, de graça): check, xis, setas, brilho, raios, interrogação,
  exclamação, coração, cifrão, raio, lâmpada, alvo, celular, prancheta, lupa, nuvem, boneco, boneco-triste,
  grupo, cronômetro, porta, etiqueta, troféu, gráfico, balão, presente, carrinho, dinheiro, casa, envelope,
  cadeado, documento, megafone, relógio, engrenagem + marcações (circulo, sublinhado, risco).
  Catálogo visual: `references/catalogo_doodles.jpg`. Desenho novo simples → escrever o vetor (ver `references/roteiro-api.md`).
- **Doodle por IA + vetorização** (personagens, cenas, objetos específicos): se o usuário tiver um gerador de
  imagem conectado (Higgsfield, Artlist etc.) ou mandar a imagem pronta, gerar com o prompt de
  `references/prompts-doodle.md` e rodar `python -I scripts/vetorizar.py <img.png> <projeto> <nome>` → a mão
  percorre o esqueleto e revela o desenho. Preto vira a tinta do tema; laranja/vermelho vira o destaque.
  Sem gerador: usar só a biblioteca vetorial (dá um vídeo completo do mesmo jeito).

### 3. Projeto + locução
Criar uma subpasta `<slug>` na pasta de projetos do usuário (perguntar se não souber):
```
python -I scripts/novo_projeto.py <pasta_de_projetos>/<slug>
python -I scripts/transcrever.py <locucao.mp3|video.mp4> <projeto> --texto copy.txt
```
Gera `words.js` (tempos de cada palavra) e `voz.wav`. Whisper `medium`; sem GPU cai pra CPU sozinho.
Conferir a lista impressa: nomes próprios/termos podem vir errados — o roteiro busca palavras sem acento.

### 4. Roteiro (`<projeto>/roteiro.js`)
Partir de `exemplos/projeto-demo/roteiro.js`. API completa: `references/roteiro-api.md`. Resumo:
```js
HD.config({ tema: 'papel', duracao: 13.6 });
HD.roteiro(({ w, we, cena, legendas }) => {
  legendas({ destaques: ['dez', 'shopee'] });            // pílula 2–3 palavras, palavra-chave colorida
  const c = cena(w('você') - .12, w('olha') - .12);      // um quadro; troca com chicote no início do próximo
  const t = c.texto('JÁ CONFERIU\nESSA LISTA?', { y: 340, size: 76, at: w('conferiu'), dur: 1.2 });
  c.desenho('prancheta', { y: 800, s: 1.4, at: t.fim, dur: 1.0 });
  c.texto('10 VEZES', { y: 1150, size: 90, cor: 'acc', at: w('dez') });
  c.circular(t.linhas[1], { at: we('vezes') });
});
```
- Tempos sempre pela fala: `w('palavra', n)` = início da n-ésima ocorrência; `we()` = fim.
- O desenho deve **terminar até a palavra correspondente** ou logo depois (≤ 0,3 s). Título começa junto da fala.
- Corte de quadro ~0,12 s antes da 1ª palavra da frase nova (o chicote dura 0,42 s).

### 5. Prévia (obrigatória antes do render)
```
node scripts/render.mjs <projeto> <tmp>/x.mp4 30 --at 0.3,2.9,5,8 --q tema=papel
```
Gera `frame_<t>.png`; montar folha de contato e revisar: texto cortado, desenho atrasado em relação à fala,
mão tapando o destaque no fim do quadro, sobreposição, safe zone. `index.html?t=5&tema=lousa-verde` congela no navegador.
`<tmp>` = pasta temporária do sistema (fora de Dropbox/OneDrive/iCloud).

### 6. Render + som
```
node scripts/render.mjs <projeto> <tmp>/mudo.mp4 30 --q tema=<tema>
python -I scripts/mix.py <tmp>/cues.json <tmp>/som.wav <duracao> --voz <projeto>/voz.wav [--trilha musica.wav]
ffmpeg -i mudo.mp4 -i som.wav -c:v copy -c:a aac -b:a 192k -shortest <projeto>/video/<nome>_sem_marca.mp4
```
- ~3 quadros/s no render (13 s ≈ 2–3 min por tema). Rodar em segundo plano; vários temas = em sequência.
- Som (já incluso em `assets/sfx/`): cada traço toca um trecho do loop de **marcador** (papel) ou **giz** (lousas),
  whoosh no chicote e "pop" de papel nas fotos. Volume do risco: `--risco-db` (padrão −32, bem por baixo da voz).
  Não dá pra ouvir daqui: avisar que o balanço foi calculado e pedir pro usuário conferir.
- Depois: marca d'água → `video/<nome>_<tema>.mp4`. Capa = quadro do gancho com o desenho pronto.

## Regras de estilo (detalhes em `references/estilo.md`)
- Fundo SEMPRE texturizado (papel com fibras; lousa com marcas de apagador e escrita fantasma) + vinheta. Nunca cor chapada.
- Uma cor de tinta + UMA cor de destaque por tema. Destaque só no que importa (número, palavra-chave, check, círculo).
- Letra manuscrita Permanent Marker em CAIXA ALTA; títulos 64–90 px, destaques até 150 px.
- Traço dos desenhos 7 px — mesmo peso em tudo; desenhos simples, muito respiro.
- A mão nunca some no meio do quadro; entre traços ela levanta (sombra cresce) e viaja em arco curto.
- Câmera sempre viva: leve push-in por quadro + segue a ponta da caneta; chicote com motion blur horizontal.

## Armadilhas já resolvidas
- `mask-image` com PNG local é bloqueada no file:// → o grão do giz é gerado em canvas (`graoGiz()`).
- `dur` do texto = tempo total real (letras + pausas entre palavras + troca de linha); `t.fim` = último traço.
- Fontes precisam estar carregadas antes de medir as letras (o motor já espera `document.fonts`).
- `words.js`/`artes/artes.js` ausentes geram aviso ERR_FILE_NOT_FOUND no console — normal se não usar.
- Windows: se o Chromium completo der `spawn UNKNOWN`, o `render.mjs` já prefere o `chromium-headless-shell`.

## Arquivos
- `scripts/`: `hd.js` (motor), `doodles.js` (vetores), `index.html`, `hd.css`, `render.mjs`, `mix.py`,
  `transcrever.py`, `vetorizar.py`, `novo_projeto.py`, `roteiro_exemplo.js`.
- `assets/`: mãos recortadas (`maos.json` = ponta da ferramenta), 3 fundos emendáveis, fontes, `sfx/`.
