import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {easeInOut, lerp, prog, useUnit} from './tokens';
import {PricePill, SiteThumb} from './ui';

// Carrossel 3D em arco (CSS 3D): cartões em profundidade girando devagar; pills de preço opcionais.
export const Carousel3D: React.FC<{
  n?: number;
  at: number;
  cardW?: number;
  radius?: number;
  spread?: number; // graus entre cartões
  speed?: number; // graus por frame
  prices?: (string | null)[];
  y?: number;
}> = ({n = 7, at, cardW = 620, radius = 1500, spread = 24, speed = 0.12, prices = [], y = 0}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const enter = prog(f, at, at + 28);
  const W = cardW * u;
  const H = W * 0.62;
  const R = radius * u;
  return (
    <AbsoluteFill style={{perspective: 1700 * u, perspectiveOrigin: '50% 40%'}}>
      <div style={{position: 'absolute', left: '50%', top: `calc(50% + ${y * u}px)`, transformStyle: 'preserve-3d', transform: `translateZ(${-R * 0.35}px)`}}>
        {Array.from({length: n}, (_, i) => {
          const th = ((i - (n - 1) / 2) * spread + (f - at) * speed - lerp(30, 0, enter)) * (Math.PI / 180);
          const x = Math.sin(th) * R;
          const z = Math.cos(th) * R - R;
          const p = prog(f, at + i * 3, at + i * 3 + 20);
          const price = prices[i];
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: -W / 2,
                top: -H / 2,
                transform: `translate3d(${x}px, ${Math.sin(f / 30 + i) * 6 * u}px, ${z}px) rotateY(${(th * 180) / Math.PI}deg)`,
                opacity: p,
                filter: `blur(${lerp(12, 0, p) * u}px)`,
              }}
            >
              <SiteThumb seed={i + 3} w={W} h={H} radius={18 * u} />
              {price && <PricePill text={price} at={at + 14 + i * 4} style={{right: -14 * u, top: -20 * u}} />}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Parede de miniaturas correndo (linhas em sentidos alternados) com blur de movimento na arrancada
export const ThumbWall: React.FC<{at: number; rows?: number; cols?: number}> = ({at, rows = 5, cols = 9}) => {
  const f = useCurrentFrame();
  const {u, width, height} = useUnit();
  const cw = width / (cols - 2.2);
  const ch = cw * 0.62;
  const burst = 1 - prog(f, at, at + 18, easeInOut); // arranca rápido e assenta
  const t = f - at;
  return (
    <AbsoluteFill style={{background: '#f3f4fb', overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, filter: `blur(${burst * 10 * u}px)`}}>
        {Array.from({length: rows}, (_, r) => {
          const dir = r % 2 ? 1 : -1;
          const off = dir * (t * 1.4 + burst * 260) * u;
          return (
            <div key={r} style={{position: 'absolute', top: (height - rows * (ch + 18 * u)) / 2 + r * (ch + 18 * u), left: -cw + (off % cw), display: 'flex', gap: 18 * u}}>
              {Array.from({length: cols + 2}, (_, c) => (
                <SiteThumb key={c} seed={r * 11 + c * 3} w={cw - 18 * u} h={ch} radius={10 * u} />
              ))}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
