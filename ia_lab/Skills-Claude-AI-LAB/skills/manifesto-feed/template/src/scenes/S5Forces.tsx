import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, F} from '../lib/theme';
import {E, SPR, clamp, kick, lerp, noise, prog, sp} from '../lib/motion';
import {CameraRig, L3} from '../components/CameraRig';
import {MaskReveal, Mono} from '../components/KineticTypography';
import {K} from '../data/script';
import {OrbitLight, glowAt} from '../components/FX';
import {S4_LAYOUT} from './S4Loop';

const SZ = 230;
const ROWS = [-400, 0, 400]; // y (mundo, centro = 0)
const SHAPE_X = -270;
// posição de origem de cada forma (de onde ela nasce na contração da cena 4)
const ORIGIN = [
	{x: 0, y: S4_LAYOUT.beltY - 960},
	{x: 0, y: 0},
	{x: 0, y: S4_LAYOUT.cardCY - 960},
];
// ponto de encaixe do emblema
export const EMBLEM_Y = -110;

const Parallelogram: React.FC<{fill?: string; op?: number}> = ({fill = C.white, op = 1}) => (
	<svg width={SZ * 1.3} height={SZ * 0.42} viewBox="0 0 130 42" style={{display: 'block', opacity: op}}>
		<polygon points="22,0 130,0 108,42 0,42" fill={fill} />
	</svg>
);

/** Extrusão 2.5D: empilha cópias em Z com sombreamento — ícones com volume real que respondem à câmera. */
const Extrude: React.FC<{depth: number; layers?: number; w: number; h: number; glow?: number; render: (color: string, front: boolean) => React.ReactNode}> = ({
	depth,
	glow = 0.3,
	layers = 12,
	w,
	h,
	render,
}) => (
	<div style={{position: 'relative', width: w, height: h, transformStyle: 'preserve-3d'}}>
		{Array.from({length: layers + 1}).map((_, k) => {
			const back = layers - k; // desenha de trás para frente
			const t = back / layers;
			const v = Math.round(lerp(0xf4, 0x3a, Math.pow(t, 0.6)));
			const color = back === 0 ? C.white : `rgb(${v - 4},${v - 2},${v - 6})`;
			return (
				<div key={k} style={{position: 'absolute', inset: 0, transform: `translateZ(${-t * depth}px)`, filter: back === 0 && glow > 0.01 ? `drop-shadow(0 0 ${8 + 26 * glow}px rgba(244,243,238,${0.35 + 0.4 * glow}))` : undefined}}>
					{render(color, back === 0)}
				</div>
			);
		})}
	</div>
);

export const S5Forces: React.FC<{f: number}> = ({f}) => {
	const born = sp(f, K.contract + 6, {damping: 18, stiffness: 120, mass: 0.9});
	const lock = sp(f, K.lock, {damping: 15, stiffness: 160, mass: 0.8});
	const settle = sp(f, K.lock + 10, SPR.lock);
	const out = prog(f, K.produce - 4, K.produce + 10, E.inExpo);

	// VELOCIDADE: dispara para a direita e volta com rastros
	const vel = prog(f, K.velocidade - 2, K.velocidade + 8, E.inExpo) * (1 - prog(f, K.velocidade + 8, K.velocidade + 24, E.outExpo));
	const velX = vel * 300;
	// CUSTO MENOR: 4 camadas colapsam em 1 e a forma contrai
	const cost = prog(f, K.custo - 2, K.custo + 16, E.outExpo);
	const costScale = lerp(1, 0.78, prog(f, K.custo + 4, K.custo + 20, E.overshoot));
	// QUALIDADE: traço de precisão + guias que encaixam
	const qDraw = prog(f, K.qualidade - 6, K.qualidade + 14, E.inOutSine);
	const qGuides = sp(f, K.qualidade + 6, SPR.lock);

	const labelsOut = prog(f, K.lock - 6, K.lock + 4, E.inQuart);

	// movimentos próprios dos ícones 3D (todos voltam a 0° no travamento)
	const free = 1 - lock;
	const iconGlow = 0.25 + 0.75 * Math.max(glowAt(f, K.lock + 8, 14, 26), glowAt(f, K.velocidade + 4, 4, 14), glowAt(f, K.custo + 4, 4, 14) * 0.6);
	const idle = (seed: number, amp: number) => noise(f / 34, seed) * amp;
	// velocidade: inclina contra o disparo (antecipação) e assenta com overshoot
	const velRy = (lerp(-24, 0, prog(f, K.velocidade - 8, K.velocidade - 2, E.outQuart)) * (1 - prog(f, K.velocidade - 2, K.velocidade + 4, E.linear)) + 38 * vel + kick(f, K.velocidade + 22, 16, 0.5, 0.14) + idle(41, 6) - 14) * free;
	const velRx = (idle(42, 4) + 10) * free;
	// custo menor: placa gira devagar; ao colapsar fica mais fina e trava de frente
	const costRy = (lerp(-32, -8, cost) + idle(43, 5)) * free;
	const costRx = (lerp(16, 6, cost) + idle(44, 3)) * free;
	// qualidade: anel gira e só para perfeitamente alinhado quando o traço fecha
	const qAlign = prog(f, K.qualidade - 16, K.qualidade + 16, E.outQuart);
	const qRy = (lerp(170, 0, qAlign) + (qAlign >= 1 ? 0 : idle(45, 4))) * free;
	const qRx = lerp(22, 0, qAlign) * free;

	// posições finais (emblema) — atração magnética
	const pos = (i: number) => {
		const bx = lerp(ORIGIN[i].x, SHAPE_X, born);
		const by = lerp(ORIGIN[i].y, ROWS[i], born);
		return {x: lerp(bx, 0, lock), y: lerp(by, EMBLEM_Y, lock)};
	};
	const p0 = pos(0), p1 = pos(1), p2 = pos(2);

	const cam = {
		ry: noise(f / 60, 21) * 6 + lerp(-10, 10, prog(f, K.contract, K.lock, E.inOutSine)) * (1 - lock),
		rx: noise(f / 70, 22) * 3 + 4 * (1 - lock),
		z: lerp(0, 160, lock) + kick(f, K.lock + 8, 40, 0.5, 0.2),
		perspective: 1700,
	};

	const op = born * (1 - out);
	const ring = prog(f, K.lock + 8, K.lock + 30, E.outExpo);

	const Label: React.FC<{i: number; word: string; at: number}> = ({i, word, at}) => (
		<div style={{position: 'absolute', left: 430, top: 960 + ROWS[i] - 70, opacity: 1 - labelsOut}}>
			<Mono style={{fontSize: 22, marginBottom: 8, opacity: prog(f, at - 8, at, E.linear)}}>{`0${i + 1}`}</Mono>
			<MaskReveal text={word} f={f} start={at - 4} stagger={1.1} style={{fontWeight: 900, fontSize: 80, letterSpacing: '-0.035em'}} />
		</div>
	);

	return (
		<AbsoluteFill style={{opacity: 1 - out * 0}}>
			<CameraRig cam={cam}>
				{/* VELOCIDADE */}
				{[5, 4, 3, 2, 1].map((k) => (
					<L3 key={k} x={p0.x + velX - k * vel * 70} y={p0.y} z={-k * 6} w={SZ * 1.3} h={SZ * 0.42} opacity={op * vel * (0.5 - k * 0.08)}>
						<Parallelogram fill={C.gray} />
					</L3>
				))}
				<L3 x={p0.x + velX} y={p0.y} z={lerp(0, 40, lock)} w={SZ * 1.3} h={SZ * 0.42} s={lerp(1, 0.86, lock)} opacity={op} ry={velRy} rx={velRx}>
					<Extrude glow={iconGlow} depth={lerp(46, 14, lock)} w={SZ * 1.3} h={SZ * 0.42} render={(c) => <Parallelogram fill={c} />} />
				</L3>
				{/* CUSTO MENOR */}
				{[3, 2, 1].map((k) => (
					<L3 key={k} x={p1.x + k * 22 * (1 - cost)} y={p1.y - k * 22 * (1 - cost)} z={-k * 30 * (1 - cost)} w={SZ} h={SZ} s={costScale * lerp(1, 1.25, lock)} opacity={op * (1 - cost) * (1 - k * 0.2)}>
						<div style={{width: SZ, height: SZ, boxShadow: `inset 0 0 0 3px ${C.gray}`, borderRadius: 18}} />
					</L3>
				))}
				<L3 x={p1.x} y={p1.y} z={0} w={SZ} h={SZ} s={costScale * lerp(1, 1.25, lock)} ry={costRy} rx={costRx} opacity={op}>
					<Extrude
						depth={lerp(lerp(70, 16, cost), 12, lock)}
						layers={10}
						w={SZ}
						h={SZ}
						render={(c) => <div style={{width: SZ, height: SZ, borderRadius: 18, boxShadow: `inset 0 0 0 ${lerp(3, 10, cost)}px ${c}`}} />}
					/>
				</L3>
				{/* QUALIDADE */}
				<L3 x={p2.x} y={p2.y} z={lerp(0, 20, lock)} w={SZ + 120} h={SZ + 120} s={lerp(1, 0.62, lock)} opacity={op} ry={qRy} rx={qRx}>
					<div style={{position: 'absolute', inset: 0, transformStyle: 'preserve-3d'}}>
						<Extrude
							depth={lerp(36, 10, lock)}
							layers={10}
							w={SZ + 120}
							h={SZ + 120}
							render={(c, front) =>
								front ? null : (
									<svg width={SZ + 120} height={SZ + 120} viewBox={`-60 -60 ${SZ + 120} ${SZ + 120}`}>
										<circle cx={SZ / 2} cy={SZ / 2} r={SZ / 2 - 6} fill="none" stroke={c} strokeWidth={10} opacity={lerp(0.55, 1, qDraw)} />
									</svg>
								)
							}
						/>
					</div>
					<svg width={SZ + 120} height={SZ + 120} viewBox={`-60 -60 ${SZ + 120} ${SZ + 120}`} style={{position: 'absolute', inset: 0}}>
						<circle cx={SZ / 2} cy={SZ / 2} r={SZ / 2 - 6} fill="none" stroke={C.white} strokeWidth={10} strokeDasharray={Math.PI * (SZ - 12)} strokeDashoffset={Math.PI * (SZ - 12) * (1 - qDraw)} transform={`rotate(-90 ${SZ / 2} ${SZ / 2})`} strokeLinecap="round" />
						<g opacity={qGuides * (1 - lock)} stroke={C.gray} strokeWidth={1.5}>
							<line x1={-50 - (1 - qGuides) * 40} y1={SZ / 2} x2={SZ + 50 + (1 - qGuides) * 40} y2={SZ / 2} />
							<line x1={SZ / 2} y1={-50 - (1 - qGuides) * 40} x2={SZ / 2} y2={SZ + 50 + (1 - qGuides) * 40} />
							{Array.from({length: 13}).map((_, t) => (
								<line key={t} x1={-50 + t * ((SZ + 100) / 12)} y1={SZ + 40} x2={-50 + t * ((SZ + 100) / 12)} y2={SZ + 40 + (t % 3 === 0 ? 16 : 8)} />
							))}
						</g>
						{qDraw >= 1 && <circle cx={SZ / 2} cy={SZ / 2} r={7} fill={C.white} opacity={1 - lock} />}
					</svg>
				</L3>
				{/* luzes orbitando cada ícone antes da atração magnética */}
				{[p0, p1, p2].map((p, i) => (
					<L3 key={`orb${i}`} x={p.x} y={p.y} z={60} w={SZ * 1.45} h={SZ * 1.45}>
						<OrbitLight f={f} start={K.lock - 24 + i * 3} dur={30} w={SZ * 1.45} h={SZ * 1.45} circle laps={1.6} runners={2} width={5} outline={0.25} />
					</L3>
				))}
				{/* depois do travamento, uma órbita só em volta do emblema */}
				<L3 x={0} y={EMBLEM_Y} z={80} w={430} h={430}>
					<OrbitLight f={f} start={K.lock + 8} dur={34} w={430} h={430} circle laps={1.2} runners={3} width={5} />
				</L3>
				{/* onda de travamento */}
				{ring > 0 && ring < 1 && (
					<L3 x={0} y={EMBLEM_Y} w={10} h={10} opacity={(1 - ring) * 0.6}>
						<div style={{position: 'absolute', left: 5 - 200 * (0.8 + ring), top: 5 - 200 * (0.8 + ring), width: 400 * (0.8 + ring), height: 400 * (0.8 + ring), borderRadius: 999, boxShadow: `inset 0 0 0 2px ${C.white}`}} />
					</L3>
				)}
			</CameraRig>
			<Label i={0} word="VELOCIDADE" at={K.velocidade + 16} />
			<Label i={1} word="CUSTO MENOR" at={K.custo} />
			<Label i={2} word="QUALIDADE" at={K.qualidade} />
			<AbsoluteFill style={{top: 960 + EMBLEM_Y + 260, alignItems: 'center', opacity: 1 - out}}>
				<MaskReveal text="E ISSO MUDA TUDO." f={f} start={K.mudaTudo - 6} stagger={1} style={{fontWeight: 900, fontSize: 76, letterSpacing: '-0.03em'}} />
				<Mono style={{marginTop: 18, opacity: clamp(settle) * prog(f, K.mudaTudo + 4, K.mudaTudo + 14, E.linear)}}>SISTEMA 01 · ONLINE</Mono>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
