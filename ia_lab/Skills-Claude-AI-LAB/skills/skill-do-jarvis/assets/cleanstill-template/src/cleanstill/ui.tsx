import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {C, FONT_BODY, FONT_HEAD, easeInOut, lerp, outBack, prog, rng, useUnit} from './tokens';

// Câmera "still" viva: push lento constante + leve deriva (a cena NUNCA fica parada)
export const Drift: React.FC<{dur: number; from?: number; to?: number; pan?: number; children: React.ReactNode}> = ({
  dur,
  from = 1,
  to = 1.06,
  pan = 0,
  children,
}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const p = prog(f, 0, dur, easeInOut);
  return (
    <div style={{position: 'absolute', inset: 0, transform: `scale(${lerp(from, to, p)}) translateX(${lerp(0, pan, p) * u}px)`}}>
      {children}
    </div>
  );
};

// Entrada padrão de qualquer elemento: blur 14→0 + escala .94→1 + y
export const Rise: React.FC<{at: number; dur?: number; y?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({
  at,
  dur = 16,
  y = 24,
  children,
  style,
}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const p = prog(f, at, at + dur);
  return (
    <div style={{opacity: p, filter: `blur(${lerp(14, 0, p) * u}px)`, transform: `translateY(${lerp(y, 0, p) * u}px) scale(${lerp(0.94, 1, p)})`, ...style}}>
      {children}
    </div>
  );
};

// Pill de vidro (legendas laterais "I dropped it" / "into Claude Code")
export const GlassPill: React.FC<{text: string; at: number; from?: 'left' | 'right'; size?: number; style?: React.CSSProperties}> = ({
  text,
  at,
  from = 'left',
  size = 46,
  style,
}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const p = prog(f, at, at + 16);
  const dx = (from === 'left' ? -50 : 50) * (1 - p);
  return (
    <div
      style={{
        position: 'absolute',
        padding: `${size * 0.32 * u}px ${size * 0.62 * u}px`,
        borderRadius: 999,
        background: 'linear-gradient(180deg, rgba(120,165,225,.42), rgba(70,120,200,.30))',
        backdropFilter: `blur(${14 * u}px)`,
        WebkitBackdropFilter: `blur(${14 * u}px)`,
        border: `${1.5 * u}px solid rgba(255,255,255,.55)`,
        boxShadow: `0 ${10 * u}px ${30 * u}px rgba(20,60,120,.18)`,
        color: '#fff',
        fontFamily: FONT_HEAD,
        fontWeight: 600,
        fontSize: size * u,
        letterSpacing: '-0.015em',
        textShadow: `0 ${1 * u}px ${6 * u}px rgba(20,50,110,.35)`,
        whiteSpace: 'nowrap',
        opacity: p,
        filter: `blur(${lerp(10, 0, p) * u}px)`,
        transform: `translateX(${dx * u}px)`,
        ...style,
      }}
    >
      {text}
    </div>
  );
};

// Pill de preço/selo azul ("$12,000") que dá "pop"
export const PricePill: React.FC<{text: string; at: number; size?: number; style?: React.CSSProperties}> = ({text, at, size = 30, style}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const p = prog(f, at, at + 14, outBack);
  return (
    <div
      style={{
        position: 'absolute',
        padding: `${size * 0.3 * u}px ${size * 0.6 * u}px`,
        borderRadius: 999,
        background: `linear-gradient(180deg, #5A86F5, ${C.pill})`,
        color: '#fff',
        fontFamily: FONT_HEAD,
        fontWeight: 700,
        fontSize: size * u,
        boxShadow: `0 ${6 * u}px ${18 * u}px rgba(59,111,240,.4), inset 0 ${1 * u}px 0 rgba(255,255,255,.35)`,
        transform: `scale(${Math.max(0, p)})`,
        opacity: Math.min(1, p * 2),
        whiteSpace: 'nowrap',
        ...style,
      }}
    >
      {text}
    </div>
  );
};

// Cursor de seta (macOS) que anda por pontos-chave [frame, x, y]; clica (encolhe) em `clicks`
export const Cursor: React.FC<{path: [number, number, number][]; clicks?: number[]; size?: number}> = ({path, clicks = [], size = 34}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  let x = path[0][1];
  let y = path[0][2];
  for (let i = 1; i < path.length; i++) {
    const [fa, xa, ya] = path[i - 1];
    const [fb, xb, yb] = path[i];
    const t = prog(f, fa, fb, easeInOut);
    if (f >= fa) {
      x = lerp(xa, xb, t);
      y = lerp(ya, yb, t);
    }
  }
  const click = clicks.reduce((acc, c) => acc + Math.sin(Math.PI * prog(f, c, c + 8)), 0);
  const o = prog(f, path[0][0], path[0][0] + 8);
  return (
    <svg
      width={size * u}
      height={size * 1.3 * u}
      viewBox="0 0 20 26"
      style={{position: 'absolute', left: x * u, top: y * u, opacity: o, transform: `scale(${1 - click * 0.18})`, transformOrigin: 'top left', filter: `drop-shadow(0 ${2 * u}px ${3 * u}px rgba(0,0,0,.3))`}}
    >
      <path d="M1 1 L1 20 L6 15.5 L9.5 23.5 L13 22 L9.6 14.2 L16 14.2 Z" fill="#111" stroke="#fff" strokeWidth="1.6" strokeLinejoin="round" />
    </svg>
  );
};

// Ícone "asterisco" de raios (marca genérica de IA/estrela). Cor quente, 1 por cena.
export const Spark: React.FC<{size: number; color?: string; rot?: number; style?: React.CSSProperties}> = ({size, color = C.warm, rot = 0, style}) => (
  <svg width={size} height={size} viewBox="-50 -50 100 100" style={{transform: `rotate(${rot}deg)`, ...style}}>
    {Array.from({length: 12}, (_, i) => (
      <line key={i} x1="0" y1="-12" x2="0" y2="-46" stroke={color} strokeWidth="7" strokeLinecap="round" transform={`rotate(${i * 30 + (i % 2) * 6})`} />
    ))}
  </svg>
);

// Cartão-papel do "arquivo" com moldura de seleção (estilo Figma: caixa azul + 8 alças + etiqueta)
export const PaperCard: React.FC<{
  at: number;
  title: string;
  sub: string;
  meta: string[];
  w?: number;
  select?: number; // frame em que a caixa de seleção aparece
  tag?: string;
}> = ({at, title, sub, meta, w = 520, select, tag}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const p = prog(f, at, at + 20);
  const sp = select !== undefined ? prog(f, select, select + 10) : 0;
  const h = w * 1.25;
  const float = Math.sin(f / 28) * 6;
  const handles = [
    [0, 0], [0.5, 0], [1, 0], [0, 0.5], [1, 0.5], [0, 1], [0.5, 1], [1, 1],
  ];
  return (
    <div
      style={{
        position: 'relative',
        width: w * u,
        height: h * u,
        opacity: p,
        filter: `blur(${lerp(14, 0, p) * u}px)`,
        transform: `perspective(${1600 * u}px) translateY(${(lerp(40, 0, p) + float) * u}px) rotateY(${-10 + Math.sin(f / 40) * 2}deg) rotateX(4deg) rotateZ(-2deg)`,
      }}
    >
      <div
        style={{
          position: 'absolute',
          inset: 0,
          borderRadius: 18 * u,
          background: 'linear-gradient(160deg, #ffffff 0%, #f1f2f6 100%)',
          boxShadow: `0 ${30 * u}px ${70 * u}px rgba(40,60,110,.22), 0 ${2 * u}px ${6 * u}px rgba(0,0,0,.06)`,
          padding: 44 * u,
          boxSizing: 'border-box',
          fontFamily: FONT_HEAD,
        }}
      >
        <Spark size={46 * u} />
        <div style={{fontWeight: 800, fontSize: 64 * u, color: C.ink, letterSpacing: '-0.03em', marginTop: 14 * u}}>{title}</div>
        <div style={{fontFamily: 'monospace', fontSize: 20 * u, color: '#d0705a', marginTop: 6 * u}}>{sub}</div>
        <div style={{height: 1.5 * u, background: '#dcdfe8', margin: `${22 * u}px 0`}} />
        {meta.map((m, i) => (
          <div key={i} style={{fontFamily: 'monospace', fontSize: 19 * u, color: '#555a6a', lineHeight: 1.7}}>
            {m}
          </div>
        ))}
        <div style={{marginTop: 30 * u}}>
          {[0.92, 0.78, 0.86, 0.64, 0.8, 0.5].map((l, i) => (
            <div key={i} style={{height: 14 * u, width: `${l * 100}%`, background: '#dfe2ea', borderRadius: 6 * u, marginBottom: 14 * u}} />
          ))}
        </div>
      </div>
      {select !== undefined && (
        <div style={{position: 'absolute', inset: -14 * u, border: `${2 * u}px solid ${C.pill}`, opacity: sp, transform: `scale(${lerp(1.04, 1, sp)})`}}>
          {handles.map(([hx, hy], i) => (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: `calc(${hx * 100}% - ${6 * u}px)`,
                top: `calc(${hy * 100}% - ${6 * u}px)`,
                width: 12 * u,
                height: 12 * u,
                background: '#fff',
                border: `${2 * u}px solid ${C.pill}`,
                boxSizing: 'border-box',
              }}
            />
          ))}
          {tag && (
            <div
              style={{
                position: 'absolute',
                left: -2 * u,
                top: -40 * u,
                background: C.pill,
                color: '#fff',
                fontFamily: 'monospace',
                fontSize: 19 * u,
                padding: `${4 * u}px ${10 * u}px`,
                borderRadius: 4 * u,
              }}
            >
              {tag}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// Notebook flutuante (o objeto herói no céu). `screen` = conteúdo da tela.
export const Laptop: React.FC<{w?: number; screen: React.ReactNode; tilt?: number}> = ({w = 900, screen, tilt = 6}) => {
  const {u} = useUnit();
  const sw = w * u;
  const sh = sw * 0.62;
  return (
    <div style={{position: 'relative', width: sw, height: sh * 1.12, transform: `perspective(${2200 * u}px) rotateX(${tilt}deg)`}}>
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: 0,
          width: sw,
          height: sh,
          borderRadius: 22 * u,
          background: 'linear-gradient(180deg,#2a2d33,#15171b)',
          padding: 14 * u,
          boxSizing: 'border-box',
          boxShadow: `inset 0 0 0 ${2 * u}px #9aa0aa, 0 ${30 * u}px ${80 * u}px rgba(10,40,90,.35)`,
        }}
      >
        <div style={{position: 'relative', width: '100%', height: '100%', borderRadius: 10 * u, overflow: 'hidden', background: '#f6f6f8'}}>
          {screen}
          <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(120deg, rgba(255,255,255,.25) 0%, rgba(255,255,255,0) 35%)'}} />
        </div>
      </div>
      <div
        style={{
          position: 'absolute',
          left: -sw * 0.09,
          top: sh - 2 * u,
          width: sw * 1.18,
          height: sh * 0.1,
          background: 'linear-gradient(180deg,#c3c7ce 0%,#8b9099 55%,#5d626b 100%)',
          clipPath: 'polygon(7% 0, 93% 0, 100% 70%, 99% 100%, 1% 100%, 0 70%)',
          borderRadius: `0 0 ${16 * u}px ${16 * u}px`,
        }}
      />
    </div>
  );
};

// Miniatura de "site" gerada por código (para carrossel e parede de grid). Nada de marca de terceiros.
const PALETTES = [
  ['#0b0b0f', '#ff5a36', '#f4f1ea'],
  ['#f5f1e8', '#2f4a3a', '#c9d6c3'],
  ['#101321', '#7b5cff', '#f1f0ff'],
  ['#ff4d2e', '#111', '#fff'],
  ['#0d0d0d', '#e9e9e9', '#ff9f43'],
  ['#e9eef7', '#1d3a8a', '#ffffff'],
];
export const SiteThumb: React.FC<{seed: number; w: number; h: number; radius?: number}> = ({seed, w, h, radius}) => {
  const {u} = useUnit();
  const r = rng(seed * 97 + 13);
  const [bg, acc, fg] = PALETTES[seed % PALETTES.length];
  const big = 0.1 + r() * 0.05;
  return (
    <div
      style={{
        position: 'relative',
        width: w,
        height: h,
        borderRadius: radius ?? 14 * u,
        overflow: 'hidden',
        background: `radial-gradient(ellipse at ${30 + r() * 50}% ${40 + r() * 40}%, ${acc}cc 0%, ${bg} 60%)`,
        boxShadow: `0 ${18 * u}px ${44 * u}px rgba(30,40,80,.25)`,
      }}
    >
      <div style={{position: 'absolute', left: '6%', top: '6%', right: '6%', display: 'flex', justifyContent: 'space-between'}}>
        <div style={{width: '18%', height: h * 0.035, background: fg, opacity: 0.85, borderRadius: 3}} />
        <div style={{display: 'flex', gap: w * 0.025}}>
          {[0, 1, 2, 3].map((i) => (
            <div key={i} style={{width: w * 0.06, height: h * 0.025, background: fg, opacity: 0.5, borderRadius: 3}} />
          ))}
        </div>
      </div>
      <div style={{position: 'absolute', left: '7%', top: '32%', width: '58%'}}>
        <div style={{height: h * big, background: fg, borderRadius: 4, marginBottom: h * 0.03}} />
        <div style={{height: h * big, width: '72%', background: fg, borderRadius: 4, marginBottom: h * 0.05}} />
        <div style={{height: h * 0.025, width: '80%', background: fg, opacity: 0.45, borderRadius: 3, marginBottom: h * 0.02}} />
        <div style={{height: h * 0.025, width: '60%', background: fg, opacity: 0.45, borderRadius: 3, marginBottom: h * 0.06}} />
        <div style={{height: h * 0.07, width: '30%', background: acc, borderRadius: 99}} />
      </div>
      <div
        style={{
          position: 'absolute',
          right: '-8%',
          bottom: '-10%',
          width: '50%',
          height: '75%',
          borderRadius: '50%',
          background: `radial-gradient(circle, ${acc} 0%, ${acc}00 70%)`,
          opacity: 0.7,
        }}
      />
    </div>
  );
};

// Cartão de vidro central com colchetes e texto trocando como slot (Portfolios → Stores → Landing pages)
export const SlotCard: React.FC<{items: string[]; steps: number[]; at: number; size?: number}> = ({items, steps, at, size = 52}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const p = prog(f, at, at + 14);
  const idx = steps.reduce((acc, s) => acc + prog(f, s, s + 10, easeInOut), 0);
  const W = size * 8.2 * u;
  const H = size * 3.6 * u;
  const br = size * 0.35 * u;
  const bracket = (side: 'l' | 'r'): React.CSSProperties => ({
    position: 'absolute',
    top: '50%',
    [side === 'l' ? 'left' : 'right']: W * 0.17,
    width: br * 0.5,
    height: size * 0.95 * u,
    transform: 'translateY(-50%)',
    borderTop: `${2 * u}px solid ${C.blue}`,
    borderBottom: `${2 * u}px solid ${C.blue}`,
    [side === 'l' ? 'borderLeft' : 'borderRight']: `${2 * u}px solid ${C.blue}`,
    opacity: 0.8,
  });
  return (
    <div
      style={{
        position: 'relative',
        width: W,
        height: H,
        borderRadius: 30 * u,
        background: 'rgba(255,255,255,.58)',
        backdropFilter: `blur(${22 * u}px)`,
        WebkitBackdropFilter: `blur(${22 * u}px)`,
        border: `${1.5 * u}px solid rgba(255,255,255,.8)`,
        boxShadow: `0 ${30 * u}px ${80 * u}px rgba(30,40,80,.25)`,
        overflow: 'hidden',
        opacity: p,
        transform: `scale(${lerp(0.9, 1, p)})`,
      }}
    >
      <div style={bracket('l')} />
      <div style={bracket('r')} />
      {items.map((t, i) => {
        const d = i - idx;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: 0,
              right: 0,
              top: H / 2 + d * size * 1.25 * u - size * 0.62 * u,
              textAlign: 'center',
              fontFamily: FONT_HEAD,
              fontWeight: 600,
              fontSize: size * u,
              color: C.ink,
              letterSpacing: '-0.02em',
              opacity: interpolate(Math.abs(d), [0, 1, 1.6], [1, 0.18, 0], {extrapolateRight: 'clamp'}),
              filter: `blur(${interpolate(Math.abs(d), [0, 1], [0, 3], {extrapolateRight: 'clamp'}) * u}px)`,
            }}
          >
            {t}
          </div>
        );
      })}
    </div>
  );
};

// Lupa que passa por cima do cartão e revela outro conteúdo dentro da lente; depois troca tudo.
export const LensReveal: React.FC<{
  a: React.ReactNode;
  b: React.ReactNode;
  w: number;
  h: number;
  path: [number, number, number][]; // [frame, x, y] em fração do cartão (0..1)
  swapAt: number;
  r?: number;
}> = ({a, b, w, h, path, swapAt, r = 90}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  let x = path[0][1];
  let y = path[0][2];
  for (let i = 1; i < path.length; i++) {
    const [fa, xa, ya] = path[i - 1];
    const [fb, xb, yb] = path[i];
    if (f >= fa) {
      const t = prog(f, fa, fb, easeInOut);
      x = lerp(xa, xb, t);
      y = lerp(ya, yb, t);
    }
  }
  const lensIn = prog(f, path[0][0], path[0][0] + 10);
  const swap = prog(f, swapAt, swapAt + 14);
  const R = r * u;
  const cx = x * w * u;
  const cy = y * h * u;
  const rad = lerp(R * lensIn, Math.hypot(w, h) * u, swap);
  return (
    <div style={{position: 'relative', width: w * u, height: h * u}}>
      <div style={{position: 'absolute', inset: 0}}>{a}</div>
      <div style={{position: 'absolute', inset: 0, clipPath: `circle(${rad}px at ${cx}px ${cy}px)`}}>{b}</div>
      <div
        style={{
          position: 'absolute',
          left: cx - R,
          top: cy - R,
          width: R * 2,
          height: R * 2,
          borderRadius: '50%',
          border: `${7 * u}px solid #3c3f4a`,
          boxSizing: 'border-box',
          background: 'radial-gradient(circle at 35% 30%, rgba(255,255,255,.45) 0%, rgba(255,255,255,0) 45%)',
          boxShadow: `0 ${10 * u}px ${24 * u}px rgba(0,0,0,.18)`,
          opacity: lensIn * (1 - swap),
        }}
      >
        <div
          style={{
            position: 'absolute',
            left: R * 2 * 0.5,
            top: R * 2 * 0.5,
            width: 9 * u,
            height: R * 1.25,
            background: '#3c3f4a',
            borderRadius: 6 * u,
            transformOrigin: 'top center',
            transform: `rotate(40deg) translateY(${R * 0.98}px)`,
          }}
        />
      </div>
    </div>
  );
};

export const Card: React.FC<{w: number; h: number; children: React.ReactNode; bg?: string; label?: string}> = ({w, h, children, bg = '#fbfbfd', label}) => {
  const {u} = useUnit();
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        width: w * u,
        height: h * u,
        borderRadius: 28 * u,
        background: bg,
        boxShadow: `0 ${30 * u}px ${70 * u}px rgba(40,60,110,.16)`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: FONT_HEAD,
      }}
    >
      {label && (
        <div style={{position: 'absolute', left: 30 * u, top: 24 * u, fontFamily: FONT_BODY, fontWeight: 600, fontSize: 24 * u, color: C.blue}}>{label}</div>
      )}
      {children}
    </div>
  );
};
