---
name: lapis-vivo
description: Cria Reels/TikTok/Shorts verticais no estilo "Lápis Vivo" (aula no caderno) — um LÁPIS de verdade (foto recortada) escreve sozinho, em letra manuscrita, a explicação inteira numa página comprida de caderno espiral (pautas, margem, textura de papel) que vai rolando conforme a aula cresce; o lápis troca de cor junto com a tinta (branco, amarelo, verde, vermelho, azul) e desenha título, subtítulo, listas em colunas, grade de quadradinhos que pinta "38 de 45", tabelas linha a linha, setas curvas "× 6", contas com o resultado colorido, ícones, sublinhados e círculos, print colado com fita e, no fim, a página escurece e ele escreve o CTA com a seta. 3 temas (grafite escuro padrão, creme, quadriculado azul). Tudo em HTML/JS renderizado quadro a quadro em paralelo, com som de lápis sincronizado a cada traço e escrita no tempo da locução. Use quando o usuário pedir "lápis vivo", "aula no caderno", "lápis escrevendo", "estilo caderno escuro com lápis", "estilo do reel de matemática do Enem", "explicação escrita à mão passo a passo", "resumo/revisão no caderno", "conta/tabela sendo escrita", ou mandar um assunto, resumo, passo a passo ou locução pra virar aula escrita.
---

# Lápis Vivo

Vídeo 9:16 em que **um lápis escreve a aula inteira numa página de caderno**. É uma página só, comprida:
o título fica lá em cima, cada frase da locução vira uma linha, uma tabela, uma conta ou um desenho, e a
página sobe sozinha pra linha que está sendo escrita ficar sempre à vista. Serve pra qualquer coisa que se
explica no papel: matemática, finanças, resumo de matéria, passo a passo, receita, comparativo, checklist.

Exemplo pronto (25 s, tema grafite): `exemplos/apresentacao.mp4` · os 3 temas: `exemplos/temas.jpg` ·
projeto completo do exemplo: `exemplos/projeto-apresentacao/`. Estilo em detalhe: `references/estilo.md`.

<!-- catalogo -->
## 🧭 Aluno perdido? Mostre o catálogo
Se o usuário não souber qual estilo quer, estiver indeciso entre as skills, ou pedir "um vídeo" sem dizer o estilo: mande o catálogo com os exemplos, **https://skills-claude-ailab.pages.dev/**, e ajude a escolher pelo material que ele tem (vídeo falando, copy em texto ou só o tema), seguindo a skill `escolher-estilo`. Se o estilo certo for outro, diga qual e passe o pedido pronto dele. Nunca comece a produzir sem saber o estilo.

<!-- safe-zone-v2 -->
## ⚠️ Safe zone — OBRIGATÓRIO antes de produzir o visual
Leia `safe-zone/SAFE-ZONE.md`. Canvas 1080×1920: topo livre até y 240 · base a partir de y 1500 ·
laterais 95 px · botões x ≥ 870 de y 800 a 1500. Nesta skill o motor já cuida: a 1ª linha nasce em y 340,
o texto começa em x 150 (depois da margem) e a página rola pra linha atual nunca passar de y 1400
(y 1180 com legenda em pílula). **Cabe a você**: não deixar linha passar de x 870 (frase longa = quebrar em
duas linhas) e conferir a prévia com `python safe-zone/safe_zone.py checar <prévia.mp4> --tempos ...`.
O lápis e a espiral podem sair da área (não são conteúdo).

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO (perguntar na 1ª vez, aplicar sempre)
`python marca-dagua/marca_dagua.py status` → se NAO CONFIGURADA, perguntar (@, logo PNG ou nenhuma) e salvar.
Último passo: `python marca-dagua/marca_dagua.py aplicar <sem_marca.mp4> <final.mp4>`. Detalhes: `marca-dagua/LEIA.md`.

<!-- notificacao -->
## 🔔 Notificação no topo — OBRIGATÓRIO em todo vídeo
- **Antes de produzir:** `python notificacao/notificacao.py status`. Se der **NAO CONFIGURADA**, pedir o @, a foto de perfil e a frase → `configurar --nome perfil --foto foto.jpg --texto "Segue pra …"` (vale pra todas as skills; não perguntar de novo).
- **Fim do pipeline, ANTES da marca d'água:** `python notificacao/notificacao.py aplicar <master.mp4> <master_notif.mp4>` — o card estilo iPhone desce em 3 s (depois do gancho), fica 3,5 s e sobe. Ele ocupa y 120–210, acima do título (y 340): não colide.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO no roteiro
Leia `ganchos/GANCHOS.md`. O título É o gancho (3–7 palavras) e **no quadro 0 o lápis já está no meio dele**:
comece o título com `at` negativo (`p.titulo('…', { at: -.75, dur: 1.9 })`). Nada de página vazia no início.
Algo novo escrito a cada 1–2 s. 3 opções de gancho → escolher a mais forte.

## Primeiro uso (uma vez só)
Precisa de Node.js, Python 3 e ffmpeg (o Claude instala o que faltar, pedindo autorização):
```
cd <pasta desta skill>/scripts && npm i && npx playwright-core install chromium-headless-shell
pip install numpy pillow faster-whisper
```

## O que pedir ao usuário (só o que faltar)
1. **Assunto ou roteiro** (ou só o tema, e eu escrevo a aula). Frases curtas: cada frase vira uma linha.
2. **Tema**: `grafite` (caderno escuro, padrão), `creme` (papel claro, tinta azul-escura) ou `quadriculado`
   (azul-noite com grade). Dá pra renderizar o mesmo roteiro nos três (`--q tema=creme`).
3. **Locução**: áudio/vídeo do usuário (gravado até no celular — eu transcrevo) **ou**, se ele tiver o
   ElevenLabs conectado, voz gerada a partir do roteiro (perguntar qual voz). Sem voz também funciona:
   tempos em segundos e só o som do lápis.
4. **CTA** do final (ex.: "Comenta AULA", "Clique aqui") e prints/imagens que devem aparecer colados — opcional.

## Pipeline

### 1. Decupar o assunto em blocos
Pense como um professor escrevendo no caderno. Cada frase da fala vira UM elemento:
| A fala… | vira |
|---|---|
| nome do assunto / gancho | `titulo` + `sub` |
| pergunta, alerta, "o que cai na prova?" | `linha` amarela |
| dado, enunciado | `linha` branca (número em `*destaque*`) |
| "X de Y", proporção, dias do mês | `grade` (quadradinhos pintados) + rótulo |
| itens, tópicos | `lista` em 1 ou 2 colunas (com ✓ se for checklist) |
| assunto novo | `secao` (verde, pula uma linha) |
| relação entre duas grandezas, comparativo | `tabela` + `chave` ("× 6") |
| o cálculo e a resposta | `linha` centralizada: `'6 × 2 = *12 kg*'` |
| conceito com imagem | `icone` (emoji) ou `desenho` (vetor) |
| "repara nisso" | `sublinhar` / `circular` / `riscar` |
| prova, print, produto | `foto` colada com fita |
| chamada final | `cta` |
A página **acumula**: nada é apagado, o que já foi escrito sobe. 20–40 s de vídeo = 10 a 16 linhas.

### 2. Projeto + locução
Criar uma subpasta `<slug>` na pasta de projetos do usuário (perguntar se não souber):
```
python -I scripts/novo_projeto.py <pasta_de_projetos>/<slug>
python scripts/transcrever.py <locucao.mp3|video.mp4> <projeto> --texto copy.txt
```
Gera `words.js` (tempo de cada palavra) e `voz.wav`. Conferir a lista impressa: número falado vira
algarismo (`w('3')`, `w('12')`), "pra" pode virar "para", nomes próprios podem vir errados.

### 3. Roteiro (`<projeto>/roteiro.js`)
Partir de `exemplos/projeto-apresentacao/roteiro.js` (com locução) ou `scripts/roteiro_exemplo.js` (sem).
API completa: `references/roteiro-api.md`. Resumo:
```js
LV.config({ tema: 'grafite', duracao: 24.7 });
LV.roteiro(({ w, we, p }) => {
  p.titulo('Regra de três', { at: -.75, dur: 1.9 });                 // gancho já escrevendo no quadro 0
  p.sub('em 20 segundos', { at: w('em') });
  p.linha('5 gotas para cada *2 kg*', { at: w('gotas'), dur: .9 });  // *…* = destaque
  p.grade({ total: 45, cheios: 38, cols: 9, rotulo: '*38* de 45', at: w('trinta') });
  const t = p.tabela([['gotas', 'quilos'], ['5', '2'], ['30', '?']], { x: 300, colW: 150, at: w('tabela') });
  p.chave(t.x0 - 24, t.meio(1), t.meio(2), { lado: 'esq', rotulo: '× 6', at: w('vezes') });
  p.linha('6 × 2 = *12 kg*', { centro: true, destaque: 'verde', at: w('doze') });
  p.cta('Comenta AULA', 'que eu te mando', { at: w('comenta'), seta: 'comentario' });
});
```
- Tempos sempre pela fala: `w('palavra', n)` = início da n-ésima ocorrência; `we()` = fim.
- **O lápis é um só**: dois elementos não podem ser escritos ao mesmo tempo. Se a fala for mais rápida que
  a escrita, encurte o texto, diminua `dur` ou deixe a escrita terminar até ~0,5 s depois da palavra.
- Sem `at`, o elemento começa logo depois do anterior (bom pra rascunhar; depois amarre na fala).
- Texto começa junto da palavra falada e termina até a palavra seguinte importante.

### 4. Prévia (obrigatória antes do render)
```
node scripts/render.mjs <projeto> <tmp>/x.mp4 30 --at 0,3,7,12,18,24
```
Gera `frame_<t>.png` em `<tmp>`; montar folha de contato e revisar: linha passando de x 870, texto em cima
de texto, tabela cortada, lápis tapando o resultado no fim, CTA legível, quadro 0 com o gancho.
Erro no roteiro (palavra não encontrada, doodle inexistente) aparece como `ERRO NO ROTEIRO` — não trava.
`index.html?t=5&tema=creme` congela no navegador. `<tmp>` = pasta temporária do sistema (fora de Dropbox/OneDrive/iCloud).

### 5. Render + som
```
python -I scripts/render_paralelo.py <projeto> <tmp>/mudo.mp4 [--partes 12] [--q tema=creme]
python -I scripts/mix.py <tmp>/cues.json <tmp>/som.wav <duracao> --voz <projeto>/voz.wav [--trilha musica.wav]
ffmpeg -i <tmp>/mudo.mp4 -i <tmp>/som.wav -c:v copy -c:a aac -b:a 192k -shortest <projeto>/video/<nome>_sem_marca.mp4
```
- `render_paralelo.py` divide o vídeo em partes e roda um Chromium por parte (25 s ≈ 40 s em 12 partes num
  PC forte; em máquina fraca use `--partes 3`).
- Som (já incluso em `assets/sfx/`): cada traço toca um trecho do loop de **lápis no papel**, "pop" nos
  ícones/fotos e um whoosh suave quando a página escurece pro CTA. Volume do lápis: `--risco-db` (padrão −30,
  bem por baixo da voz). Não dá pra ouvir daqui: avisar que o balanço foi calculado e pedir pro usuário conferir.
- Depois: notificação → marca d'água → `video/<nome>.mp4`. Capa = quadro com a tabela/conta pronta.

## Regras de estilo (detalhes em `references/estilo.md`)
- Uma página só, de cima pra baixo. Nunca limpar a página nem trocar de "slide".
- Toda linha de texto senta numa pauta do caderno (o motor alinha; não force `y` quebrado sem motivo).
- Cores com função fixa: branco = conteúdo · cinza = detalhe · **amarelo = pergunta/atenção** ·
  **verde = seção e resposta certa** · vermelho = erro comum · azul = extra. No máximo 3 cores por bloco.
- O lápis fica da cor do que está escrevendo. Ele nunca some no meio; na pausa longa descansa ao lado.
- Frases curtas (até ~28 letras por linha no tamanho padrão). Número e resultado sempre em destaque.
- Fundo é sempre o caderno com textura, pauta, margem e espiral — nunca cor chapada.

## Armadilhas já resolvidas
- Dois espaços seguidos no texto: o motor já usa `white-space: pre` (antes desalinhava as letras).
- Traço com `at` negativo (gancho): o `mix.py` corta o som no zero em vez de falhar.
- Fonte Patrick Hand não tem todos os símbolos: `×`, `≈`, `→`, `✓` caem numa fonte do sistema e funcionam;
  pra ✓ de checklist prefira `p.desenho('check', { s: .3, cor: 'verde' })`.
- `words.js` ausente gera aviso ERR_FILE_NOT_FOUND no console — normal em roteiro sem locução.
- Emoji usa a fonte do sistema (Segoe UI Emoji no Windows, Apple Color Emoji no Mac): o desenho muda um
  pouco de um sistema pro outro. Pra ficar idêntico, use `p.icone('', { src: 'img/icone.png' })`.
- Imagem local no file:// é bloqueada em máscara/filtro: por isso o lápis e o papel vão em `assets/imgs.js` (data URL).
  Trocou `lapis.png`/`papel.jpg`? Regere o `imgs.js` (base64 dos três arquivos) e rode `novo_projeto.py` de novo.
- O grão do grafite é o filtro SVG `#grafite` do `index.html` (ruído + leve deslocamento no traço).
- Windows: se o Chromium completo der `spawn UNKNOWN`, o `render.mjs` já prefere o `chromium-headless-shell`.

## Arquivos
- `scripts/`: `lv.js` (motor), `lv.css`, `index.html`, `doodles.js` (vetores), `render.mjs` (prévia),
  `render_paralelo.py` (render completo), `mix.py`, `transcrever.py`, `novo_projeto.py`, `roteiro_exemplo.js`.
- `assets/`: fontes (Patrick Hand, Inter), `sfx/` (lápis, pop, whoosh), `lapis.png` (lápis fotográfico recortado),
  `lapis_mask.png` (corpo laqueado, tingido com a cor da tinta), `papel.jpg` (textura real de papel) e `imgs.js`
  (os três em data URL, pra funcionar no file://). Pautas, margem e espiral são desenhadas por código.
