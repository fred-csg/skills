import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, F} from '../lib/theme';
import {E, hash, lerp, prog, rng} from '../lib/motion';
import {Chars, Mono} from '../components/KineticTypography';
import {K} from '../data/script';
import {OrbitLight} from '../components/FX';

const WORD = 'INCRÍVEL';
const FS = 104;
const ROW_H = 118;
const WORD_W = 560; // passo horizontal entre repetições
const ROWS = 17;
const MID = 8;

const mixColor = (a: string, b: string, t: number) => {
	const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
	const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
	return `rgb(${pa.map((v, i) => Math.round(lerp(v, pb[i], t))).join(',')})`;
};

export const S7Paradox: React.FC<{f: number}> = ({f}) => {
	const start = K.incrivelWall;
	// velocidade das fileiras: corre e desacelera até a imobilidade
	const speedT = (t: number) => (t < start ? 0 : 1 - prog(t, K.tudoIncrivel, K.still, E.outQuart));
	let travel = 0;
	for (let t = start; t < f; t++) travel += speedT(t) * 9;
	const saturate = prog(f, start + 8, K.tudoIncrivel + 4, E.inOutSine); // perde força
	const othersOut = prog(f, K.still - 2, K.still + 14, E.inOutSine);
	const dissolve = prog(f, K.dissolve, K.dissolve + 12, E.inQuart);
	const out = prog(f, 958, 972, E.linear);

	const words: React.ReactNode[] = [];
	for (let r = 0; r < ROWS; r++) {
		const dr = Math.abs(r - MID);
		const rowStart = start + dr * 2.2;
		if (f < rowStart) continue;
		const dir = r % 2 ? 1 : -1;
		const off = r === MID ? 0 : (dir * travel * (0.7 + hash(r) * 0.6)) % WORD_W;
		for (let c = -3; c <= 3; c++) {
			if (r === MID && c === 0) continue;
			const appear = prog(f, rowStart + Math.abs(c) * 2.4, rowStart + Math.abs(c) * 2.4 + 8, E.outExpo);
			if (appear <= 0) continue;
			// cópias nascem da palavra vizinha (duplicação)
			const x = 540 + (c * WORD_W + off) * lerp(0.4, 1, appear);
			const y = 960 + (r - MID) * ROW_H;
			words.push(
				<div
					key={`${r}:${c}`}
					style={{
						position: 'absolute',
						left: x,
						top: y,
						transform: 'translate(-50%, -50%)',
						fontFamily: F.display,
						fontWeight: 900,
						fontSize: FS,
						letterSpacing: '-0.03em',
						whiteSpace: 'nowrap',
						color: mixColor('#F4F3EE', '#2A2E32', Math.min(1, saturate + dr * 0.04)),
						opacity: appear * (1 - othersOut),
					}}
				>
					{WORD}
				</div>,
			);
		}
	}

	// palavra central: volta a ser branca quando todo o resto some… e então se desfaz
	const centerColor = mixColor('#F4F3EE', '#2A2E32', saturate * (1 - prog(f, K.still, K.still + 12, E.outQuart)));
	const particles: React.ReactNode[] = [];
	if (f >= K.dissolve) {
		const chars = [...WORD];
		chars.forEach((ch, i) => {
			const r = rng(i * 97 + 3);
			for (let k = 0; k < 14; k++) {
				const delay = r() * 10;
				const t = Math.max(0, f - K.dissolve - delay);
				const ang = r() * Math.PI * 2;
				const sp0 = 2 + r() * 6;
				const dist = sp0 * 12 * (1 - Math.exp(-t / 12));
				const life = 1 - prog(t, 6, 34 + r() * 10, E.inOutSine);
				if (t <= 0 || life <= 0) continue;
				particles.push(
					<div
						key={`${i}:${k}`}
						style={{
							position: 'absolute',
							left: 540 + (i - 3.5) * 66 + Math.cos(ang) * dist,
							top: 960 + Math.sin(ang) * dist * 0.8 - t * 0.6,
							fontFamily: F.mono,
							fontSize: 14 + r() * 10,
							color: C.gray,
							opacity: life * 0.8,
						}}
					>
						{ch}
					</div>,
				);
			}
		});
	}

	return (
		<AbsoluteFill style={{opacity: 1 - out}}>
			{words}
			{f < K.dissolve + 14 && (
				<div
					style={{
						position: 'absolute',
						left: 540,
						top: 960,
						transform: `translate(-50%, -50%) scale(${lerp(1, 0.92, prog(f, K.still, K.dissolve, E.cameraSoft))})`,
						opacity: prog(f, start - 4, start + 4, E.linear),
					}}
				>
					<Chars
						text={WORD}
						style={{fontWeight: 900, fontSize: FS, letterSpacing: '-0.03em', color: centerColor}}
						charStyle={(i) => {
							const d = prog(f, K.dissolve + i * 1.3, K.dissolve + 8 + i * 1.3, E.inQuart);
							return {opacity: 1 - d, filter: d > 0 ? `blur(${d * 10}px)` : undefined, transform: `translateY(${-d * 14}px) scale(${1 - d * 0.4})`};
						}}
					/>
				</div>
			)}
			<div style={{position: 'absolute', left: 540 - 330, top: 960 - 95, width: 660, height: 190}}>
				<OrbitLight f={f} start={K.still + 2} dur={K.dissolve + 6 - (K.still + 2)} w={660} h={190} r={95} laps={1} runners={1} width={3} color={C.gray} outline={0.15} />
			</div>
			{particles}
			<AbsoluteFill style={{alignItems: 'center', top: 880}}>
				<Mono style={{fontSize: 26, opacity: prog(f, K.diferencial - 6, K.diferencial + 10, E.linear), letterSpacing: '0.3em'}}>DEIXA DE SER</Mono>
			</AbsoluteFill>
			<AbsoluteFill style={{alignItems: 'center', top: 930}}>
				<div
					style={{
						fontFamily: F.display,
						fontWeight: 800,
						fontSize: 92,
						color: C.white,
						letterSpacing: `${lerp(0.5, -0.02, prog(f, K.diferencial, K.diferencial + 46, E.outQuart))}em`,
						opacity: prog(f, K.diferencial + 4, K.diferencial + 20, E.linear),
						whiteSpace: 'nowrap',
					}}
				>
					DIFERENCIAL.
				</div>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
