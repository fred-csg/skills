import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {C, easeIn, easeInOut, easeOut, lerp, outBack, prog, useUnit} from './tokens';
import {Spark} from './ui';

// Transições APROVADAS do cleanstill. (O "dissolve em retícula/halftone" do vídeo de referência
// NÃO entra: mosaico/pixel/blocos é proibido pelo usuário.)

// 1) BLOOM: um sol/brilho branco nasce no centro, cresce e lava a tela de branco; a próxima cena surge
// por baixo enquanto o branco se dissipa. Trocar de cena em at + dur*0.55. dur 14–20 f.
export const Bloom: React.FC<{at: number; dur?: number; x?: number; y?: number; color?: string}> = ({at, dur = 18, x = 0.5, y = 0.42, color = '#ffffff'}) => {
  const f = useCurrentFrame();
  const {width, height} = useUnit();
  if (f < at || f > at + dur) return null;
  const grow = prog(f, at, at + dur * 0.55, easeIn);
  const fade = interpolate(f, [at + dur * 0.55, at + dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: easeOut});
  const D = Math.hypot(width, height) * 2.4;
  const s = lerp(0.05, 1, grow);
  return (
    <AbsoluteFill style={{pointerEvents: 'none', opacity: fade}}>
      <div
        style={{
          position: 'absolute',
          left: x * width - (D * s) / 2,
          top: y * height - (D * s) / 2,
          width: D * s,
          height: D * s,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${color} 0%, ${color} 28%, ${color}cc 40%, ${color}00 68%)`,
        }}
      />
    </AbsoluteFill>
  );
};

// 2) BLOB / PORTAL: forma orgânica (bolha que ondula) cresce do centro revelando a próxima cena,
// com borda ciano luminosa. Envolve a cena NOVA. dur 16–22 f.
const blobPath = (cx: number, cy: number, R: number, t: number) => {
  const N = 72;
  let d = '';
  for (let i = 0; i <= N; i++) {
    const th = (i / N) * Math.PI * 2;
    const r = R * (1 + 0.09 * Math.sin(3 * th + t) + 0.05 * Math.sin(5 * th - 1.3 * t) + 0.03 * Math.sin(7 * th + 2.1 * t));
    const x = cx + Math.cos(th) * r;
    const y = cy + Math.sin(th) * r;
    d += (i === 0 ? 'M' : 'L') + x.toFixed(1) + ' ' + y.toFixed(1) + ' ';
  }
  return d + 'Z';
};
export const BlobReveal: React.FC<{at: number; dur?: number; x?: number; y?: number; children: React.ReactNode}> = ({at, dur = 20, x = 0.5, y = 0.5, children}) => {
  const f = useCurrentFrame();
  const {width, height, u} = useUnit();
  if (f < at) return null;
  const p = prog(f, at, at + dur, easeInOut);
  if (p >= 1) return <AbsoluteFill>{children}</AbsoluteFill>;
  const R = lerp(20 * u, Math.hypot(width, height) * 0.62, p);
  const d = blobPath(x * width, y * height, R, f / 5);
  const rim = 1 - prog(f, at + dur * 0.6, at + dur);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{clipPath: `path('${d}')`}}>{children}</AbsoluteFill>
      <AbsoluteFill style={{pointerEvents: 'none'}}>
        <svg width={width} height={height} style={{overflow: 'visible'}}>
          <defs>
            <filter id="cs-blob-glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation={14 * u} />
            </filter>
          </defs>
          <path d={d} fill="none" stroke={C.cyan} strokeWidth={34 * u} opacity={0.75 * rim} filter="url(#cs-blob-glow)" />
          <path d={d} fill="none" stroke="#e8fbff" strokeWidth={4 * u} opacity={0.9 * rim} />
        </svg>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// 3) BURST: ícone-asterisco gira e cresce no centro, os raios explodem para fora + flash branco.
// Trocar de cena em at + dur*0.6. dur ~24 f.
export const RayBurst: React.FC<{at: number; dur?: number; color?: string}> = ({at, dur = 24, color = C.warm}) => {
  const f = useCurrentFrame();
  const {width, height, u} = useUnit();
  if (f < at || f > at + dur) return null;
  const icon = prog(f, at, at + dur * 0.4, outBack);
  const spin = interpolate(f, [at, at + dur * 0.5], [0, 140], {extrapolateRight: 'clamp', easing: easeIn});
  const rays = prog(f, at + dur * 0.35, at + dur * 0.75, easeIn);
  const flash = interpolate(f, [at + dur * 0.5, at + dur * 0.62, at + dur], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const D = Math.hypot(width, height);
  const iconOut = prog(f, at + dur * 0.45, at + dur * 0.62);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
        <div
          style={{
            width: 360 * u,
            height: 360 * u,
            borderRadius: '42%',
            background: 'rgba(255,255,255,.75)',
            boxShadow: `0 ${20 * u}px ${60 * u}px rgba(40,60,110,.12)`,
            transform: `scale(${icon * (1 - iconOut * 0.6)})`,
            opacity: 1 - iconOut,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Spark size={200 * u} color={color} rot={spin} />
        </div>
      </AbsoluteFill>
      <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
        <defs>
          <filter id="cs-ray-blur">
            <feGaussianBlur stdDeviation={6 * u} />
          </filter>
        </defs>
        {rays > 0 &&
          Array.from({length: 18}, (_, i) => {
            const th = (i / 18) * Math.PI * 2 + spin * (Math.PI / 180);
            const r0 = lerp(80 * u, D * 0.35, rays);
            const r1 = lerp(120 * u, D * 0.9, rays);
            return (
              <line
                key={i}
                x1={width / 2 + Math.cos(th) * r0}
                y1={height / 2 + Math.sin(th) * r0}
                x2={width / 2 + Math.cos(th) * r1}
                y2={height / 2 + Math.sin(th) * r1}
                stroke={i % 2 ? '#ffd9a8' : color}
                strokeWidth={lerp(26, 70, rays) * u}
                strokeLinecap="round"
                opacity={1 - rays * 0.6}
                filter="url(#cs-ray-blur)"
              />
            );
          })}
      </svg>
      <AbsoluteFill style={{background: '#fff', opacity: flash}} />
    </AbsoluteFill>
  );
};

// 4) CROSS-BLUR: dissolve com desfoque (a cena antiga desfoca e some, a nova entra desfocada).
// Use em <CrossBlur at dur out={<Antiga/>} in={<Nova/>} />. dur 10–14 f.
export const CrossBlur: React.FC<{at: number; dur?: number; out: React.ReactNode; in: React.ReactNode}> = ({at, dur = 12, out, in: inn}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const p = prog(f, at, at + dur, easeInOut);
  return (
    <AbsoluteFill>
      {p < 1 && <AbsoluteFill style={{opacity: 1 - p, filter: `blur(${p * 18 * u}px)`, transform: `scale(${lerp(1, 1.04, p)})`}}>{out}</AbsoluteFill>}
      {p > 0 && <AbsoluteFill style={{opacity: p, filter: `blur(${(1 - p) * 18 * u}px)`, transform: `scale(${lerp(0.97, 1, p)})`}}>{inn}</AbsoluteFill>}
    </AbsoluteFill>
  );
};
