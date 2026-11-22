import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, rng, useUnit} from './tokens';

// Grão de filme bem leve (o vídeo de referência nunca é "chapado")
export const Grain: React.FC<{opacity?: number}> = ({opacity = 0.05}) => (
  <AbsoluteFill style={{opacity, mixBlendMode: 'multiply', pointerEvents: 'none'}}>
    <svg width="100%" height="100%">
      <filter id="cs-grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch" />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="100%" height="100%" filter="url(#cs-grain)" />
    </svg>
  </AbsoluteFill>
);

// 1) Fundo padrão: off-white com névoas pastel (lavanda / azul / pêssego) derivando devagar
export const PastelHaze: React.FC<{seed?: number}> = ({seed = 1}) => {
  const f = useCurrentFrame();
  const {width, height} = useUnit();
  const blobs = [
    {c: C.hazeLav, x: 0.82, y: 0.85, r: 0.75, s: 0.7},
    {c: C.hazeBlue, x: 0.12, y: 0.95, r: 0.7, s: 0.9},
    {c: C.hazePeach, x: 0.05, y: 0.15, r: 0.55, s: 1.1},
    {c: C.hazeBlue, x: 0.9, y: 0.1, r: 0.5, s: 0.8},
  ];
  const D = Math.max(width, height);
  return (
    <AbsoluteFill style={{background: C.bg, overflow: 'hidden'}}>
      {blobs.map((b, i) => {
        const t = f / 30;
        const dx = Math.sin(t * 0.35 * b.s + i * 1.7 + seed) * 0.05;
        const dy = Math.cos(t * 0.3 * b.s + i * 2.3 + seed) * 0.05;
        const R = b.r * D;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: (b.x + dx) * width - R / 2,
              top: (b.y + dy) * height - R / 2,
              width: R,
              height: R,
              borderRadius: '50%',
              background: `radial-gradient(circle, ${b.c} 0%, ${b.c}cc 30%, ${b.c}00 70%)`,
            }}
          />
        );
      })}
      <Grain opacity={0.04} />
    </AbsoluteFill>
  );
};

// 2) Palco de céu: azul saturado + nuvens volumosas nas laterais/base (objeto herói flutua no meio)
export const SkyClouds: React.FC<{seed?: number; drift?: number}> = ({seed = 7, drift = 1}) => {
  const f = useCurrentFrame();
  const {width, height, u} = useUnit();
  const r = rng(seed);
  // cachos de nuvem: esquerda, direita e base
  const clusters = [
    {x: 0.02, y: 0.55, w: 0.42},
    {x: 0.98, y: 0.4, w: 0.45},
    {x: 0.5, y: 1.05, w: 0.9},
    {x: 0.15, y: 1.0, w: 0.5},
    {x: 0.88, y: 1.0, w: 0.5},
  ];
  const puffs = clusters.flatMap((c, ci) =>
    Array.from({length: 26}, () => {
      const k = r();
      return {
        ci,
        x: c.x + (r() - 0.5) * c.w,
        y: c.y + (r() - 0.65) * c.w * 0.5 * (width / height) * (0.6 + k * 0.6),
        s: (0.06 + r() * 0.13) * Math.max(width, height),
        sq: 0.7 + r() * 0.25, // achatamento (nuvem é mais larga que alta)
      };
    }),
  );
  return (
    <AbsoluteFill
      style={{background: `linear-gradient(180deg, ${C.sky1} 0%, #2B8BE0 45%, ${C.sky2} 80%, #A8D8FA 100%)`, overflow: 'hidden'}}
    >
      <div style={{position: 'absolute', inset: 0, filter: `blur(${7 * u}px)`}}>
        {puffs.map((p, i) => {
          const dx = Math.sin(f / 90 + i) * 6 * u * drift + (p.ci === 0 ? -1 : p.ci === 1 ? 1 : 0) * f * 0.15 * u * drift;
          const w = p.s * 1.35;
          const h = p.s * p.sq;
          return (
            <div key={i} style={{position: 'absolute', left: p.x * width - w / 2 + dx, top: p.y * height - h / 2}}>
              {/* sombra azulada embaixo = volume */}
              <div
                style={{
                  position: 'absolute',
                  left: w * 0.04,
                  top: h * 0.22,
                  width: w,
                  height: h,
                  borderRadius: '50%',
                  background: 'radial-gradient(ellipse at 50% 55%, rgba(110,140,185,.42) 0%, rgba(110,140,185,.18) 40%, rgba(110,140,185,0) 68%)',
                }}
              />
              <div
                style={{
                  position: 'absolute',
                  width: w,
                  height: h,
                  borderRadius: '50%',
                  background:
                    'radial-gradient(ellipse at 46% 36%, #ffffff 0%, rgba(250,252,255,.96) 22%, rgba(238,245,252,.7) 42%, rgba(230,240,250,.25) 58%, rgba(230,240,250,0) 70%)',
                }}
              />
            </div>
          );
        })}
      </div>
      <Grain opacity={0.035} />
    </AbsoluteFill>
  );
};

// 3) Cena escura de virada: quase preto + arco de "planeta" com brilho azul e linha fina clara
export const NightArc: React.FC<{rise?: number}> = ({rise = 0}) => {
  const {width, height, u} = useUnit();
  const R = Math.max(width, height) * 1.6;
  const top = height * 0.72 - rise * height * 0.08;
  return (
    <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 30%, #0a1030 0%, ${C.night} 60%)`, overflow: 'hidden'}}>
      <div
        style={{
          position: 'absolute',
          left: width / 2 - R / 2,
          top,
          width: R,
          height: R,
          borderRadius: '50%',
          background: '#02040b',
          border: `${2 * u}px solid ${C.rim}`,
          boxShadow: `0 ${-14 * u}px ${90 * u}px ${26 * u}px rgba(47,85,232,.75), inset 0 ${40 * u}px ${110 * u}px rgba(47,85,232,.7)`,
        }}
      />
      <Grain opacity={0.06} />
    </AbsoluteFill>
  );
};
