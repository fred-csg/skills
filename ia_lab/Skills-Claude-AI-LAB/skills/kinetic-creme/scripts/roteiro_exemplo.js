/* Roteiro de exemplo (preview 15 s, copy genérica) — mostra todos os componentes.
   Para um vídeo novo: copie este arquivo, troque textos e tempos (ver references/componentes.md). */
function roteiro() {
  const { CX } = KC;
  const cam = KC.setup({ duration: 15, handle: '@seuperfil' });

  /* 1 · GANCHO (0 – 3.4) — ícones conectados + cards jorrando + título palavra a palavra + pílulas */
  let s = KC.scene(cam, 0, 3.4, { out: 'whip' });
  const pulses = [];
  KC.tile(s, { x: CX - 220, y: 560, icon: 'doc', t0: 0.05 });
  KC.connector(s, { x1: CX - 140, y1: 560, x2: CX + 140, y2: 560, t0: 0.3, d: 0.45 });
  KC.cardBurst(s, { fx: CX + 220, fy: 560, t0: 0.75, t1: 2.9, n: 15, region: [110, 40, 1040, 380], hubPulses: pulses });
  KC.tile(s, { x: CX + 220, y: 560, icon: 'spark', t0: 0.3, spin: 18, pulses });
  KC.monoChip(s, { x: CX + 240, y: 690, t0: 0.9, text: t => `vídeos: <b>${t < 1.3 ? 1 : t < 1.6 ? 12 : t < 1.9 ? 48 : '∞'}</b>` });
  KC.words(s, 'Essa *ferramenta* faz\nvídeos *ilimitados*', { y: 840, size: 92, t0: 0.15, step: 0.17 });
  KC.pill(s, { x: CX, y: 1010, text: 'em qualquer formato', t0: 1.9 });
  KC.pill(s, { x: CX, y: 1100, text: 'pronto em minutos', t0: 2.25 });

  /* 2 · VIRADA (3.4 – 5.2) — caps letra a letra + palavra grande + sublinhado */
  s = KC.scene(cam, 3.4, 5.2, { out: 'tilt' });
  KC.glyph(s, { x: CX - 170, y: 560, text: '{ }', t0: 3.45 });
  KC.glyph(s, { x: CX + 90, y: 1000, text: '( )', t0: 3.6 });
  KC.words(s, 'deixa eu te mostrar', { y: 700, size: 30, cls: 'caps', t0: 3.45, step: 0.035, letters: true });
  KC.words(s, 'COMO FUNCIONA', { y: 785, size: 104, t0: 3.95, step: 0.12 });
  KC.underline(s, { x: CX, y: 865, w: 170, t0: 4.35 });

  /* 3 · PROVA (5.2 – 8.8) — janela escura: código digitando → painel com contadores e gráfico */
  s = KC.scene(cam, 5.2, 8.8, { out: 'whip' });
  const win = KC.windowCard(s, { x: CX, y: 640, w: 820, h: 640, t0: 5.2 });
  KC.codeTyper(win.body, { t0: 5.55, cps: 130, until: 6.75, lines: [
    [['const ', 'k'], ['video', ''], [' = ', 'p'], ['cena', 'k'], ['({', 'p']],
    [['  formato: ', ''], ['"9:16"', 's'], [',', 'p']],
    [['  estilo: ', ''], ['"creme"', 's'], [',', 'p']],
    [['  legenda: ', ''], ['"palavra a palavra"', 's'], [',', 'p']],
    [['});', 'p']],
    [['render', 'k'], ['(video, ', 'p'], ['30', 's'], [');  ', 'p'], ['// fps', 'c']],
    [['', '']],
    [['● pronto · quadro a quadro', 's']],
  ] });
  KC.statTile(win.body, { x: 24, y: 22, w: 376, label: 'views', to: 248000, t0: 6.95, d: 1.1 });
  KC.statTile(win.body, { x: 420, y: 22, w: 376, label: 'salvamentos', to: 12400, t0: 7.1, d: 1.1 });
  KC.areaChart(win.body, { x: 24, y: 192, w: 772, h: 360, t0: 7.0, d: 1.2 });
  KC.tag(s, { x: CX - 210, y: 860, text: 'em apenas 3 dias', t0: 7.85 });
  KC.tag(s, { x: CX - 170, y: 935, text: 'feito em código', t0: 8.1, rot: 0, white: true,
    icon: '<span style="width:30px;height:30px;border-radius:8px;background:#F47B20;display:inline-block"></span>' });
  KC.captionCard(s, { x: CX, y: 1085, w: 820, t0: 5.45, step: 0.2, spec: 'Feito *100%* em código: *248 mil* views em *3* dias' });

  /* 4 · OBJEÇÃO (8.8 – 11.4) — frase riscada + carimbo laranja */
  s = KC.scene(cam, 8.8, 11.4, { out: 'tilt' });
  KC.words(s, 'Agora você deve estar pensando', { y: 640, size: 38, cls: 'sub', t0: 8.85, step: 0.1 });
  const obj = KC.words(s, 'que isso é\nmuito difícil', { y: 770, size: 96, t0: 9.45, step: 0.14 });
  KC.strikeLines(obj, { t0: 10.15 });
  KC.stamp(s, { x: CX, y: 950, text: 'não é não.', t0: 10.5 });

  /* 5 · ESCALA (11.4 – 12.9) — hub central + rede de celulares */
  s = KC.scene(cam, 11.4, 12.9, { out: 'whip' });
  KC.hubNetwork(s, { cx: CX, cy: 555, r: 285, t0: 11.3 });
  KC.words(s, 'Uma ideia vira\n*dez* conteúdos', { y: 1130, size: 84, t0: 11.5, step: 0.14 });

  /* 6 · CTA (12.9 – 15) — "Comenta" + caixa de comentário + DM automática */
  s = KC.scene(cam, 12.9, 15, { last: true });
  KC.words(s, 'Se você quer saber como', { y: 620, size: 40, cls: 'sub', t0: 12.95, step: 0.09 });
  const cw = KC.words(s, 'Comenta', { x: CX + 45, y: 720, size: 118, t0: 13.3, step: 0.1 });
  KC.tile(s, { x: CX + 45 - cw.box.offsetWidth / 2 - 62, y: 724, size: 100, icon: 'spark', t0: 13.3, spin: 25, bare: true });
  KC.commentBox(s, { x: CX, y: 880, text: 'QUERO', t0: 13.55, cps: 13, pubAt: 14.35 });
  KC.dmToast(s, { x: CX, y: 1050, t0: 14.5, html: '<svg width="40" viewBox="0 0 40 30"><rect x="2" y="2" width="36" height="26" rx="5" fill="#fff"/><path d="M5 6l15 11L35 6" fill="none" stroke="#EA6511" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg> DM enviada: <b>todos os detalhes</b>' });
  KC.words(s, 'chega no seu *direct* ↓', { y: 1150, size: 30, cls: 'sub', t0: 14.7, step: 0.05 });
}
