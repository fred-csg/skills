// Demo do estilo CLEANSTILL — mostra cada recurso do catálogo (references/cleanstill.md) em ~35 s.
// Serve de ponto de partida: troque textos/tempos pelos da locução e apague o que não usar.
import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame} from 'remotion';
import {C, FONT_BODY, FONT_HEAD, prog, useUnit} from './cleanstill/tokens';
import {NightArc, PastelHaze, SkyClouds} from './cleanstill/backgrounds';
import {FocusList, Impact, Kicker, Line, ZoomExit} from './cleanstill/text';
import {Card, Cursor, Drift, GlassPill, Laptop, LensReveal, PaperCard, Rise, SlotCard, Spark} from './cleanstill/ui';
import {Carousel3D, ThumbWall} from './cleanstill/stage';
import {BlobReveal, Bloom, RayBurst} from './cleanstill/transitions';

const Center: React.FC<{children: React.ReactNode; gap?: number}> = ({children, gap = 0}) => (
  <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap}}>{children}</AbsoluteFill>
);

// A · hook no céu
const SceneA: React.FC = () => (
  <AbsoluteFill>
    <Drift dur={62} to={1.08}>
      <SkyClouds seed={3} />
    </Drift>
    <Center>
      <Line size={96} color="#fff" glow words={[{t: 'E', at: 6}, {t: 'se…', at: 12}]} style={{marginTop: -120}} />
    </Center>
  </AbsoluteFill>
);

// B · kicker + palavra-chave azul com brilho + serifa itálica; sai em zoom-through
const SceneB: React.FC = () => {
  const {u} = useUnit();
  return (
    <ZoomExit at={110}>
      <Kicker text="você poderia criar" at={6} size={42} />
      <div style={{height: 10 * u}} />
      <Line size={170} words={[{t: 'vídeos', at: 16, s: 'key'}]} />
      <Line size={96} words={[{t: 'como', at: 44, s: 'serif'}, {t: 'esses?', at: 52, s: 'serif'}]} style={{marginTop: -6 * u}} />
    </ZoomExit>
  );
};

// C · lista em foco
const SceneC: React.FC = () => (
  <ZoomExit at={112} to={1.12}>
    <FocusList items={['Sem estúdio.', 'Sem editor.', 'Sem equipe.', 'Sem orçamento.']} steps={[28, 56, 84]} size={80} />
  </ZoomExit>
);

// D · texto à esquerda + cartão-arquivo com seleção e cursor à direita
const SceneD: React.FC = () => {
  const {u, vertical} = useUnit();
  return (
    <AbsoluteFill style={{flexDirection: vertical ? 'column-reverse' : 'row', alignItems: 'center', justifyContent: 'center', gap: (vertical ? 80 : 160) * u}}>
      <div style={{textAlign: vertical ? 'center' : 'left'}}>
        <Kicker text="Só isso." at={4} size={44} align={vertical ? 'center' : 'left'} />
        <div style={{height: 14 * u}} />
        <Line size={118} align={vertical ? 'center' : 'left'} words={[{t: 'Um', at: 14}, {t: 'arquivo.', at: 22, s: 'key'}]} />
      </div>
      <div style={{position: 'relative'}}>
        <PaperCard at={8} select={34} tag="ROTEIRO.md" title="ROTEIRO.md" sub="motion-cleanstill" meta={['nome: cleanstill', 'versão: 1.0', 'estilo: limpo e calmo']} w={480} />
        <Cursor path={[[40, 560, 640], [70, 380, 470], [100, 400, 500]]} clicks={[72]} />
      </div>
    </AbsoluteFill>
  );
};

// E · objeto herói flutuando no céu + pills de vidro nas laterais
const AppScreen: React.FC = () => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const typed = 'faça um anúncio cinematográfico'.slice(0, Math.max(0, Math.floor((f - 50) / 1.6)));
  return (
    <AbsoluteFill style={{background: '#f7f7f9', fontFamily: FONT_BODY}}>
      <div style={{position: 'absolute', left: 18 * u, top: 14 * u, display: 'flex', gap: 8 * u}}>
        {['#ff5f57', '#febc2e', '#28c840'].map((c) => (
          <div key={c} style={{width: 12 * u, height: 12 * u, borderRadius: '50%', background: c}} />
        ))}
      </div>
      <div style={{position: 'absolute', left: '12%', right: '12%', top: '42%'}}>
        <Spark size={40 * u} style={{marginBottom: 14 * u}} />
        <div
          style={{
            background: '#fff',
            borderRadius: 16 * u,
            border: `${1.5 * u}px solid #e3e5ec`,
            padding: `${18 * u}px ${20 * u}px`,
            fontSize: 22 * u,
            color: C.ink,
            boxShadow: `0 ${8 * u}px ${24 * u}px rgba(0,0,0,.05)`,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <span>
            {typed}
            <span style={{opacity: Math.floor(f / 8) % 2 ? 1 : 0, color: C.blue}}>|</span>
          </span>
          <div style={{width: 34 * u, height: 34 * u, borderRadius: '50%', background: C.pill, color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 20 * u}}>↑</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
const SceneE: React.FC = () => {
  const f = useCurrentFrame();
  const {u, vertical} = useUnit();
  const bob = Math.sin(f / 26) * 8;
  return (
    <AbsoluteFill>
      <SkyClouds seed={9} />
      <Drift dur={150} from={0.94} to={1.04}>
        <Center>
          <div style={{transform: `translateY(${bob * u}px)`}}>
            <Laptop w={vertical ? 820 : 800} screen={<AppScreen />} />
          </div>
        </Center>
        <AbsoluteFill>
          <GlassPill text="joguei o arquivo" at={26} from="left" style={vertical ? {left: 90 * u, top: '24%'} : {left: '4%', top: '40%'}} />
          <GlassPill text="no editor de IA" at={40} from="right" style={vertical ? {right: 90 * u, top: '70%'} : {right: '4%', top: '40%'}} />
        </AbsoluteFill>
      </Drift>
    </AbsoluteFill>
  );
};

// F · frase karaokê (palavras-fantasma) + carrossel 3D com pills de preço
const SceneF: React.FC = () => {
  const {u, vertical} = useUnit();
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{top: (vertical ? 300 : 90) * u, height: 'auto', padding: `0 ${70 * u}px`}}>
        <Line
          size={vertical ? 92 : 84}
          ghost
          words={[
            {t: 'Todo', at: 8},
            {t: 'dia,', at: 14},
            {t: 'gente', at: 26},
            {t: 'paga', at: 34},
            {t: 'milhares', at: 44, s: 'key'},
          ]}
        />
      </AbsoluteFill>
      <Carousel3D at={4} n={7} cardW={vertical ? 660 : 640} radius={vertical ? 1500 : 1700} spread={vertical ? 21 : 23} prices={[null, 'R$ 9.800', null, 'R$ 12.000', null, 'R$ 7.500', null]} y={vertical ? 80 : 90} />
    </AbsoluteFill>
  );
};

// G · parede de miniaturas + cartão de vidro com slot de palavras
const SceneG: React.FC = () => (
  <AbsoluteFill>
    <ThumbWall at={0} />
    <Center>
      <SlotCard at={6} items={['Portfólios', 'Lojas', 'Landing pages']} steps={[32, 60]} size={54} />
    </Center>
  </AbsoluteFill>
);

// H · virada escura com arco de planeta, destaque "selecionado" e palavra de impacto
const SceneH: React.FC = () => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  return (
    <AbsoluteFill>
      <NightArc rise={prog(f, 0, 130)} />
      <Center gap={50 * u}>
        <Line
          size={66}
          color="#fff"
          glow
          words={[
            {t: 'E', at: 8, s: 'white'},
            {t: 'agora', at: 14, s: 'white'},
            {t: 'você', at: 22, s: 'white'},
            {t: 'tá', at: 30, s: 'white'},
            {t: 'pensando…', at: 38, s: 'hl'},
          ]}
          style={{marginTop: -160 * u}}
        />
        <Impact text="sem chance." at={64} />
      </Center>
    </AbsoluteFill>
  );
};

// I · cartão com lupa revelando o "depois" + fecho
const SceneI: React.FC = () => {
  const f = useCurrentFrame();
  const {u} = useUnit();
  const W = 640;
  const H = 380;
  const big = (t: string, c: string) => (
    <div style={{fontFamily: FONT_HEAD, fontWeight: 800, fontSize: 170 * u, letterSpacing: '-0.03em', color: c}}>{t}</div>
  );
  const out = prog(f, 118, 130);
  return (
    <AbsoluteFill style={{opacity: 1 - out, filter: `blur(${out * 14 * u}px)`}}>
      <Center gap={40 * u}>
        <Line size={70} words={[{t: 'Depois', at: 4}, {t: 'disso,', at: 12}, {t: 'é', at: 64}, {t: 'pago.', at: 70, s: 'key'}]} />
        <Rise at={10}>
          <LensReveal
            w={W}
            h={H}
            a={<Card w={W} h={H} label="ROTEIRO.md · primeiros 200">{big('GRÁTIS', C.blue)}</Card>}
            b={<Card w={W} h={H} bg="#fbe9df" label="ROTEIRO.md · depois dos 200">{big('PAGO', C.warm)}</Card>}
            path={[[26, 0.12, 0.6], [56, 0.45, 0.58], [80, 0.7, 0.55]]}
            swapAt={84}
            r={95}
          />
        </Rise>
      </Center>
    </AbsoluteFill>
  );
};

export const CleanstillDemo: React.FC = () => {
  return (
    <AbsoluteFill style={{background: C.bg}}>
      {/* fundos */}
      <Sequence from={0} durationInFrames={62}>
        <SceneA />
      </Sequence>
      <Sequence from={57} durationInFrames={380}>
        <PastelHaze seed={1} />
      </Sequence>
      <Sequence from={545} durationInFrames={160}>
        <PastelHaze seed={4} />
      </Sequence>
      <Sequence from={920} durationInFrames={140}>
        <PastelHaze seed={8} />
      </Sequence>

      {/* conteúdo */}
      <Sequence from={57} durationInFrames={125}>
        <SceneB />
      </Sequence>
      <Sequence from={178} durationInFrames={128}>
        <SceneC />
      </Sequence>
      <Sequence from={300} durationInFrames={135}>
        <SceneD />
      </Sequence>
      <Sequence from={0} durationInFrames={553}>
        <BlobReveal at={412} dur={22}>
          <Sequence from={412} durationInFrames={141}>
            <SceneE />
          </Sequence>
        </BlobReveal>
      </Sequence>
      <Sequence from={556} durationInFrames={146}>
        <SceneF />
      </Sequence>
      <Sequence from={700} durationInFrames={102}>
        <SceneG />
      </Sequence>
      <Sequence from={800} durationInFrames={122}>
        <SceneH />
      </Sequence>
      <Sequence from={920} durationInFrames={140}>
        <SceneI />
      </Sequence>

      {/* transições por cima */}
      <Bloom at={44} dur={20} />
      <Bloom at={540} dur={20} />
      <RayBurst at={784} dur={26} />
    </AbsoluteFill>
  );
};

export const DEMO_FRAMES = 1060;
