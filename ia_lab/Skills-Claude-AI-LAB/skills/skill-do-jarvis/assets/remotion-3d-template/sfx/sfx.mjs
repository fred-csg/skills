#!/usr/bin/env node
// Gerador de SFX 100% por código (Node puro, zero dependências).
// Uso: node sfx.mjs <cues.mjs> <pastaSaida> [variante]
//   cues.mjs exporta default (variante) => {duration, name, cues: [{t, s, p?, g?, send?, bus?}]}
//   t = segundos, s = nome do som (ver SOUNDS), p = parâmetros, g = ganho linear, send = reverb 0..1
// Saída: <name>.wav (mix final), stems/<bus>.wav (alinhados, p/ Premiere) e <name>-cues.csv
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

export const SR = 48000;
const TAU = Math.PI * 2;

// ─── utilidades ──────────────────────────────────────────────────────────
let seed = 12345;
const rnd = () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646; // RNG semeado: mesmo som sempre
const noise = () => rnd() * 2 - 1;
export const midi = (m) => 440 * 2 ** ((m - 69) / 12);
const len = (sec) => Math.max(1, Math.ceil(sec * SR));
const expLerp = (a, b, t) => a * (b / a) ** t;

// biquad RBJ com frequência variável no tempo
function filter(x, type, freqFn, q = 0.707) {
  const y = new Float32Array(x.length);
  let x1 = 0, x2 = 0, y1 = 0, y2 = 0, b0 = 0, b1 = 0, b2 = 0, a1 = 0, a2 = 0;
  for (let i = 0; i < x.length; i++) {
    if ((i & 15) === 0) {
      const f = Math.min(Math.max(freqFn(i / SR), 20), SR * 0.45);
      const w = (TAU * f) / SR, cs = Math.cos(w), al = Math.sin(w) / (2 * q);
      let n0, n1, n2;
      if (type === 'lp') [n0, n1, n2] = [(1 - cs) / 2, 1 - cs, (1 - cs) / 2];
      else if (type === 'hp') [n0, n1, n2] = [(1 + cs) / 2, -(1 + cs), (1 + cs) / 2];
      else [n0, n1, n2] = [al, 0, -al]; // bp
      const a0 = 1 + al;
      [b0, b1, b2, a1, a2] = [n0 / a0, n1 / a0, n2 / a0, (-2 * cs) / a0, (1 - al) / a0];
    }
    const o = b0 * x[i] + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2;
    x2 = x1; x1 = x[i]; y2 = y1; y1 = o; y[i] = o;
  }
  return y;
}
const f = (v) => () => v;

// envelope: ataque exponencial curto + decaimento exponencial
const envAD = (t, a, d) => (t < a ? t / a : Math.exp(-(t - a) / d));

const mono = (n, fn) => {
  const b = new Float32Array(n);
  for (let i = 0; i < n; i++) b[i] = fn(i / SR, i);
  return b;
};
const add = (a, b, g = 1) => {
  for (let i = 0; i < Math.min(a.length, b.length); i++) a[i] += b[i] * g;
  return a;
};
// mono → estéreo com pan (−1..1) fixo ou função do tempo
const pan = (m, p = 0) => {
  const L = new Float32Array(m.length), R = new Float32Array(m.length);
  for (let i = 0; i < m.length; i++) {
    const pp = typeof p === 'function' ? p(i / m.length) : p;
    const a = ((pp + 1) * Math.PI) / 4;
    L[i] = m[i] * Math.cos(a);
    R[i] = m[i] * Math.sin(a);
  }
  return [L, R];
};

// ─── instrumentos ────────────────────────────────────────────────────────
export const SOUNDS = {
  // "tim" de vidro: parciais inarmônicos com batimento sutil (casa com o look VIDRO)
  glass: ({note = 84, decay = 1.4, pan: p = 0} = {}) => {
    const f0 = midi(note), n = len(decay * 3.2);
    const parts = [[1, 1, 1], [2.76, 0.45, 0.55], [5.4, 0.22, 0.32], [8.93, 0.1, 0.2]];
    const m = mono(n, (t) => {
      let s = 0;
      for (const [r, a, dk] of parts) s += a * Math.sin(TAU * f0 * r * t) * envAD(t, 0.002, decay * dk) * (1 + 0.15 * Math.sin(TAU * 1.7 * t));
      return s * 0.45;
    });
    add(m, filter(mono(len(0.01), (t) => noise() * envAD(t, 0.0005, 0.002)), 'hp', f(5000)), 0.3);
    return pan(m, p);
  },
  // blip digital (look HOLOGRAMA): onda quadrada filtrada + eco curto
  digi: ({note = 84, dur = 0.09, pan: p = 0} = {}) => {
    const f0 = midi(note), n = len(dur + 0.25);
    let ph = 0;
    const raw = mono(n, (t) => {
      ph += (f0 * (1 + 0.04 * Math.exp(-t * 60))) / SR;
      const sq = Math.sign(Math.sin(TAU * ph)) * 0.6 + Math.sin(TAU * ph * 2) * 0.2;
      return sq * envAD(t, 0.001, dur * 0.5);
    });
    const crushed = raw.map((v) => Math.round(v * 10) / 10); // bitcrush leve
    const m = filter(crushed, 'lp', f(midi(note) * 6), 0.9);
    const echo = new Float32Array(n);
    const d = len(0.075);
    for (let i = 0; i < n; i++) echo[i] = m[i] + (i >= d ? m[i - d] * 0.35 : 0) + (i >= 2 * d ? m[i - 2 * d] * 0.12 : 0);
    return pan(echo.map((v) => v * 0.35), p);
  },
  // blip de UI limpo
  blip: ({note = 88, dur = 0.08, pan: p = 0} = {}) => {
    const f0 = midi(note);
    const m = mono(len(dur + 0.1), (t) => (Math.sin(TAU * f0 * t) + 0.3 * Math.sin(TAU * f0 * 2 * t)) * envAD(t, 0.002, dur * 0.4) * 0.4);
    return pan(m, p);
  },
  tick: ({pan: p = 0, tone = 4500} = {}) => {
    const m = filter(mono(len(0.03), (t) => noise() * envAD(t, 0.0003, 0.004)), 'bp', f(tone), 2.5);
    return pan(m.map((v) => v * 0.9), p);
  },
  // whoosh: ruído com banda passante varrendo + pan atravessando
  whoosh: ({dur = 1.2, from = 300, to = 3000, q = 1.4, p0 = -0.7, p1 = 0.7, peak = 0.55} = {}) => {
    const n = len(dur);
    const env = (t) => {
      const x = t / dur;
      return x < peak ? Math.sin(((x / peak) * Math.PI) / 2) ** 2 : Math.cos((((x - peak) / (1 - peak)) * Math.PI) / 2) ** 2;
    };
    const src = mono(n, (t) => noise() * env(t));
    const bp = filter(src, 'bp', (t) => expLerp(from, to, Math.min(t / dur, 1)), q);
    const air = filter(src, 'hp', f(6000));
    const m = add(bp.map((v) => v * 1.6), air, 0.12);
    return pan(m, (x) => p0 + (p1 - p0) * x);
  },
  // riser: ruído clareando + tom subindo, crescendo até o fim
  riser: ({dur = 1.3, from = 110, to = 660} = {}) => {
    const n = len(dur);
    let ph = 0;
    const m = mono(n, (t) => {
      const x = t / dur;
      const fr = expLerp(from, to, x);
      ph += fr / SR;
      const tone = Math.sin(TAU * ph) * 0.5 + Math.sin(TAU * ph * 1.5) * 0.25 + Math.sin(TAU * ph * 2.01) * 0.2;
      return (tone * 0.6 + noise() * 0.5) * x ** 2.2 * (x > 0.97 ? (1 - x) / 0.03 : 1);
    });
    const out = filter(m, 'hp', (t) => expLerp(150, 2500, t / dur), 0.8);
    return pan(out.map((v) => v * 0.7), (x) => 0.4 * Math.sin(x * 9));
  },
  // impacto: sub com queda de pitch + corpo de ruído + clique
  impact: ({size = 1} = {}) => {
    const n = len(1.8 * size);
    let ph = 0;
    const sub = mono(n, (t) => {
      ph += (38 + 90 * Math.exp(-t * 14)) / SR;
      return Math.tanh(Math.sin(TAU * ph) * 1.8) * envAD(t, 0.002, 0.55 * size);
    });
    const body = filter(mono(n, (t) => noise() * envAD(t, 0.001, 0.09)), 'lp', (t) => 2400 * Math.exp(-t * 6) + 200);
    const click = filter(mono(len(0.01), (t) => noise() * envAD(t, 0.0002, 0.0015)), 'hp', f(3000));
    const m = add(add(sub.map((v) => v * 0.9), body, 0.7), click, 0.4);
    return pan(m, 0);
  },
  // baque suave (parede/peça encaixando)
  thump: ({note = 40, pan: p = 0} = {}) => {
    let ph = 0;
    const f0 = midi(note);
    const m = mono(len(0.35), (t) => {
      ph += (f0 * (1 + 0.6 * Math.exp(-t * 30))) / SR;
      return Math.sin(TAU * ph) * envAD(t, 0.002, 0.08);
    });
    add(m, filter(mono(len(0.06), (t) => noise() * envAD(t, 0.0005, 0.012)), 'lp', f(900)), 0.5);
    return pan(m.map((v) => v * 0.8), p);
  },
  // varredura de scan (holograma / blueprint desenhando)
  scan: ({dur = 2, from = 500, to = 1800} = {}) => {
    const n = len(dur);
    let ph = 0;
    const m = mono(n, (t) => {
      const x = t / dur;
      ph += expLerp(from, to, x) / SR;
      const trem = 0.6 + 0.4 * Math.sin(TAU * 28 * t);
      return Math.sin(TAU * ph) * trem * Math.sin(Math.PI * x) ** 1.5 * 0.18;
    });
    const hiss = filter(mono(n, (t) => noise() * Math.sin((Math.PI * t) / dur) * 0.25), 'bp', (t) => expLerp(from * 3, to * 3, t / dur), 4);
    return pan(add(m, hiss, 1), (x) => -0.5 + x);
  },
  // swell quente (luzes acendendo)
  swell: ({dur = 1.6, notes = [52, 59, 64, 66, 71]} = {}) => {
    const n = len(dur + 1.2);
    const m = mono(n, (t) => {
      const e = t < dur ? (t / dur) ** 2 : Math.exp(-(t - dur) / 0.45);
      let s = 0;
      for (const nt of notes) s += Math.sin(TAU * midi(nt) * t) + 0.3 * Math.sin(TAU * midi(nt) * 2.003 * t);
      return (s / notes.length) * e * 0.5;
    });
    return pan(filter(m, 'lp', (t) => 600 + 3000 * Math.min(t / dur, 1)), 0);
  },
  // cama sonora (pad) com filtro respirando
  pad: ({dur = 15, notes = [40, 47, 50, 54, 55, 62], fadeIn = 2, fadeOut = 1.6} = {}) => {
    const n = len(dur);
    const L = new Float32Array(n), R = new Float32Array(n);
    notes.forEach((nt, k) => {
      for (const det of [-0.08, 0.08]) {
        const fr = midi(nt + det);
        const side = det < 0 ? L : R;
        for (let i = 0; i < n; i++) {
          const t = i / SR;
          let s = 0;
          for (let h = 1; h <= 5; h++) s += Math.sin(TAU * fr * h * t + k) / h ** 1.6;
          side[i] += s * 0.06;
        }
      }
    });
    const env = (t) => Math.min(1, t / fadeIn) * Math.min(1, (dur - t) / fadeOut) * (0.85 + 0.15 * Math.sin(TAU * 0.18 * t));
    const lfo = (t) => 500 + 700 * (0.5 + 0.5 * Math.sin(TAU * 0.07 * t - 1.2));
    return [filter(L, 'lp', lfo, 0.9).map((v, i) => v * env(i / SR)), filter(R, 'lp', lfo, 0.9).map((v, i) => v * env(i / SR))];
  },
};

// ─── reverb (Freeverb simplificado) ──────────────────────────────────────
function reverb([L, R], {room = 0.86, damp = 0.35, wet = 1} = {}) {
  const combs = [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617].map((c) => Math.round((c * SR) / 44100));
  const aps = [556, 441, 341, 225].map((c) => Math.round((c * SR) / 44100));
  const run = (x, spread) => {
    const out = new Float32Array(x.length);
    for (const c of combs) {
      const size = c + spread, buf = new Float32Array(size);
      let idx = 0, store = 0;
      for (let i = 0; i < x.length; i++) {
        const o = buf[idx];
        store = o * (1 - damp) + store * damp;
        buf[idx] = x[i] * 0.015 + store * room;
        idx = (idx + 1) % size;
        out[i] += o;
      }
    }
    for (const a of aps) {
      const size = a + spread, buf = new Float32Array(size);
      let idx = 0;
      for (let i = 0; i < x.length; i++) {
        const b = buf[idx], o = -out[i] + b;
        buf[idx] = out[i] + b * 0.5;
        idx = (idx + 1) % size;
        out[i] = o;
      }
    }
    return out.map((v) => v * wet);
  };
  return [run(L, 0), run(R, 23)];
}

// ─── WAV 24-bit estéreo ──────────────────────────────────────────────────
export function writeWav(file, [L, R]) {
  const n = L.length, bytes = 3, data = Buffer.alloc(n * 2 * bytes), head = Buffer.alloc(44);
  for (let i = 0; i < n; i++)
    for (const [c, ch] of [[0, L], [1, R]]) {
      const v = Math.max(-1, Math.min(1, ch[i])) * 8388607;
      data.writeIntLE(Math.round(v), (i * 2 + c) * bytes, 3);
    }
  head.write('RIFF', 0); head.writeUInt32LE(36 + data.length, 4); head.write('WAVE', 8);
  head.write('fmt ', 12); head.writeUInt32LE(16, 16); head.writeUInt16LE(1, 20); head.writeUInt16LE(2, 22);
  head.writeUInt32LE(SR, 24); head.writeUInt32LE(SR * 2 * bytes, 28); head.writeUInt16LE(2 * bytes, 32); head.writeUInt16LE(24, 34);
  head.write('data', 36); head.writeUInt32LE(data.length, 40);
  fs.mkdirSync(path.dirname(file), {recursive: true});
  fs.writeFileSync(file, Buffer.concat([head, data]));
}

const dbfs = (v) => (20 * Math.log10(v + 1e-12)).toFixed(1);

// ─── mixagem a partir da lista de cues ───────────────────────────────────
export function render({duration, name, cues}, outDir) {
  const n = len(duration);
  const buses = {};
  const send = [new Float32Array(n), new Float32Array(n)];
  for (const c of cues) {
    const [l, r] = SOUNDS[c.s](c.p ?? {});
    const bus = (buses[c.bus ?? c.s] ??= [new Float32Array(n), new Float32Array(n)]);
    const off = Math.round(c.t * SR), g = c.g ?? 1, sd = c.send ?? 0.25;
    for (let i = 0; i < l.length && off + i < n; i++) {
      if (off + i < 0) continue;
      bus[0][off + i] += l[i] * g; bus[1][off + i] += r[i] * g;
      send[0][off + i] += l[i] * g * sd; send[1][off + i] += r[i] * g * sd;
    }
  }
  const [vl, vr] = reverb(send);
  buses.reverb = [vl, vr];
  const mix = [new Float32Array(n), new Float32Array(n)];
  for (const [l, r] of Object.values(buses)) { add(mix[0], l); add(mix[1], r); }
  // fade final + limitador suave + normalização de pico em −1 dBFS
  for (let i = 0; i < n; i++) {
    const fo = Math.min(1, (n - i) / (SR * 0.4));
    mix[0][i] = Math.tanh(mix[0][i] * 1.1) * fo; mix[1][i] = Math.tanh(mix[1][i] * 1.1) * fo;
  }
  let peak = 0, sq = 0;
  for (let i = 0; i < n; i++) { peak = Math.max(peak, Math.abs(mix[0][i]), Math.abs(mix[1][i])); sq += mix[0][i] ** 2 + mix[1][i] ** 2; }
  const norm = 0.891 / peak;
  for (const ch of mix) for (let i = 0; i < n; i++) ch[i] *= norm;
  writeWav(path.join(outDir, `${name}.wav`), mix);
  for (const [b, st] of Object.entries(buses)) writeWav(path.join(outDir, 'stems', name, `${b}.wav`), st.map((ch) => ch.map((v) => v * norm)));
  fs.writeFileSync(path.join(outDir, `${name}-cues.csv`), 'tempo_s;som;ganho\n' + cues.map((c) => `${c.t.toFixed(3)};${c.s};${c.g ?? 1}`).join('\n'));
  const rms = Math.sqrt(sq / (2 * n)) * norm;
  console.log(`${name}: ${duration}s · ${cues.length} cues · pico −1.0 dBFS · RMS ${dbfs(rms)} dBFS · stems: ${Object.keys(buses).join(', ')}`);
}

// CLI
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [cueFile, outDir = '.', variant] = process.argv.slice(2);
  if (!cueFile) {
    console.log('uso: node sfx.mjs <cues.mjs> <pastaSaida> [variante]');
    process.exit(1);
  }
  const mod = await import(pathToFileURL(path.resolve(cueFile)).href);
  const specs = [].concat(mod.default(variant));
  for (const s of specs) render(s, outDir);
}
