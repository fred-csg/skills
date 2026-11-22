import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {C, FONT_BODY, FONT_HEAD, FONT_SERIF, easeIn, easeInOut, lerp, prog, useUnit} from './tokens';

export type WordStyle = 'ink' | 'key' | 'serif' | 'soft' | 'hl' | 'white';
export type W = {t: string; at: number; s?: WordStyle};

// Uma palavra entrando letra por letra: blur 10→0, y 0.28em→0, opacidade; stagger 1 frame por letra.
// ghost = palavra já visível bem apagada antes de ser "falada" (efeito karaokê do vídeo de referência).
const Word: React.FC<{w: W; ghost?: boolean; size: number; color?: string}> = ({w, ghost, size, color}) => {
  const f = useCurrentFrame();
  const s = w.s ?? 'ink';
  const chars = Array.from(w.t);
  const fam = s === 'serif' ? FONT_SERIF : FONT_HEAD;
  const baseColor =
    color ?? (s === 'soft' ? C.inkSoft : s === 'white' || s === 'hl' ? '#ffffff' : s === 'key' ? C.blue : C.ink);
  // Destaque tipo "texto selecionado": retângulo azul cresce da esquerda
  const hl = s === 'hl' ? prog(f, w.at + 2, w.at + 12) : 0;
  // Brilho que atravessa a palavra-chave depois que ela assenta
  const shStart = w.at + chars.length + 10;
  const sh = s === 'key' ? interpolate(f, [shStart, shStart + 30], [100, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: easeInOut}) : 0;
  const shOn = s === 'key' && f > shStart && f < shStart + 30;
  return (
    <span
      style={{
        position: 'relative',
        display: 'inline-block',
        fontFamily: fam,
        fontStyle: s === 'serif' ? 'italic' : 'normal',
        fontWeight: s === 'serif' ? 400 : 700,
        letterSpacing: s === 'serif' ? '0' : '-0.025em',
        marginRight: '0.24em',
        whiteSpace: 'pre',
      }}
    >
      {s === 'hl' && (
        <span
          style={{
            position: 'absolute',
            left: '-0.12em',
            right: '-0.12em',
            top: '0.04em',
            bottom: '0.0em',
            background: `linear-gradient(180deg, #4C7DF5, ${C.pill})`,
            borderRadius: '0.08em',
            transformOrigin: 'left center',
            transform: `scaleX(${hl})`,
            boxShadow: `0 0 ${size * 0.5}px rgba(59,111,240,${0.55 * hl})`,
          }}
        />
      )}
      {chars.map((ch, i) => {
        const p = prog(f, w.at + i, w.at + i + 14);
        const o = ghost ? lerp(0.18, 1, p) : p;
        const blur = ghost ? lerp(2.5, 0, p) : lerp(10, 0, p);
        const y = ghost ? 0 : lerp(0.28, 0, p);
        const c = s === 'hl' && hl < 0.5 ? C.ink : baseColor;
        return (
          <span
            key={i}
            style={{
              position: 'relative',
              display: 'inline-block',
              opacity: o,
              filter: blur > 0.05 ? `blur(${blur * (size / 100)}px)` : undefined,
              transform: `translateY(${y}em)`,
              color: c,
            }}
          >
            {ch}
          </span>
        );
      })}
      {shOn && (
        <span
          style={{
            position: 'absolute',
            left: 0,
            top: 0,
            color: '#e4ecff',
            pointerEvents: 'none',
            WebkitMaskImage: 'linear-gradient(100deg, transparent 40%, #000 50%, transparent 60%)',
            maskImage: 'linear-gradient(100deg, transparent 40%, #000 50%, transparent 60%)',
            WebkitMaskSize: '300% 100%',
            maskSize: '300% 100%',
            WebkitMaskPosition: `${sh}% 0`,
            maskPosition: `${sh}% 0`,
          }}
        >
          {w.t}
        </span>
      )}
    </span>
  );
};

// Linha de texto cinético. Tamanho em px na unidade 1080.
export const Line: React.FC<{
  words: W[];
  size: number;
  ghost?: boolean;
  align?: 'left' | 'center';
  color?: string;
  glow?: boolean;
  style?: React.CSSProperties;
}> = ({words, size, ghost, align = 'center', color, glow, style}) => {
  const {u} = useUnit();
  return (
    <div
      style={{
        fontSize: size * u,
        lineHeight: 1.08,
        textAlign: align,
        textShadow: glow ? `0 0 ${size * 0.35 * u}px rgba(190,215,255,.65)` : undefined,
        ...style,
      }}
    >
      {words.map((w, i) => (
        <Word key={i} w={w} ghost={ghost} size={size * u} color={color} />
      ))}
    </div>
  );
};

// Kicker cinza pequeno acima do título ("could make", "Just this.")
export const Kicker: React.FC<{text: string; at: number; size?: number; color?: string; align?: 'left' | 'center'}> = ({
  text,
  at,
  size = 40,
  color = C.inkSoft,
  align = 'center',
}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const p = prog(f, at, at + 14);
  return (
    <div
      style={{
        fontFamily: FONT_BODY,
        fontWeight: 500,
        fontSize: size * u,
        color,
        textAlign: align,
        opacity: p,
        filter: `blur(${lerp(6, 0, p) * u}px)`,
        transform: `translateY(${lerp(10, 0, p) * u}px)`,
        letterSpacing: '-0.01em',
      }}
    >
      {text}
    </div>
  );
};

// Saída "zoom-through": o bloco cresce, desfoca e some (passa pela câmera). 8–12 frames, ease in.
export const ZoomExit: React.FC<{at: number; dur?: number; children: React.ReactNode; to?: number}> = ({at, dur = 10, children, to = 1.35}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const p = prog(f, at, at + dur, easeIn);
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        transform: `scale(${lerp(1, to, p)})`,
        filter: `blur(${lerp(0, 16, p) * u}px)`,
        opacity: 1 - p,
      }}
    >
      {children}
    </div>
  );
};

// Lista em foco (roda de seletor tipo iOS): linha central nítida + seta azul, vizinhas desfocadas.
export const FocusList: React.FC<{items: string[]; steps: number[]; size?: number; enterAt?: number}> = ({
  items,
  steps,
  size = 76,
  enterAt = 0,
}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const idx = steps.reduce((acc, s) => acc + prog(f, s, s + 14, easeInOut), 0);
  const enter = prog(f, enterAt, enterAt + 16);
  const lineH = size * 1.0 * u;
  const nudge = steps.reduce((acc, s) => acc + Math.sin(Math.PI * prog(f, s, s + 14, easeInOut)), 0);
  return (
    <div style={{position: 'relative', width: '100%', height: lineH * 5, opacity: enter, filter: `blur(${lerp(10, 0, enter) * u}px)`}}>
      <div
        style={{
          position: 'absolute',
          left: `calc(50% - ${size * 3.9 * u}px)`,
          top: lineH * 2.5 - size * 0.42 * u,
          fontFamily: FONT_BODY,
          fontWeight: 600,
          fontSize: size * 0.7 * u,
          color: C.blue,
          transform: `translateX(${-nudge * 10 * u}px)`,
        }}
      >
        →
      </div>
      {items.map((t, i) => {
        const d = i - idx;
        const ad = Math.abs(d);
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: `calc(50% - ${size * 3.1 * u}px)`,
              top: lineH * 2.5 + d * lineH - size * 0.55 * u,
              fontFamily: FONT_HEAD,
              fontWeight: 600,
              letterSpacing: '-0.02em',
              fontSize: size * u * interpolate(ad, [0, 1], [1, 0.82], {extrapolateRight: 'clamp'}),
              color: C.ink,
              whiteSpace: 'nowrap',
              opacity: interpolate(ad, [0, 1, 2.4], [1, 0.22, 0], {extrapolateRight: 'clamp'}),
              filter: `blur(${interpolate(ad, [0, 1, 2], [0, 2.5, 5], {extrapolateRight: 'clamp'}) * u}px)`,
            }}
          >
            {t}
          </div>
        );
      })}
    </div>
  );
};

// Palavra de impacto na cena escura: branca, glow, entra de blur 24 + escala 1.15
export const Impact: React.FC<{text: string; at: number; size?: number}> = ({text, at, size = 190}) => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const p = prog(f, at, at + 16);
  return (
    <div
      style={{
        fontFamily: FONT_HEAD,
        fontWeight: 800,
        letterSpacing: '-0.04em',
        fontSize: size * u,
        color: '#fff',
        opacity: p,
        filter: `blur(${lerp(24, 0, p) * u}px)`,
        transform: `scale(${lerp(1.15, 1, p)}) translateY(${lerp(30, 0, p) * u}px)`,
        textShadow: `0 0 ${40 * u}px rgba(200,225,255,.55), 0 0 ${8 * u}px rgba(255,255,255,.6)`,
        textAlign: 'center',
      }}
    >
      {text}
    </div>
  );
};
