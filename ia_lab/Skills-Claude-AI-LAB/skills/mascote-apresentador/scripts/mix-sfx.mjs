// Mixa as cues exportadas do index.html usando a biblioteca de SFX do Lucas (Ocular + avulsos em ADDONS/SFX).
// uso: node scripts/mix-sfx.mjs <cues.json> <saida.wav> [LUFS alvo, padrão -16]
// Saída: <saida>.wav (mix masterizado) + <saida>-cues.csv (lista pra conferir no Premiere)
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {execFileSync, spawnSync} from 'node:child_process';
import ffmpeg from 'ffmpeg-static';

const SR = 48000;
const [cuesPath, outWav, lufsArg] = process.argv.slice(2);
const TARGET = +(lufsArg || -16);

const OC = 'E:/Dropbox/ADDONS/SFX/Ocular Sounds/Ocular Sounds/Sound Effects - The Ultimate Sound FX Bundle (All in One)/The Ultimate Sound FX Bundle/';
const AD = 'E:/Dropbox/ADDONS/SFX/';
const UI = AD + 'COMPILED SELECTIONS/UI MOTION - Reel Timi (sound design)/';
const MC = AD + 'COMPILED SELECTIONS/MECANICOS - Reel Alvin Juan (cliques, catraca, obturador)/';
const S = {
  click_short: OC + 'The Complete Devices Collection/Camera Shutters/COMCam_Short Click_Camera Shutters.wav',
  click_metal: OC + 'The Complete Devices Collection/Camera Shutters/COMCam_Pre Shifted Very Short Metal Click_Camera Shutters.wav',
  pop_soft: OC + 'The Complete Devices Collection/Camera Shutters/COMCam_Kissy Short Shutter_Camera Shutters.wav',
  snap_elastic: OC + 'The Complete Devices Collection/Camera Shutters/COMCam_Quick Shutter, Button Pullback_Camera Shutters.wav',
  beep_tick: OC + 'The Complete Devices Collection/Camera Shutters/COMCam_Short Beep Shutter_Camera Shutters.wav',
  whip_a: OC + 'The Complete Whooshes Collection/Quick Whips/DSGNWhsh_Short Whip, Short Whoosh 3_Quick Whips.wav',
  whip_b: OC + 'The Complete Whooshes Collection/Quick Whips/DSGNWhsh_Short Whip, Short Whoosh 9_Quick Whips.wav',
  whip_c: OC + 'The Complete Whooshes Collection/Quick Whips/DSGNWhsh_Short Whip, Short Whoosh 17_Quick Whips.wav',
  whip_d: OC + 'The Complete Whooshes Collection/Quick Whips/DSGNWhsh_Short Whip, Short Whoosh 24_Quick Whips.wav',
  swipe_paper: OC + 'The Complete Whooshes Collection/Short Whooshes/DSGNWhsh_Quick Whoosh, Paper Drag, Soft_Short Whooshes.wav',
  swipe_rl: OC + 'The Complete Whooshes Collection/Short Whooshes/DSGNWhsh_Quick Whoosh, Deep, Filtered, Right to Left_Short Whooshes.wav',
  swipe_sand: OC + 'The Complete Whooshes Collection/Short Whooshes/DSGNWhsh_Quick Whoosh, Crackling, Sand, Left to Right_Short Whooshes.wav',
  whoosh_exhale: OC + 'The Complete Whooshes Collection/Short Whooshes/DSGNWhsh_Quick Whoosh, Exhale, Deep, Filtered_Short Whooshes.wav',
  reverse_swell: OC + 'The Complete Impacts Collection/Epic Hits Vol. 2/DSGNImpt_Reversed Glass Rising, Soft Metal Hit Crassh,_Epic Hits Vol 2.wav',
  impact_soft: OC + 'The Complete Impacts Collection/Deep Impacts/DSGNImpt_Soft Transient, Deep Drum Hit_Deep Impacts.wav',
  impact_low: OC + 'The Complete Impacts Collection/Deep Impacts/DSGNImpt_Deep Single Hit Impact_Deep Impacts.wav',
  final_hit: OC + 'The Complete Impacts Collection/Deep Impacts/DSGNImpt_Whooshy Impact, Reverb Synth, Bmaj_Deep Impacts.wav',
  sub_tail: OC + 'The Complete Impacts Collection/Deep Impacts/DSGNImpt_Acouctic Bass Impact, Long Tail_Deep Impacts.wav',
  tonal_accent: OC + 'The Complete Impacts Collection/Powerful Braaams/DSGNBram_High End Airy Synth Oneshot, Key F_Powerful Braaams.wav',
  bass_mecha: OC + 'The Complete Impacts Collection/Bass Drops/DSGNBass_Distorted Mecha Hit, Low Electro Decrease, Short Reverb_Bass Drops.wav',
  gears: OC + 'The Cinematic Elements Collection/Cinematic Mechanics/COMCam_Mech Mini Gears Rotation 1_Cinematic Mechanics.wav',
  ticking: OC + 'The Complete Drones Collection/Granular Drones/DSGNDron_Mechanical, Ticking, Loop_Granular Drones.wav',
  bed: OC + 'The Complete Drones Collection/Granular Drones/DSGNDron_Vast, Bright, Airy, Loop, Key Gmaj_Granular Drones.wav',
  mech_lock: OC + 'The Complete Sci-Fi Collection/Sounds of Spaceships/SCIDoor_Spaceship Door Locking System 1_Sounds of Spaceships.wav',
  riser_pulse: OC + 'The Complete Risers Collection/Tonal Risers/DSGNRise_Stepping Riser, Rythmic, Reverb_Tonal Risers.wav',
  riser_sparkle: OC + 'The Complete Risers Collection/Tonal Risers/DSGNRise_Short Sparkling Synth Riser, No Reverb_Tonal Risers.wav',
  glitch: OC + 'The Complete Sci-Fi Collection/Sci-Fi Glitches/UIGlitch-Futuristic_Machines Devices-Glitch 12_Sci-Fi Glitches.wav',
  glitch2: OC + 'The Complete Sci-Fi Collection/Sci-Fi Glitches/UIGlitch-Futuristic_Machines Devices-Glitch 3_Sci-Fi Glitches.wav',
  glitch3: OC + 'The Complete Sci-Fi Collection/Sci-Fi Glitches/UIGlitch-Futuristic_Machines Devices-Glitch 27_Sci-Fi Glitches.wav',
  robot_down: OC + 'The Complete Sci-Fi Collection/Robots & Machines/ROBTMvmt_Futuristic Robot, Electric Glitch, Servo Motor, Slow Down 1_Sounds of Robots & Machines.wav',
  servo_init: OC + 'The Complete Sci-Fi Collection/Robots & Machines/ROBTMvmt_Futuristic Robot, Servo Motor, System Initiation 1_Sounds of Robots & Machines.wav',
  mouse: AD + 'InspectorJ - Working From Home - Computer Mouse Single Click .aac',
  typing: AD + 'Vadi Sound - Qwerty - Computer Keyboard Quick Typing (1).aac',
  glitchy_counter: AD + 'Phil Michalski - UI - Glitchy Counter.aac',
  glitchy_bleep: AD + 'Phil Michalski - UI - Glitchy Bleep.aac',
  bursting_bleep: AD + 'Phil Michalski - UI - Bursting Bleep.aac',
  chime: AD + 'Skyclad Sound - Data Point - UI Bright Chime.aac',
  msg_bleep: AD + 'Unrealsfx - Cyberpunk - UI Message Bleep.aac',
  app_open: AD + 'Unrealsfx - Cyberpunk - UI Micro App Open.aac',
  tonal_beeps: AD + 'Unrealsfx - Sci Tech Transitions - Glitchy Tonal Digital Beeps Eb to Gb.aac',
  elec_ui: AD + 'Epic Stock Media - Advanced UI - Electric Interface .aac',
  stutter_whoosh: AD + 'Sound Surgeon - Cinematic State - Alien Stutter Whoosh.aac',
  braam: AD + 'Artlist Studios - Braamagog - Low Braam.aac',
  fut_blip: AD + 'DeanKR - UI Mechanisms - Button Futuristic Downwards Blip .aac',
  // UI MOTION (COMPILED SELECTIONS) — base oficial pra cards, pílulas e mãos do mascote
  ui_click: UI + 'UI_01_CLICK_00.04s.wav', ui_click2: UI + 'UI_05_CLICK_00.64s.wav',
  ui_pop: UI + 'UI_04_POP_00.51s.wav', ui_pop2: UI + 'UI_10_POP_01.67s.wav',
  ui_swish: UI + 'UI_07_SWISH_00.97s.wav', ui_swish2: UI + 'UI_17_SWISH_03.08s.wav',
  ui_whoosh: UI + 'UI_11_WHOOSH_01.85s.wav', ui_impact: UI + 'UI_13_IMPACT_02.34s.wav', ui_impact2: UI + 'UI_24_IMPACT_08.38s.wav',
  mec_click: MC + '07_CLICK.wav', mec_catraca: MC + '09_CATRACA_MECANICA.wav', obturador: MC + '06_OBTURADOR_CLICK.wav',
};
// apelidos usados no HTML
const ALIAS = {tick_hi: 'beep_tick', blip: 'fut_blip', digi: 'beep_tick', beep_retro: 'typing'};
// sons contínuos (não normalizar por pico, não cortar silêncio inicial)
const SUSTAIN = new Set(['bed', 'ticking', 'typing', 'riser_pulse', 'riser_sparkle', 'reverse_swell', 'robot_down', 'gears']);

// ===== BANCO DO MASCOTE — SÓ a pasta COMPILED SELECTIONS (pedido do Lucas). Variações alternam sozinhas a cada uso. =====
// Sons longos da raiz (mecânicos, pedra, água) entram CORTADOS (TRIM, com fade) — viram acento, nunca ambiência.
const CSR = AD + 'COMPILED SELECTIONS/', AV = MC + 'avulsos/';
const cs = (n) => CSR + n + '.wav', ui = (n) => UI + n + '.wav', mc = (n) => MC + n + '.wav', av = (n) => AV + n + '.wav';
Object.assign(S, {
  m_pop: ['UI_04_POP_00.51s', 'UI_10_POP_01.67s', 'UI_12_POP_02.11s', 'UI_21_POP_07.81s', 'UI_22_POP_07.99s', 'UI_23_POP_08.16s', 'UI_27_POP_10.14s', 'UI_28_POP_10.34s'].map(ui),
  m_click: ['UI_01_CLICK_00.04s', 'UI_02_CLICK_00.18s', 'UI_03_CLICK_00.32s', 'UI_05_CLICK_00.64s', 'UI_06_CLICK_00.81s', 'UI_08_CLICK_01.28s', 'UI_14_CLICK_02.63s', 'UI_15_CLICK_02.76s', 'UI_16_CLICK_02.91s', 'UI_19_CLICK_06.96s', 'UI_25_CLICK_09.87s', 'UI_26_CLICK_10.01s'].map(ui)
    .concat(['HIT_02_CLICK_00.24s', 'HIT_05_CLICK_00.74s', 'HIT_09_CLICK_04.10s', 'HIT_13_CLICK_05.34s', 'HIT_17_CLICK_06.53s', 'HIT_21_CLICK_08.12s', 'HIT_26_CLICK_09.71s'].map(av)),
  m_swish: ['UI_07_SWISH_00.97s', 'UI_09_SWISH_01.42s', 'UI_17_SWISH_03.08s', 'UI_18_SWISH_04.29s'].map(ui),
  m_whip: [ui('UI_11_WHOOSH_01.85s'), mc('12_WHOOSH'), mc('15_WHOOSH_b'), ui('UI_20_SWISH_07.10s')],
  m_impact: [ui('UI_13_IMPACT_02.34s'), av('HIT_24_IMPACT_08.77s'), av('HIT_29_IMPACT_10.63s'), ui('UI_29_IMPACT_10.58s'), ui('UI_24_IMPACT_08.38s')],
  m_mec: ['02_CLICK_x2', '05_CLICK_x2_b', '07_CLICK', '13_CLICK_x2_c'].map(mc),
  m_rajada: [mc('11_CLICK_x5'), mc('01_RISER_E_CLIQUES_x10')],                 // digitação, cronômetro, contagem
  m_catraca: [mc('03_CATRACA_MECANICA_x3'), mc('09_CATRACA_MECANICA')],
  m_shutter: ['04_OBTURADOR_x2', '06_OBTURADOR_CLICK', '08_OBTURADOR_CLICK_b', '10_OBTURADOR_x2_b', '14_OBTURADOR_CLICK_c'].map(mc),
  // acentos criativos (favoritos da raiz, cortados)
  m_hit: [cs('ROCKBrk_Dry Break Impact, Crispy, Small Rise And Hit_Cinematic Stone'), cs('COMCam_Camera Clicks, Low Impact, Mech Double Hit_Cinematic Mechanics'), cs('MECHLvr_Metal Lever Activation_Cinematic Mechanics')],
  m_sparkle: [cs('MACHGym_Foley Kit, Treadmill Start Button, Tone_Cinematic Gym'), cs('COMCam_Mech Mini Gears, Camera Switch Buttons_Cinematic Mechanics'), cs('COMCam_Mech Mini Gears, Camera Wind, Handling, Clicks, Shutter_Cinematic Mechanics')],
  m_magic: [cs('COMCam_Mech Mini Gears Rotation 3_Cinematic Mechanics'), cs('CLOCKMech_Multi Small Gear Rotation, Double Low Whoosh_Cinematic Mechanics'), cs('DSGNGran_Synth Bass Double Whoosh, Crispy Gears, Sharp Robot 2_Cinematic Mechanics')],
  m_morph: [cs('ROCKMvmt_Sequence, Liquid Rocks, Multi Whoosh and Impact_Cinematic Stone'), cs('CLOCKMech_Time Control Clock, Pendulum Transition_Cinematic Mechanics'), cs('ROCKMvmt_Sequence, Granular Rocks, Multi Whoosh_Cinematic Stone')],
  m_bell: [cs('CLOCKMech_Agressive Impact, Alarm Clock Wing_Cinematic Mechanics'), cs('CLOCKMech_Agressive Impact, Alarm Clock Wing, Weird High Resonance_Cinematic Mechanics')],
  m_bubble: [cs('WATRBubl_Processed, Bubbles, Water Movements, Sequence 2_Cinematic Water')],
  m_paper: [cs('OBJBook_Book Page Flip, Deep Fast Tremolo_Cinematic Mechanics')],
  m_assemble: [cs('MECHGear_Agressive Impact, Assembling Metal Parts, Slowing Down 1_Cinematic Mechanics'), cs('ROCKBrk_Rock Yielding To Pressure, Low Granular Crackles_Cinematic Stone')],
});

// CONSTRUÇÃO — família do som favorito do Lucas (Ocular › Cinematic Elements › Cinematic Stone: "Dry Break Impact, Crispy, Small Rise And Hit").
// Subida curta + batida crocante/tecnológica. WIN = [antes, depois] do pico: a batida cai NO elemento (use whoosh(t,'m_build') = alinha o pico).
const ST = OC + 'The Cinematic Elements Collection/Cinematic Stone/', st = (n) => ST + n + '_Cinematic Stone.wav';
S.m_build = ['ROCKBrk_Dry Break Impact, Crispy, Small Rise And Hit', 'ROCKImpt_Short Rise and Hit, Dry Rocks Soft Crackles, Crispy', 'ROCKImpt_Short Bass Rise, Organic Stones Impact',
  'ROCKImpt_Short Rise, Granular Rocks Hit, Soft Crackles, Smooth Bass', 'ROCKImpt_Short Rise and Hit, Molten Rocks Soft Crackles, Smooth Bass, Slimmy Tail Tone',
  'ROCKImpt_Rise and Hit, Molten Rocks Soft Crackles, High Electronic Whistling, Smooth Bass', 'ROCKBrk_Short Rise and Hit, Smooth Massive Rocks Breaks And Impact, Light Bass Synth',
  'ROCKTonl_Short Sequence, Granular Low Hit, High Tonal', 'ROCKTonl_Short Sequence, Tonal Scratchs, High Tonal', 'ROCKImpt_Whoosh and Hit, Granular Rocks Crackles, Heavy Crispy Clicks, Smooth Bass',
  'ROCKMvmt_Short Sequence, Liquid Rocks, Crispy, Multi Whoosh 1', 'ROCKMvmt_Short Sequence, Granular Rocks, Crispy, Multi Whoosh'].map(st);
S.m_build1 = [st('ROCKBrk_Dry Break Impact, Crispy, Small Rise And Hit')];   // o original, pros momentos principais
const WIN = {m_build: [0.5, 0.65], m_build1: [0.6, 0.9]};

// UI POP - Reel Sumama (sound design Drive) — o Lucas amou os pops: viram o POP principal (m_pop), Timi fica em m_popt
const SU = AD + 'COMPILED SELECTIONS/UI POP - Reel Sumama (sound design Drive)/', su = (n) => SU + n + '.wav';
S.m_popt = S.m_pop;
S.m_pop = ['UI_08_POP_03.15s', 'UI_09_POP_03.36s', 'UI_11_POP_04.34s', 'UI_12_POP_04.48s', 'UI_13_POP_04.67s', 'UI_14_POP_04.81s', 'UI_16_POP_05.43s', 'UI_21_POP_06.55s', 'UI_23_POP_07.04s', 'UI_24_POP_07.28s',
  'UI_25_POP_07.42s', 'UI_26_POP_07.59s', 'UI_29_POP_08.02s', 'UI_30_POP_08.18s', 'UI_33_POP_09.00s', 'UI_35_POP_10.02s', 'UI_36_POP_10.22s'].map(su);
S.m_click = ['UI_01_CLICK_00.03s', 'UI_02_CLICK_00.20s', 'UI_04_CLICK_00.99s', 'UI_06_CLICK_02.25s', 'UI_07_CLICK_02.39s', 'UI_17_CLICK_05.57s', 'UI_19_CLICK_06.11s', 'UI_27_CLICK_07.72s', 'UI_28_CLICK_07.85s', 'UI_39_CLICK_12.06s'].map(su).concat(S.m_click);
S.m_swish = ['UI_05_SWISH_01.12s', 'UI_18_SWISH_05.84s', 'UI_10_SWISH_03.50s', 'UI_03_SWISH_00.33s'].map(su).concat(S.m_swish);
S.m_whip = ['UI_20_WHOOSH_06.24s', 'UI_32_WHOOSH_08.69s'].map(su).concat(S.m_whip);
S.m_impact = ['UI_15_IMPACT_05.03s', 'UI_22_IMPACT_06.71s', 'UI_31_IMPACT_08.31s', 'UI_34_IMPACT_09.16s', 'UI_37_IMPACT_10.43s'].map(su).concat(S.m_impact);
// duração máxima (s) de cada id — corta com fade pra nunca virar ambiência
const TRIM = {m_hit: 0.8, m_sparkle: 0.6, m_magic: 0.9, m_morph: 0.9, m_bell: 0.7, m_bubble: 0.4, m_paper: 0.5, m_assemble: 0.8, m_catraca: 0.9, m_rajada: 0.6, m_impact: 0.7};

const cache = {};
const VAR = {};
function load(id) {
  if (Array.isArray(S[id])) { const lst = S[id], k = (VAR[id] = (VAR[id] ?? -1) + 1) % lst.length; const key = id + '#' + k; if (!(key in cache)) { const keep = S[id]; S[id] = lst[k]; cache[key] = loadOne(id); delete cache[id]; S[id] = keep; } return cache[key]; }
  return loadOne(id);
}
function loadOne(id) {
  if (id in cache) return cache[id];
  // 1º biblioteca do acervo; senão <projeto>/sfx/<id>.(wav|mp3) (ex.: gerado no ElevenLabs); senão pula a cue
  let file = S[id];
  if (!file || !fs.existsSync(file)) file = ['wav', 'mp3'].map((e) => path.join(process.cwd(), 'sfx', `${id}.${e}`)).find((f) => fs.existsSync(f));
  if (!file) { console.warn(`SFX ausente, cue pulada: ${id}`); return (cache[id] = null); }
  const raw = execFileSync(ffmpeg, ['-nostdin', '-loglevel', 'error', '-i', file, '-f', 'f32le', '-ac', '2', '-ar', String(SR), '-'], {maxBuffer: 1 << 30});
  let x = new Float32Array(raw.buffer, raw.byteOffset, raw.byteLength / 4);
  let peak = 0;
  for (const v of x) peak = Math.max(peak, Math.abs(v));
  // corta silêncio inicial dos one-shots (o transiente cai exatamente na cue)
  if (!SUSTAIN.has(id)) {
    let i = 0;
    while (i < x.length && Math.abs(x[i]) < peak * 0.04) i++;
    i = Math.max(0, (i >> 1) * 2 - 2 * Math.round(SR * 0.004));
    x = x.slice(i);
  } else x = x.slice();
  // normaliza pelo pico, mas limita o RMS: sons densos (crest baixo) não podem soar mais altos que os transientes
  let ss = 0;
  for (const v of x) ss += v * v;
  const rms = Math.sqrt(ss / x.length);
  let norm = peak > 0 ? 0.9 / peak : 1;
  const RMS_CAP = 0.9 * 10 ** (-18 / 20);
  if (rms * norm > RMS_CAP) norm *= RMS_CAP / (rms * norm);
  for (let i = 0; i < x.length; i++) x[i] *= norm;
  let pi = 0, pv = 0;
  for (let i = 0; i < x.length; i++) if (Math.abs(x[i]) > pv) { pv = Math.abs(x[i]); pi = i; }
  x.peakSec = (pi >> 1) / SR;
  if (WIN[id]) {               // recorta em volta do pico (subida curta antes, rabo curto depois) com fades
    const [pre, post] = WIN[id], pf = pi >> 1, a = Math.max(0, pf - Math.round(pre * SR)), b = Math.min(x.length >> 1, pf + Math.round(post * SR));
    const y = x.slice(a * 2, b * 2), n = y.length >> 1, fin = Math.round(Math.min(pre, (pf - a) / SR) * 0.6 * SR), fout = Math.round(post * 0.6 * SR);
    for (let i = 0; i < n; i++) { let e = 1; if (i < fin) e *= i / fin; if (i > n - fout) e *= Math.max(0, (n - i) / fout); y[2 * i] *= e; y[2 * i + 1] *= e; }
    y.peakSec = (pf - a) / SR; return (cache[id] = y);
  }
  return (cache[id] = x);
}

const {duration, cues} = JSON.parse(fs.readFileSync(cuesPath, 'utf8'));
const N = Math.ceil((duration + 1.5) * SR);
const L = new Float32Array(N), R = new Float32Array(N);
const csv = ['tempo,timecode,id,ganho,pan,arquivo'];

for (const c of cues) {
  const id = ALIAS[c.id] || c.id;
  const src = load(id);
  if (!src) continue;
  const frames = src.length / 2;
  const start = Math.round((c.align === 'peak' ? c.t - src.peakSec : c.t) * SR);
  const tr = TRIM[id] && !c.dur ? Math.min(frames, Math.round(TRIM[id] * SR)) : 0;
  const len = c.dur ? Math.round(c.dur * SR) : tr || (c.loop ? N - start : frames);
  const fi = Math.round((c.fadeIn || 0.004) * SR), fo = Math.round((c.fadeOut ?? (c.dur ? 0.15 : tr ? Math.min(0.25, TRIM[id] * 0.4) : 0)) * SR);
  const p = Math.max(-1, Math.min(1, c.p || 0));
  const gl = c.g * Math.min(1, 1 - p) * (p < 0 ? 1 + 0.25 * -p : 1), gr = c.g * Math.min(1, 1 + p) * (p > 0 ? 1 + 0.25 * p : 1);
  for (let k = 0; k < len; k++) {
    const o = start + k;
    if (o >= N) break;
    if (o < 0) continue;
    let j = k;
    if (j >= frames) { if (!c.loop) break; j %= frames; }
    let env = 1;
    if (k < fi) env *= k / fi;
    if (fo && k > len - fo) env *= Math.max(0, (len - k) / fo);
    if (c.duck) for (const [a, b, lvl] of c.duck) {
      const tt = o / SR, rmp = 0.5;
      let d = 1;
      if (tt > a - rmp && tt < b + rmp) d = tt < a ? 1 - (1 - lvl) * ((tt - a + rmp) / rmp) : tt > b ? lvl + (1 - lvl) * ((tt - b) / rmp) : lvl;
      env *= d;
    }
    L[o] += src[2 * j] * gl * env;
    R[o] += src[2 * j + 1] * gr * env;
  }
  const tc = `${String(Math.floor(c.t / 60)).padStart(2, '0')}:${(c.t % 60).toFixed(2).padStart(5, '0')}`;
  csv.push([c.t, tc, c.id, c.g, c.p || 0, `"${id}"`].join(','));
}

// interleave → raw → mede loudness → aplica ganho + limitador
const inter = new Float32Array(N * 2);
for (let i = 0; i < N; i++) { inter[2 * i] = L[i]; inter[2 * i + 1] = R[i]; }
const tmp = path.join(os.tmpdir(), `sfxmix_${process.pid}.f32`);
fs.writeFileSync(tmp, Buffer.from(inter.buffer));
let I = -20;
{

  const r = spawnSync(ffmpeg, ['-nostdin', '-hide_banner', '-f', 'f32le', '-ar', String(SR), '-ac', '2', '-i', tmp, '-af', 'loudnorm=print_format=json', '-f', 'null', '-'], {encoding: 'utf8'});
  const m = r.stderr.match(/"input_i"\s*:\s*"(-?[\d.]+)"/);
  if (m) I = +m[1];
  const gain = TARGET - I;
  execFileSync(ffmpeg, ['-nostdin', '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', String(SR), '-ac', '2', '-i', tmp,
    '-af', `volume=${gain.toFixed(2)}dB,alimiter=limit=0.84:attack=2:release=60:level=disabled`, '-c:a', 'pcm_s24le', outWav]);
  fs.rmSync(tmp);
  fs.writeFileSync(outWav.replace(/\.wav$/i, '-cues.csv'), csv.join('\n'));
  console.log(`${cues.length} cues · loudness bruto ${I} LUFS → ganho ${gain.toFixed(1)} dB (alvo ${TARGET}) → ${outWav}`);
}
