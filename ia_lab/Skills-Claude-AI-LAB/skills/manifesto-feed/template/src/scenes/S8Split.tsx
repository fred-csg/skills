import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, F} from '../lib/theme';
import {E, SPR, clamp, hash, lerp, noise, prog, sp} from '../lib/motion';
import {MaskReveal, Mono} from '../components/KineticTypography';
import {FeedCard} from '../components/FeedCards';
import {K} from '../data/script';
import {HERO_IMAGE} from '../data/morphix-assets';
import {OrbitLight} from '../components/FX';

type P = [number, number];
const bez = (p0: P, p1: P, p2: P, p3: P, t: number): P => {
	const u = 1 - t;
	return [
		u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
		u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1],
	];
};
const FORK: P = [540, 1180];
const TRUNK: P = [540, 1660];
const LEFT: [P, P, P, P] = [FORK, [540, 900], [250, 1000], [250, -200]];
const RIGHT: [P, P, P, P] = [FORK, [540, 900], [830, 1000], [830, -200]];
const STOP_Y = 640;
const tStop = (() => {
	let lo = 0, hi = 1;
	for (let i = 0; i < 30; i++) {
		const m = (lo + hi) / 2;
		if (bez(...RIGHT, m)[1] > STOP_Y) lo = m;
		else hi = m;
	}
	return lo;
})();
const pathD = (b: [P, P, P, P]) => `M${b[0][0]},${b[0][1]} C${b[1][0]},${b[1][1]} ${b[2][0]},${b[2][1]} ${b[3][0]},${b[3][1]}`;

const EMIT_GAP = 3; // cadência mecânica: um card a cada 0,1 s
const LIFE = 22; // atravessa rápido demais para ser visto
const CW = 250; // card que merece atenção
const CH = 444;

export const S8Split: React.FC<{f: number}> = ({f}) => {
	const trunk = prog(f, K.splitLine, K.fork, E.inOutSine);
	const branches = prog(f, K.fork, K.fork + 30, E.outQuart);
	const streamOn = f >= K.fork + 6;
	const fadeFuture = prog(f, K.futuro, K.futuro + 20, E.inOutSine); // o fluxo vai embora
	const dolly = prog(f, K.suficiente + 14, K.suficiente + 44, E.inExpo);

	// câmera: acompanha a separação e depois escolhe o lado direito
	const pan = prog(f, K.outro - 6, K.parar + 4, E.camera);
	const camX = lerp(0, -120, pan) + noise(f / 50, 31) * 6;
	const camS = lerp(1, 1.06, pan);
	const leftBlur = lerp(1.5, 6, pan);

	// fluxo da esquerda: infinito, acelerado
	const stream: React.ReactNode[] = [];
	if (streamOn) {
		const first = K.fork + 6;
		const lastEmit = Math.floor((f - first) / EMIT_GAP);
		for (let k = Math.max(0, lastEmit - Math.ceil(LIFE / EMIT_GAP)); k <= lastEmit; k++) {
			const t0 = first + k * EMIT_GAP;
			const t = (f - t0) / LIFE;
			if (t < 0 || t > 1) continue;
			const tt = Math.pow(t, 1.6);
			const [x, y] = bez(...LEFT, tt);
			const born = clamp(t * 6);
			stream.push(
				<div key={k} style={{position: 'absolute', left: x - 62, top: y - 110, transform: `scale(${born * lerp(0.75, 1, tt)}) rotate(${lerp(0, -9, tt)}deg)`, opacity: born * (1 - fadeFuture)}}>
					<FeedCard seed={5000 + (k % 3) * 3} w={124} h={220} meta={false} radius={14} />
				</div>,
			);
		}
	}

	// o card que para
	const cardT0 = K.outro - 4;
	const travel = prog(f, cardT0, K.parar, E.outExpo);
	const [rx, ry] = bez(...RIGHT, travel * tStop);
	const lift = sp(f, K.parar - 2, SPR.heavy);
	const ring = prog(f, K.parar, K.parar + 26, E.outExpo);
	const rightOn = f >= cardT0;

	// dolly para dentro do card
	const dollyScale = lerp(1, 9, dolly);
	const camTransform = `translate(${lerp(camX, 540 - rx * camS - camX, dolly * 0)}px, 0px) scale(${camS})`;

	const labelsOut = prog(f, K.futuro - 4, K.futuro + 10, E.inQuart);

	return (
		<AbsoluteFill style={{opacity: 1}}>
			<AbsoluteFill style={{transform: camTransform, transformOrigin: '540px 960px'}}>
				<AbsoluteFill style={{transform: `scale(${dollyScale})`, transformOrigin: `${rx}px ${ry}px`, opacity: 1}}>
					{/* linhas */}
					<svg width={1080} height={1920} style={{position: 'absolute', opacity: 1 - fadeFuture * 0.85}}>
						<line x1={TRUNK[0]} y1={TRUNK[1]} x2={TRUNK[0]} y2={lerp(TRUNK[1], FORK[1], trunk)} stroke={C.gray} strokeWidth={2.5} />
						{[LEFT, RIGHT].map((b, i) => (
							<path key={i} d={pathD(b)} fill="none" stroke={i ? C.white : C.struct} strokeWidth={2.5} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - branches} opacity={i ? lerp(0.35, 0.9, pan) : 1} />
						))}
						<circle cx={TRUNK[0]} cy={TRUNK[1]} r={6 * prog(f, K.splitLine - 4, K.splitLine + 6, E.overshoot)} fill={C.white} />
					</svg>
					<div style={{position: 'absolute', inset: 0, filter: `blur(${leftBlur}px) grayscale(1)`, opacity: lerp(0.8, 0.32, pan)}}>{stream}</div>
					{rightOn && (
						<div style={{position: 'absolute', left: rx - 520, top: ry - 520, width: 1040, height: 1040, borderRadius: 999, background: 'radial-gradient(circle, rgba(244,243,238,0.075) 0%, rgba(244,243,238,0) 60%)', opacity: lift}} />
					)}
					{rightOn && (
						<div style={{position: 'absolute', left: rx - CW / 2, top: ry - CH / 2, transform: `scale(${lerp(0.4, 1, prog(f, cardT0, cardT0 + 10, E.outExpo)) * lerp(1, 1.3, lift)})`}}>
							{ring > 0 && ring < 1 && (
								<div style={{position: 'absolute', left: -40 * ring, top: -40 * ring, width: CW + 80 * ring, height: CH + 80 * ring, borderRadius: 30, boxShadow: `inset 0 0 0 2px ${C.orange}`, opacity: 1 - ring}} />
							)}
							<FeedCard seed={9} image={HERO_IMAGE} w={CW} h={CH} accent radius={26} progress={lift} style={{boxShadow: `0 ${lerp(10, 50, lift)}px ${lerp(30, 90, lift)}px rgba(0,0,0,0.7), inset 0 0 0 ${lerp(0, 3, lift)}px ${C.orange}, 0 0 ${110 * lift}px rgba(255,99,62,${0.38 * lift})`}} />
							<OrbitLight f={f} start={K.parar - 10} dur={34} w={CW} h={CH} r={26} laps={1.5} runners={2} color={C.orange} width={6} pad={10} />
							<OrbitLight f={f} start={K.suficiente + 4} dur={28} w={CW} h={CH} r={26} laps={1.8} runners={3} color={C.orange} width={5} pad={10} />
							<div style={{position: 'absolute', right: 14, top: 14, width: 14, height: 14, borderRadius: 9, background: C.orange, transform: `scale(${lift})`}} />
						</div>
					)}
				</AbsoluteFill>
			</AbsoluteFill>
			{/* rótulos */}
			<AbsoluteFill style={{top: 240, alignItems: 'center', opacity: 1 - prog(f, K.ocupar - 20, K.ocupar - 6, E.linear)}}>
				<Mono style={{opacity: prog(f, K.splitLine + 4, K.splitLine + 16, E.linear)}}>O CONTEÚDO ESTÁ SE DIVIDINDO</Mono>
			</AbsoluteFill>
			<div style={{position: 'absolute', left: 70 + camX * 0.6, top: 1330, opacity: (1 - labelsOut) * lerp(1, 0.55, pan)}}>
				<Mono style={{fontSize: 20, marginBottom: 10, opacity: prog(f, K.ocupar - 14, K.ocupar - 6, E.linear)}}>DE UM LADO</Mono>
				<MaskReveal text="OCUPAR" f={f} start={K.ocupar - 12} stagger={1} style={{fontWeight: 900, fontSize: 62, letterSpacing: '-0.03em', color: C.gray, lineHeight: 1}} />
				<MaskReveal text="O FEED" f={f} start={K.ocupar - 6} stagger={1} style={{fontWeight: 900, fontSize: 62, letterSpacing: '-0.03em', color: C.gray, lineHeight: 1}} />
			</div>
			<div style={{position: 'absolute', right: 70 - camX * 0.4, top: 1330, textAlign: 'right', opacity: 1 - labelsOut, display: 'flex', flexDirection: 'column', alignItems: 'flex-end'}}>
				<Mono style={{fontSize: 20, marginBottom: 10, opacity: prog(f, K.outro - 4, K.outro + 4, E.linear)}}>DO OUTRO</Mono>
				<MaskReveal text="FAZER" f={f} start={K.parar - 14} stagger={1} style={{fontWeight: 900, fontSize: 62, letterSpacing: '-0.03em', lineHeight: 1}} />
				<MaskReveal text="PARAR" f={f} start={K.parar - 4} stagger={1.2} style={{fontWeight: 900, fontSize: 62, letterSpacing: '-0.03em', lineHeight: 1}} />
			</div>
			{/* produzir mais não será suficiente */}
			<AbsoluteFill style={{top: 1290, alignItems: 'center', opacity: 1 - dolly}}>
				<div style={{position: 'relative'}}>
					<MaskReveal text="TODO MUNDO PRODUZ." f={f} start={K.futuro + 10} stagger={0.8} style={{fontWeight: 900, fontSize: 80, letterSpacing: '-0.035em', color: f > K.suficiente + 2 ? C.gray : C.white}} />
					<div style={{position: 'absolute', left: -14, top: '52%', height: 7, right: -14, background: C.white, transformOrigin: 'left center', transform: `scaleX(${prog(f, K.suficiente - 2, K.suficiente + 8, E.outExpo)})`}} />
				</div>
				<Mono style={{marginTop: 26, opacity: prog(f, K.suficiente + 2, K.suficiente + 12, E.linear)}}>VIROU O MÍNIMO</Mono>
			</AbsoluteFill>
			{/* interior do card: preenche a tela no fim do dolly */}
			<AbsoluteFill style={{background: C.bg, opacity: prog(f, K.suficiente + 36, K.suficiente + 46, E.linear)}} />
		</AbsoluteFill>
	);
};
