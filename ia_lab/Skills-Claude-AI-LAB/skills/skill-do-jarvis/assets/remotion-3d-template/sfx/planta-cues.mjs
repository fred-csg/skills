// Cues de SFX da planta 3D, sincronizadas com T (src/scene/Scene.tsx) e ITEMS (src/scene/data.ts).
// Variante 'vidro' (tins de vidro) ou 'holograma' (blips digitais). Tempo em segundos = frame / 30.
const FPS = 30;
const s = (frame) => frame / FPS;

// mesma ordem de ITEMS em data.ts: modo de entrada de cada móvel
const ITEM_MODES = ['rise', 'rise', 'rise', 'drop', 'drop', 'rise', 'drop', 'rise', 'rise', 'drop', 'rise', 'drop', 'rise', 'drop', 'drop', 'rise', 'rise', 'rise', 'drop'];
// escala pentatônica de Mi menor (casa com o pad em Em9): a montagem vira uma melodia subindo
const PENTA = [76, 79, 81, 83, 86, 88, 91, 93];
const MELODY = [0, 1, 2, 3, 2, 4, 3, 5, 4, 6, 5, 4, 5, 6, 7, 6, 5, 6, 7];

export default (variant = 'vidro') => {
  const holo = variant === 'holograma';
  const ping = holo ? 'digi' : 'glass';
  const cues = [];
  const c = (t, sName, p = {}, g = 1, send = 0.25, bus) => cues.push({t, s: sName, p, g, send, bus});

  // cama sonora o vídeo todo
  c(0, 'pad', {dur: 15}, holo ? 0.55 : 0.6, 0.15);

  // 01 · planta: linhas desenhando
  c(s(8), 'scan', {dur: 2.2, from: holo ? 700 : 450, to: holo ? 2200 : 1400}, holo ? 1.6 : 1.4, 0.3);
  c(s(40), 'blip', {note: 88, pan: -0.3}, 0.5, 0.3, 'ui');
  c(s(44), 'blip', {note: 93, pan: 0.3}, 0.45, 0.3, 'ui');
  // rótulos dos cômodos (5, stagger 4f)
  [0, 1, 2, 3, 4].forEach((i) => c(s(54 + i * 4), holo ? 'digi' : 'tick', holo ? {note: 96 + i * 2, pan: -0.4 + i * 0.2} : {pan: -0.4 + i * 0.2, tone: 5200}, holo ? 0.35 : 0.5, 0.2, 'ui'));

  // 02 · perspectiva: grande whoosh na rotação da câmera + riser até as paredes
  c(s(84), 'whoosh', {dur: 2.6, from: 180, to: 2200, q: 1.1, p0: 0.7, p1: -0.6, peak: 0.5}, 0.9, 0.35, 'whoosh');
  c(s(98), 'riser', {dur: s(140) - s(98)}, 0.55, 0.3, 'whoosh');

  // 03 · estrutura: impacto quando as paredes começam a subir + baques por parede
  c(s(140), 'impact', {size: 1}, 0.95, 0.35, 'impact');
  for (let i = 0; i < 12; i++) c(s(138 + i * 6 + 6), 'thump', {note: 36 + (i % 3) * 2, pan: -0.6 + (i % 5) * 0.3}, 0.32, 0.15, 'impact');
  // piso trocando de material: brilho varrendo
  c(s(178), 'whoosh', {dur: 1.5, from: 1200, to: 7000, q: 2.5, p0: -0.5, p1: 0.5, peak: 0.35}, 0.35, 0.5, 'whoosh');

  // 04 · ambientação: cada móvel toca uma nota quando aparece/aterrissa
  ITEM_MODES.forEach((mode, i) => {
    const start = 214 + i * 6;
    const hit = start + (mode === 'drop' ? 9 : 4);
    const note = PENTA[MELODY[i] % PENTA.length];
    const panv = -0.6 + ((i * 0.37) % 1.2);
    c(s(hit), ping, holo ? {note, pan: panv} : {note, decay: 0.75, pan: panv}, holo ? 0.45 : 0.3, 0.4, 'melodia');
    if (mode === 'drop') c(s(hit), 'thump', {note: 45, pan: panv}, 0.22, 0.1, 'impact');
  });

  // luzes acendendo + card final
  c(s(330), 'swell', {dur: 1.4}, holo ? 0.45 : 0.6, 0.5, 'final');
  c(s(352), 'whoosh', {dur: 0.9, from: 400, to: 3500, q: 1.6, p0: 0, p1: 0, peak: 0.6}, 0.45, 0.3, 'whoosh');
  // count-up 0→80: ticks acelerando e desacelerando (curva out cubic)
  for (let k = 0; k < 14; k++) {
    const x = k / 13;
    const fr = 356 + (1 - (1 - x) ** (1 / 3)) * 44;
    c(s(fr), 'tick', {tone: 3800 + k * 120, pan: 0.15}, 0.4, 0.1, 'ui');
  }
  [366, 371, 376].forEach((fr, i) => c(s(fr + 3), holo ? 'digi' : 'glass', holo ? {note: 88 + i * 3} : {note: 88 + i * 3, decay: 0.6}, 0.22, 0.4, 'ui'));
  // acorde final
  [76, 83, 88, 91].forEach((nt, i) => c(s(400) + i * 0.035, ping, holo ? {note: nt} : {note: nt, decay: 2.2}, 0.35, 0.6, 'final'));

  return {duration: 15, name: `planta-${variant}`, cues};
};
