import {loadFont} from '@remotion/google-fonts/Poppins';
import {ThreeCanvas} from '@remotion/three';
import {useEffect, useState} from 'react';
import {AbsoluteFill, Audio, continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {inOut, outBack, outCubic, outExpo, prog} from './anim';
import {LOOKS, LookName} from './scene/looks';
import {Scene, T} from './scene/Scene';

const {fontFamily, waitUntilDone} = loadFont('normal', {weights: ['600', '700', '800', '900'], subsets: ['latin', 'latin-ext']});

// Texto letra por letra, cada caractere com easing próprio
const TypeText = ({text, start, f, step = 1.4, style}: {text: string; start: number; f: number; step?: number; style?: React.CSSProperties}) => (
  <span style={{display: 'inline-block', whiteSpace: 'pre', ...style}}>
    {text.split('').map((ch, i) => {
      const p = prog(f, start + i * step, start + i * step + 12, outCubic);
      return (
        <span key={i} style={{display: 'inline-block', opacity: p, transform: `translateY(${(1 - p) * 18}px)`, filter: `blur(${(1 - p) * 6}px)`}}>
          {ch}
        </span>
      );
    })}
  </span>
);

const STEPS = [
  {at: 0, txt: '01 · PLANTA BAIXA'},
  {at: T.orbit[0] + 6, txt: '02 · PERSPECTIVA'},
  {at: T.walls[0] + 6, txt: '03 · ESTRUTURA'},
  {at: T.furn[0] + 4, txt: '04 · AMBIENTAÇÃO'},
];

const Corner = ({x, y, r, c}: {x: string; y: string; r: number; c: string}) => (
  <div
    style={{
      position: 'absolute',
      [x]: 56,
      [y]: 56,
      width: 46,
      height: 46,
      borderTop: `3px solid ${c}`,
      borderLeft: `3px solid ${c}`,
      transform: `rotate(${r}deg)`,
      opacity: 0.8,
    }}
  />
);

const Hud = ({f, accent}: {f: number; accent: string}) => {
  const LIME = accent;
  const {durationInFrames} = useVideoConfig();
  const inA = prog(f, 4, 26, outCubic);
  const stepIdx = STEPS.reduce((acc, s, i) => (f >= s.at ? i : acc), 0);
  const step = STEPS[stepIdx];
  const sp = prog(f, step.at, step.at + 14, outExpo);
  // bússola gira junto com a câmera
  const theta = 0.8 * prog(f, 74, 182, inOut) + 0.45 * prog(f, 160, 450);
  const card = prog(f, 352, 378, outBack);
  const area = Math.round(interpolate(prog(f, 356, 400, outCubic), [0, 1], [0, 80]));

  return (
    <AbsoluteFill style={{fontFamily, color: '#F2F4EE', opacity: inA}}>
      <Corner x="left" y="top" r={0} c={accent} />
      <Corner x="right" y="top" r={90} c={accent} />
      <Corner x="left" y="bottom" r={-90} c={accent} />
      <Corner x="right" y="bottom" r={180} c={accent} />

      {/* barra de progresso */}
      <div style={{position: 'absolute', left: 120, right: 120, top: 92, height: 3, background: 'rgba(255,255,255,.12)', borderRadius: 2}}>
        <div style={{width: `${(f / (durationInFrames - 1)) * 100}%`, height: '100%', background: LIME, borderRadius: 2, boxShadow: `0 0 12px ${LIME}`}} />
      </div>

      {/* etapa */}
      <div style={{position: 'absolute', left: 120, top: 128}}>
        <div
          style={{
                        fontSize: 44,
            fontWeight: 800,
            letterSpacing: 1,
            color: LIME,
            textShadow: `0 0 24px ${accent}66`,
            opacity: sp,
            transform: `translateX(${(1 - sp) * -40}px)`,
          }}
        >
          <TypeText key={step.txt} text={step.txt} start={step.at} f={f} step={1.1} />
        </div>
      </div>

      {/* bússola */}
      <div style={{position: 'absolute', right: 120, top: 128, width: 96, height: 96, borderRadius: 48, border: '2px solid rgba(255,255,255,.25)', display: 'grid', placeItems: 'center'}}>
        <div style={{transform: `rotate(${(-theta * 180) / Math.PI}deg)`, display: 'grid', placeItems: 'center'}}>
          <div style={{width: 0, height: 0, borderLeft: '10px solid transparent', borderRight: '10px solid transparent', borderBottom: `30px solid ${LIME}`, marginBottom: 4}} />
          <div style={{fontSize: 18, fontWeight: 700}}>N</div>
        </div>
      </div>

      {/* card final */}
      {card > 0 && (
        <div
          style={{
            position: 'absolute',
            left: 120,
            right: 120,
            bottom: 210,
            padding: '36px 44px',
            borderRadius: 32,
            background: 'rgba(10,20,42,.5)',
            border: `1.5px solid ${accent}55`,
            backdropFilter: 'blur(18px)',
            boxShadow: '0 30px 80px rgba(0,0,0,.45)',
            opacity: Math.min(card, 1),
            transform: `perspective(1100px) rotateX(${(1 - card) * -38}deg) translateY(${(1 - card) * 60}px)`,
            transformOrigin: '50% 100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div>
            <div style={{fontSize: 22, letterSpacing: 5, fontWeight: 600, opacity: 0.6}}>ÁREA TOTAL</div>
            <div style={{fontSize: 108, fontWeight: 800, lineHeight: 1, marginTop: 6}}>
              {area}
              <span style={{fontSize: 48, color: LIME, marginLeft: 8}}>m²</span>
            </div>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', gap: 12, alignItems: 'flex-end'}}>
            {['1 QUARTO', '1 BANHO', 'SALA + COZINHA'].map((c, i) => {
              const cp = prog(f, 366 + i * 5, 384 + i * 5, outBack);
              return (
                <div
                  key={c}
                  style={{
                    fontSize: 22,
                    fontWeight: 700,
                    letterSpacing: 2,
                    padding: '10px 18px',
                    borderRadius: 999,
                    border: `1.5px solid ${LIME}`,
                    color: LIME,
                    background: `${accent}14`,
                    opacity: cp,
                    transform: `scale(${0.6 + 0.4 * cp})`,
                  }}
                >
                  {c}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};

export const Planta3D = ({look = 'vidro'}: {look?: LookName}) => {
  const L = LOOKS[look];
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const [handle] = useState(() => delayRender('fontes'));
  const [ready, setReady] = useState(false);
  useEffect(() => {
    waitUntilDone().then(() => {
      setReady(true);
      continueRender(handle);
    });
  }, [handle]);

  const fadeIn = prog(f, 0, 14, outCubic);
  return (
    <AbsoluteFill
      style={{
        background: 'radial-gradient(120% 80% at 50% 45%, #141a17 0%, #07090a 60%, #040505 100%)'
      }}
    >
      <AbsoluteFill style={{opacity: fadeIn}}>
        {ready && (
          <ThreeCanvas width={width} height={height} shadows gl={{antialias: true, alpha: true}} camera={{fov: 40, near: 0.1, far: 200, position: [0, 24, 0.05]}}>
            <Scene look={L} />
          </ThreeCanvas>
        )}
      </AbsoluteFill>
      {/* vinheta */}
      <AbsoluteFill style={{background: 'radial-gradient(90% 70% at 50% 50%, transparent 55%, rgba(2,6,16,.5) 100%)', pointerEvents: 'none'}} />
      {ready && <Hud f={f} accent={L.accent} />}
      {/* SFX gerado por código: node sfx/sfx.mjs sfx/planta-cues.mjs public/sfx <vidro|holograma> */}
      <Audio src={staticFile(`sfx/planta-${look === 'holograma' ? 'holograma' : 'vidro'}.wav`)} />
    </AbsoluteFill>
  );
};
