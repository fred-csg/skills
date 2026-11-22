import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C} from '../lib/theme';
import {E, clamp, prog} from '../lib/motion';

/**
 * Luz que percorre o contorno de um elemento (retângulo arredondado ou círculo),
 * com rastro de cometa e glow. Anuncia o objeto que vai se transformar.
 * Coordenadas locais: ocupa uma caixa w×h a partir de (0,0) do pai.
 */
export const OrbitLight: React.FC<{
	f: number;
	start: number;
	dur: number;
	w: number;
	h: number;
	r?: number;
	circle?: boolean;
	color?: string;
	laps?: number;
	runners?: number; // quantas luzes ao mesmo tempo
	width?: number;
	pad?: number;
	outline?: number; // contorno aceso por baixo (0..1)
}> = ({f, start, dur, w, h, r = 30, circle, color = C.white, laps = 1.2, runners = 2, width = 5, pad = 6, outline = 0.35}) => {
	const id = `orb${React.useId().replace(/[^a-zA-Z0-9]/g, '')}`;
	if (f < start || f > start + dur) return null;
	const t = (f - start) / dur;
	const env = Math.min(prog(f, start, start + 5, E.linear), 1 - prog(f, start + dur - 8, start + dur, E.linear));
	const W = w + pad * 2;
	const H = h + pad * 2;
	const d = circle
		? `M ${W / 2} ${pad} A ${w / 2} ${h / 2} 0 1 1 ${W / 2 - 0.01} ${pad}`
		: `M ${pad + r} ${pad} H ${pad + w - r} A ${r} ${r} 0 0 1 ${pad + w} ${pad + r} V ${pad + h - r} A ${r} ${r} 0 0 1 ${pad + w - r} ${pad + h} H ${pad + r} A ${r} ${r} 0 0 1 ${pad} ${pad + h - r} V ${pad + r} A ${r} ${r} 0 0 1 ${pad + r} ${pad}`;
	const head = E.inOutSine(t) * laps;
	const TRAIL = 9;
	const seg = 0.012;
	return (
		<svg width={W} height={H} style={{position: 'absolute', left: -pad, top: -pad, overflow: 'visible', pointerEvents: 'none'}}>
			<defs>
				<filter id={id} x="-50%" y="-50%" width="200%" height="200%">
					<feGaussianBlur stdDeviation={width * 1.6} result="b" />
					<feMerge>
						<feMergeNode in="b" />
						<feMergeNode in="b" />
						<feMergeNode in="SourceGraphic" />
					</feMerge>
				</filter>
			</defs>
			<path d={d} fill="none" stroke={color} strokeWidth={1.5} opacity={outline * env * (0.4 + 0.6 * Math.sin(t * Math.PI))} pathLength={1} />
			<g filter={`url(#${id})`} opacity={env}>
				{Array.from({length: runners}).map((_, ri) =>
					Array.from({length: TRAIL}).map((__, k) => {
						const pos = (((head + ri / runners - k * seg * 1.3) % 1) + 1) % 1;
						return (
							<path
								key={`${ri}:${k}`}
								d={d}
								fill="none"
								stroke={k === 0 ? '#FFFFFF' : color}
								strokeWidth={width * (1 - k / TRAIL) + 0.5}
								strokeLinecap="round"
								pathLength={1}
								strokeDasharray={`${seg} ${1 - seg}`}
								strokeDashoffset={-pos}
								opacity={(1 - k / TRAIL) ** 1.6}
							/>
						);
					}),
				)}
			</g>
		</svg>
	);
};

/** intensidade de um pulso de glow (0..1) em torno de um frame */
export const glowAt = (f: number, at: number, before = 10, after = 16) =>
	Math.min(prog(f, at - before, at, E.inQuart), 1 - prog(f, at, at + after, E.outQuart));

export type FlashEvent = {at: number; amp: number; color?: string; double?: boolean};

/** Flash piscante nas transições: dois pulsos rápidos + bloom radial (blend screen). */
export const Flashes: React.FC<{f: number; events: FlashEvent[]}> = ({f, events}) => {
	let v = 0;
	let color = C.white;
	for (const e of events) {
		const t = f - e.at;
		if (t < -2 || t > 14) continue;
		const p1 = Math.exp(-((t - 0) ** 2) / 2.2);
		const p2 = e.double === false ? 0 : 0.6 * Math.exp(-((t - 4) ** 2) / 1.6);
		const tail = t > 0 ? 0.25 * Math.exp(-t / 5) : 0;
		const val = e.amp * clamp(p1 + p2 + tail);
		if (val > v) {
			v = val;
			color = e.color ?? C.white;
		}
	}
	if (v < 0.005) return null;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'screen'}}>
			<AbsoluteFill style={{background: `radial-gradient(ellipse 75% 55% at 50% 50%, ${color} 0%, rgba(0,0,0,0) 70%)`, opacity: v}} />
			<AbsoluteFill style={{background: color, opacity: v * 0.35}} />
		</AbsoluteFill>
	);
};
