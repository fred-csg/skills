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
};
// apelidos usados no HTML
const ALIAS = {tick_hi: 'beep_tick', blip: 'fut_blip', digi: 'beep_tick', beep_retro: 'typing'};
// sons contínuos (não normalizar por pico, não cortar silêncio inicial)
const SUSTAIN = new Set(['bed', 'ticking', 'typing', 'riser_pulse', 'riser_sparkle', 'reverse_swell', 'robot_down', 'gears']);

const cache = {};
function load(id) {
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
  const len = c.dur ? Math.round(c.dur * SR) : (c.loop ? N - start : frames);
  const fi = Math.round((c.fadeIn || 0.004) * SR), fo = Math.round((c.fadeOut ?? (c.dur ? 0.15 : 0)) * SR);
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
  csv.push([c.t, tc, c.id, c.g, c.p || 0, `"${S[id] ? path.basename(S[id]) : id}"`].join(','));
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
