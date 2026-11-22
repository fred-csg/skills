import {loadFont as loadPoppins} from '@remotion/google-fonts/Poppins';
import {measureText} from '@remotion/layout-utils';
import React from 'react';
import {AbsoluteFill, Easing, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {BLOCOS, Bloco, Key, Line} from './blocos';
import analise from './data/analise.json';
import palavras from './data/palavras.json';

// fonte padrão: Poppins (Bold nas palavras comuns, Black nas palavras-chave)
const poppins = loadPoppins('normal', {weights: ['600', '700', '900'], subsets: ['latin', 'latin-ext']});
const poppinsItalic = loadPoppins('italic', {weights: ['700'], subsets: ['latin', 'latin-ext']});
const inter = poppins;
const interItalic = poppinsItalic;
const rubik = poppins;

export const FPS = 24;
const W = 1080;
const H = 1920;
const ACCENT = '#ff6619'; // trocar pela cor amostrada da cena (analise.json → cores[0])
const N = analise.n;
// margem CENTRAL: nada encosta nas bordas, tudo fica nos ~76% do meio da tela
const M = Math.round(W * 0.12);
const TOP = 150;
const BOTTOM = H - 190;

// largura real do texto (fonte já carregada); cache por chave
const mcache = new Map<string, number>();
const textW = (text: string, fontFamily: string, fontSize: number, fontWeight: string | number, italic = false) => {
  const key = `${text}|${fontFamily}|${fontWeight}|${italic}`;
  let w1 = mcache.get(key);
  if (w1 === undefined) {
    w1 = measureText({text, fontFamily, fontSize: 100, fontWeight: String(fontWeight), letterSpacing: '0px', ...(italic ? {fontVariantNumeric: undefined} : {})}).width / 100;
    mcache.set(key, w1);
  }
  return w1 * fontSize;
};

type Word = {w: string; a: number; b: number};
const WORDS = palavras as Word[];
const fr = (sec: number) => Math.round(sec * FPS);

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const prog = (f: number, a: number, b: number, ease = Easing.out(Easing.cubic)) => interpolate(f, [a, b], [0, 1], {...clamp, easing: ease});
const outBack = Easing.out(Easing.back(1.7));
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
// RNG semeado por string: mesmo resultado em todo frame
const rnd = (seed: number) => {
  const x = Math.sin(seed * 9301 + 49297) * 233280;
  return x - Math.floor(x);
};

const anchorAt = (f: number) => {
  const a = analise.anch[Math.max(0, Math.min(N - 1, f))];
  return {cx: a[0] * W, cy: a[1] * H, u: a[2] * W, top: a[4] * H};
};

// ─── tempos dos blocos ───
const blockWords = (b: Bloco) => [...b.lines.flatMap((l) => l.words), ...b.keys.map((k) => k.i)];
const TIMES = BLOCOS.map((b) => {
  const ws = blockWords(b);
  const first = Math.min(...ws.map((i) => WORDS[i].a));
  const last = Math.max(...ws.map((i) => WORDS[i].b));
  return {start: fr(first) - 2, lastEnd: fr(last)};
});
const blockEnd = (k: number) => (k + 1 < BLOCOS.length ? TIMES[k + 1].start : N);

// ─── palavra comum ───
const WordSpan: React.FC<{i: number; f: number; accent?: boolean}> = ({i, f, accent}) => {
  const s = fr(WORDS[i].a);
  const p = prog(f, s, s + 4);
  const sc = interpolate(f, [s, s + 5], [0.55, 1], {...clamp, easing: outBack});
  return (
    <span
      style={{
        display: 'inline-block',
        marginRight: '0.24em',
        opacity: p,
        transform: `translateY(${(1 - p) * 14}px) scale(${sc})`,
        filter: `blur(${(1 - p) * 8}px)`,
        color: accent ? ACCENT : '#fff',
        fontFamily: accent ? rubik.fontFamily : undefined,
        fontWeight: accent ? 900 : undefined,
      }}
    >
      {WORDS[i].w}
    </span>
  );
};

const LineEl: React.FC<{l: Line; f: number; hx: number; hy: number; u: number; rank: number}> = ({l, f, hx, hy, u, rank}) => {
  const x = (l.x ?? 0.8) * u;
  const fam = l.italic ? interItalic.fontFamily : inter.fontFamily;
  let fs = (l.size ?? 0.48) * u;
  const full = l.words.map((i) => WORDS[i].w).join(' ');
  const lw = (z: number) => textW(full + ' ', fam, z, 700, l.italic);
  // espaço disponível do lado escolhido
  const room = l.side === 'L' ? hx - x - M : l.side === 'R' ? W - M - (hx + x) : W - 2 * M;
  // reduz até caber no próprio lado (sem invadir o outro lado nem o rosto)
  if (lw(fs) > room) fs = Math.max(fs * 0.42, room / (lw(fs) / fs));
  const w = lw(fs);
  let left = l.side === 'L' ? hx - x - w : l.side === 'R' ? hx + x : hx - w / 2;
  left = Math.max(M, Math.min(W - M - w, left));
  const tx = '0%';
  return (
    <div
      style={{
        position: 'absolute',
        left,
        // no close, as linhas de cima batem no teto: empilha pela ordem em vez de sobrepor
        top: Math.max(TOP + fs / 2 + rank * 0.62 * u, Math.min(BOTTOM - fs / 2, hy + l.y * u)),
        width: w + 2,
        transform: `translate(${tx}, -50%) rotate(${l.rot ?? 0}deg)`,
        transformOrigin: l.side === 'L' ? '100% 50%' : '0% 50%',
        whiteSpace: 'nowrap',
        fontFamily: l.italic ? interItalic.fontFamily : inter.fontFamily,
        fontStyle: l.italic ? 'italic' : 'normal',
        fontWeight: 700,
        fontSize: fs,
        letterSpacing: '-0.015em',
        textShadow: '0 2px 14px rgba(0,0,0,.55)',
        lineHeight: 1,
      }}
    >
      {l.words.map((i) => (
        <WordSpan key={i} i={i} f={f} accent={l.accent} />
      ))}
    </div>
  );
};

// ─── palavra-chave ───
const KeyEl: React.FC<{k: Key; f: number; hx: number; hy: number; u: number; uid: string}> = ({k, f, hx, hy, u, uid}) => {
  const s = fr(WORDS[k.i].a);
  const e = fr(WORDS[k.i].b);
  const text = k.text ?? WORDS[k.i].w.toUpperCase().replace(/[.,!?]/g, '');
  if (f < s - 1) return null;
  let size = k.size * u;
  let bigW = 0;
  const maxW = W - 2 * M;
  if (k.type === 'big') {
    const rotK = Math.cos(((k.rot ?? 0) * Math.PI) / 180);
    const w1 = textW(text, rubik.fontFamily, size, 900) * 0.98;
    if (w1 / rotK > maxW) size = (size * maxW * rotK) / w1;
    bigW = (w1 * size) / (k.size * u);
  } else if (k.type === 'scatter') {
    size = Math.min(size, maxW / (Math.max(1, text.length - 1) * 0.66 + 0.8));
  } else if (k.type === 'type') {
    const w1 = textW(text, rubik.fontFamily, size, 900);
    if (w1 > maxW) size = (size * maxW) / w1;
  }
  const base: React.CSSProperties = {fontFamily: rubik.fontFamily, fontWeight: 900, fontSize: size, lineHeight: 0.9, color: ACCENT, whiteSpace: 'nowrap', letterSpacing: '-0.02em'};

  if (k.type === 'big') {
    const q = prog(f, s, s + 6);
    const sy = interpolate(f, [s, s + 7], [0.5, 1], {...clamp, easing: outBack});
    const sx = lerp(1.7, 1, q);
    const shake = k.shake && f > s + 4 && f < s + 12 ? (rnd(f) - 0.5) * 14 * (1 - (f - s - 4) / 8) : 0;
    const split = k.rgb ? 14 * (1 - prog(f, s, s + 10)) + (f > s + 10 ? 0 : 0) : 0;
    const style: React.CSSProperties = {
      ...base,
      position: 'absolute',
      left: Math.max(M + bigW / 2, Math.min(W - M - bigW / 2, hx + (k.x ?? 0) * u)) + shake,
      top: Math.max(TOP + size * 0.45, hy + (k.y ?? 0) * u) + shake * 0.6,
      transform: `translate(-50%, -50%) rotate(${k.rot ?? 0}deg) scale(${sx}, ${sy})`,
      opacity: q,
      filter: `blur(${(1 - q) * 16}px)`,
    };
    return (
      <>
        {split > 0.3 && (
          <>
            <div style={{...style, color: '#ff1f3d', mixBlendMode: 'screen', left: (style.left as number) - split, opacity: 0.85}}>{text}</div>
            <div style={{...style, color: '#20d4ff', mixBlendMode: 'screen', left: (style.left as number) + split, opacity: 0.85}}>{text}</div>
          </>
        )}
        <div style={style}>{text}</div>
      </>
    );
  }

  if (k.type === 'scatter') {
    const letters = text.split('');
    const spacing = size * 0.66;
    const w0 = (letters.length - 1) * spacing;
    return (
      <>
        {letters.map((ch, j) => {
          const d = s + j * 1.6;
          const p = interpolate(f, [d, d + 9], [0, 1], {...clamp, easing: Easing.bounce});
          const vis = prog(f, d, d + 2);
          const r0 = (rnd(k.i * 31 + j) - 0.5) * 70;
          const r1 = (rnd(k.i * 17 + j) - 0.5) * 16;
          const dy = (rnd(k.i * 7 + j) - 0.5) * 0.35 * u;
          return (
            <div
              key={j}
              style={{
                ...base,
                position: 'absolute',
                left: Math.max(M + w0 / 2 + size * 0.35, Math.min(W - M - w0 / 2 - size * 0.35, hx + (k.x ?? 0) * u)) - w0 / 2 + j * spacing,
                top: Math.max(TOP + size * 0.45, Math.min(BOTTOM - size * 0.5, hy + (k.y ?? 0) * u)) + dy - (1 - p) * 1.4 * u,
                transform: `translate(-50%, -50%) rotate(${lerp(r0, r1, p)}deg)`,
                opacity: vis,
              }}
            >
              {ch}
            </div>
          );
        })}
      </>
    );
  }

  if (k.type === 'type') {
    const n = Math.floor(interpolate(f, [s, Math.max(s + 4, e)], [0, text.length], clamp));
    const caret = f <= e + 6 && Math.floor(f / 4) % 2 === 0;
    return (
      <div style={{...base, fontSize: size, position: 'absolute', left: Math.max(M + textW(text, rubik.fontFamily, size, 900) / 2, Math.min(W - M - textW(text, rubik.fontFamily, size, 900) / 2, hx + (k.x ?? 0) * u)), top: hy + (k.y ?? 0) * u, transform: 'translate(-50%, -50%)'}}>
        <span>{text.slice(0, n)}</span>
        <span style={{opacity: 0}}>{text.slice(n)}</span>
        <span style={{position: 'absolute', marginLeft: -text.slice(n).length * size * 0.66, opacity: caret ? 1 : 0, color: '#fff'}}>|</span>
      </div>
    );
  }

  // arc: texto em curva em volta da cabeça
  let r = k.arc!.r * u;
  const maxR = Math.min(hx, W - hx) - M - size * 0.45;
  r = Math.min(r, Math.max(maxR, 1.1 * u));
  const arcLen = Math.PI * r * 0.86;
  const tw = textW(text, rubik.fontFamily, size, 900) * 1.04;
  if (tw > arcLen) size = (size * arcLen) / tw;
  const cy = hy - 0.05 * u;
  const top = k.arc!.side === 'top';
  const d = top ? `M ${hx - r} ${cy} A ${r} ${r} 0 0 1 ${hx + r} ${cy}` : `M ${hx - r} ${cy} A ${r} ${r} 0 0 0 ${hx + r} ${cy}`;
  const id = `arc-${uid}`;
  const letters = text.split('');
  const grow = interpolate(f, [s, s + 7], [0.6, 1], {...clamp, easing: outBack});
  return (
    <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', transform: `scale(${grow})`, transformOrigin: `${hx}px ${cy}px`}}>
      <defs>
        <path id={id} d={d} />
      </defs>
      <text fontFamily={rubik.fontFamily} fontWeight={900} fontSize={size} fill={ACCENT} letterSpacing={size * 0.02}>
        <textPath href={`#${id}`} startOffset="50%" textAnchor="middle" dominantBaseline={top ? 'auto' : 'hanging'}>
          {letters.map((ch, j) => (
            <tspan key={j} fillOpacity={prog(f, s + j * 0.9, s + j * 0.9 + 3)}>
              {ch}
            </tspan>
          ))}
        </textPath>
      </text>
    </svg>
  );
};

// ─── um bloco (frase) preso ao rosto ───
const BlocoEl: React.FC<{k: number; f: number; layer: 'behind' | 'front'}> = ({k, f, layer}) => {
  const b = BLOCOS[k];
  const {start} = TIMES[k];
  const end = blockEnd(k);
  if (f < start || f >= end) return null;
  const a0 = anchorAt(f);
  const out = prog(f, end - 4, end, Easing.in(Easing.cubic));
  const keys = b.keys.filter((x) => x.layer === layer);
  const lines = layer === 'front' ? b.lines : [];
  if (!keys.length && !lines.length) return null;
  return (
    <AbsoluteFill
      style={{
        transform: `scale(${lerp(1, 0.92, out)})`,
        transformOrigin: `${a0.cx}px ${a0.cy}px`,
        opacity: 1 - out,
        filter: out > 0 ? `blur(${out * 10}px)` : undefined,
      }}
    >
      {keys.map((x, j) => (
        <KeyEl key={j} k={x} f={f} hx={a0.cx} hy={a0.cy} u={a0.u} uid={`${k}-${j}`} />
      ))}
      {lines.map((l, j) => (
        <LineEl key={j} l={l} f={f} hx={a0.cx} hy={a0.cy} u={a0.u} rank={l.y < 0 ? lines.filter((o) => o.side === l.side && o.y < l.y).length : 0} />
      ))}
    </AbsoluteFill>
  );
};

// ─── micro-legenda digitando ───
const Micro: React.FC<{f: number}> = ({f}) => {
  const k = TIMES.findIndex((t, j) => f >= t.start && f < blockEnd(j));
  if (k < 0) return null;
  const ws = blockWords(BLOCOS[k]).sort((x, y) => x - y);
  const full = ws.map((i) => WORDS[i].w).join(' ');
  const t0 = TIMES[k].start + 2;
  const n = Math.floor(interpolate(f, [t0, TIMES[k].lastEnd], [0, full.length], clamp));
  return (
    <div style={{position: 'absolute', left: 64, bottom: 92, fontFamily: inter.fontFamily, fontWeight: 600, fontSize: 24, color: 'rgba(255,255,255,.78)', textShadow: '0 1px 6px rgba(0,0,0,.6)', maxWidth: 760}}>
      {full.slice(0, n)}
    </div>
  );
};

const pad = (i: number) => String(i).padStart(5, '0');

export const Legenda: React.FC = () => {
  const f = useCurrentFrame();
  const mk = staticFile(`mk/${pad(Math.min(f, N - 1))}.png`);
  // punch de câmera nas palavras-chave dos blocos marcados
  let punch = 0;
  BLOCOS.forEach((b, k) => {
    if (!b.punch || !b.keys.length) return;
    const s = fr(WORDS[b.keys[b.keys.length - 1].i].a);
    punch = Math.max(punch, prog(f, s, s + 3) * (1 - prog(f, s + 6, s + 18, Easing.inOut(Easing.cubic))));
  });
  const a = anchorAt(f);
  const video = <OffthreadVideo src={staticFile('video.mp4')} style={{width: W, height: H, position: 'absolute'}} />;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <AbsoluteFill style={{transform: `scale(${1 + 0.04 * punch})`, transformOrigin: `${a.cx}px ${a.cy}px`}}>
        {video}
        {/* atrás da pessoa */}
        {BLOCOS.map((_, k) => (
          <BlocoEl key={`b${k}`} k={k} f={f} layer="behind" />
        ))}
        {/* a pessoa recortada por cima */}
        <AbsoluteFill style={{WebkitMaskImage: `url(${mk})`, maskImage: `url(${mk})`, WebkitMaskSize: '100% 100%', maskSize: '100% 100%'}}>
          <OffthreadVideo src={staticFile('video.mp4')} muted style={{width: W, height: H, position: 'absolute'}} />
        </AbsoluteFill>
        {/* na frente */}
        {BLOCOS.map((_, k) => (
          <BlocoEl key={`f${k}`} k={k} f={f} layer="front" />
        ))}
      </AbsoluteFill>
      <Micro f={f} />
      {/* garante que a máscara deste frame carregou antes do screenshot */}
      <Img src={mk} style={{position: 'absolute', width: 1, height: 1, opacity: 0}} />
    </AbsoluteFill>
  );
};

export const DURATION = N;
