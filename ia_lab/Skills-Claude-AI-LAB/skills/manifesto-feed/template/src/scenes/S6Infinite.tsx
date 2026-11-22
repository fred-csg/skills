import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {CORRIDOR_IMAGES, CORRIDOR_SHARE} from '../data/morphix-assets';
import {C, F} from '../lib/theme';
import {E, clamp, hash, lerp, prog, sp, track} from '../lib/motion';
import {CameraRig, L3} from '../components/CameraRig';
import {MaskReveal, Mono} from '../components/KineticTypography';
import {Thumb} from '../components/FeedCards';
import {K} from '../data/script';
import {OrbitLight, glowAt} from '../components/FX';
import {EMBLEM_Y} from './S5Forces';

// Subdivisão: 1 → 4 → 16 → 64 → 256 (cada vez mais rápida)
const LEVELS = [K.produce, K.produce + 13, K.produce + 25, K.produce + 36, K.produce + 46];
const REGION = {w: 980, h: 1742, cx: 540, cy: 960};
const PUSH = K.produce + 50; // câmera atravessa a grade

const levelRect = (L: number, i: number, j: number) => {
	if (L === 0) {
		const w = 250, h = 444;
		return {x: 540, y: 960 + EMBLEM_Y, w, h};
	}
	const n = 2 ** L;
	const gap = Math.max(4, 22 / L);
	const cw = (REGION.w - gap * (n - 1)) / n;
	const ch = (REGION.h - gap * (n - 1)) / n;
	return {
		x: REGION.cx - REGION.w / 2 + cw / 2 + i * (cw + gap),
		y: REGION.cy - REGION.h / 2 + ch / 2 + j * (ch + gap),
		w: cw,
		h: ch,
	};
};

const Subdivide: React.FC<{f: number}> = ({f}) => {
	let L = 0;
	for (let k = 0; k < LEVELS.length; k++) if (f >= LEVELS[k]) L = k;
	const t = sp(f, LEVELS[L], {damping: 17, stiffness: 190, mass: 0.6});
	const birth = sp(f, K.produce - 2, {damping: 14, stiffness: 150, mass: 0.7});
	const push = prog(f, PUSH, PUSH + 22, E.inExpo);
	const n = 2 ** L;
	const cards: React.ReactNode[] = [];
	for (let i = 0; i < n; i++)
		for (let j = 0; j < n; j++) {
			const to = levelRect(L, i, j);
			const from = L === 0 ? to : levelRect(L - 1, Math.floor(i / 2), Math.floor(j / 2));
			const tt = L === 0 ? 1 : t;
			const x = lerp(from.x, to.x, tt), y = lerp(from.y, to.y, tt);
			const w = lerp(L === 0 ? from.w : from.w, to.w, tt), h = lerp(from.h, to.h, tt);
			const seed = 700 + L * 1000 + i * 37 + j;
			cards.push(
				<div key={`${i}:${j}`} style={{position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, height: h, borderRadius: Math.max(3, 24 / (L + 1)), overflow: 'hidden', background: C.panel2}}>
					<div style={{transform: `scale(${w / 120}, ${h / 213})`, transformOrigin: '0 0'}}>
						<Thumb seed={seed} w={120} h={213} detail={0} accent={hash(seed) > 0.97} />
					</div>
				</div>,
			);
		}
	const scale = lerp(1, 7, push) * lerp(0.2, 1, birth);
	const r0 = levelRect(0, 0, 0);
	// a grade inteira acende por um instante antes da câmera atravessar
	const edge = glowAt(f, PUSH, 8, 6);
	return (
		<AbsoluteFill style={{transform: `scale(${scale})`, transformOrigin: '540px 900px', opacity: 1 - prog(f, PUSH + 8, PUSH + 22, E.linear), filter: push > 0.05 ? `blur(${push * 8}px)` : undefined}}>
			{cards}
			<div style={{position: 'absolute', left: r0.x - r0.w / 2, top: r0.y - r0.h / 2, width: r0.w, height: r0.h}}>
				<OrbitLight f={f} start={K.produce - 8} dur={22} w={r0.w} h={r0.h} r={24} laps={1.6} runners={2} width={5} />
			</div>
			<div style={{position: 'absolute', left: REGION.cx - REGION.w / 2, top: REGION.cy - REGION.h / 2, width: REGION.w, height: REGION.h}}>
				<OrbitLight f={f} start={PUSH - 16} dur={20} w={REGION.w} h={REGION.h} r={12} laps={1} runners={4} width={7} outline={0.5} />
				<div style={{position: 'absolute', inset: 0, boxShadow: `0 0 ${120 * edge}px rgba(244,243,238,${0.4 * edge}), inset 0 0 ${80 * edge}px rgba(244,243,238,${0.25 * edge})`}} />
			</div>
		</AbsoluteFill>
	);
};

// Corredor 3D procedural de conteúdo
const SLICE = 560;
const SLICES = 14;
const LEN = SLICE * SLICES;
const WALLS = [
	{x: -560, y: -380, ry: 72, rx: 0},
	{x: -560, y: 380, ry: 72, rx: 0},
	{x: 560, y: -380, ry: -72, rx: 0},
	{x: 560, y: 380, ry: -72, rx: 0},
	{x: -220, y: 1000, ry: 0, rx: 74},
	{x: 220, y: 1000, ry: 0, rx: 74},
	{x: -220, y: -1000, ry: 0, rx: -74},
	{x: 220, y: -1000, ry: 0, rx: -74},
];

/** posição da câmera ao longo do corredor: acelera e depois desacelera até parar */
export const corridorZ = (f: number) => {
	// integral numérica de uma velocidade suave (determinística)
	const v = (t: number) =>
		track(t, [
			[PUSH, 0],
			[PUSH + 14, 34, E.outQuart],
			[K.massa, 92, E.inOutSine],
			[K.incrivelWall + 6, 70, E.linear],
			[K.still - 6, 0, E.outQuart],
		]);
	let z = 0;
	for (let t = PUSH; t < f; t++) z += v(t);
	return z;
};

const Corridor: React.FC<{f: number}> = ({f}) => {
	const camZ = corridorZ(f);
	const on = prog(f, PUSH + 4, PUSH + 22, E.outQuart);
	const out = prog(f, K.incrivelWall - 2, K.incrivelWall + 14, E.inOutSine);
	const cards: React.ReactNode[] = [];
	for (let s = 0; s < SLICES; s++) {
		for (let w = 0; w < WALLS.length; w++) {
			const wall = WALLS[w];
			let z = -s * SLICE - (w % 2) * (SLICE / 2) + camZ;
			z = ((((z + LEN - 600) % LEN) + LEN) % LEN) - LEN + 600; // repete o corredor infinitamente
			const fog = clamp((z + LEN - 600) / 2400) * clamp((700 - z) / 500);
			if (fog <= 0.01) continue;
			const id = s * 8 + w + Math.floor((-s * SLICE + camZ) / LEN) * 1000;
			const seed = 3000 + id * 13;
			const labelAt = K.incrivelWall + hash(id + 5) * 26 - 8;
			const lab = prog(f, labelAt, labelAt + 8, E.outExpo);
			cards.push(
				<L3 key={`${s}:${w}`} x={wall.x} y={wall.y} z={z} ry={wall.ry} rx={wall.rx} w={340} h={600} opacity={fog * on}>
					<div style={{width: 340, height: 600, borderRadius: 26, overflow: 'hidden', position: 'relative', background: C.panel2}}>
						{CORRIDOR_IMAGES.length > 0 && hash(id + 99) < CORRIDOR_SHARE ? (
							<Img src={staticFile(`morphix/${CORRIDOR_IMAGES[Math.floor(hash(id + 7) * CORRIDOR_IMAGES.length)]}`)} style={{width: 340, height: 600, objectFit: 'cover', display: 'block'}} />
						) : (
							<div style={{opacity: CORRIDOR_IMAGES.length ? 0.45 : 1}}>
								<Thumb seed={seed} w={340} h={600} accent={hash(seed) > 0.93} />
							</div>
						)}
						{lab > 0 && (
							<div style={{position: 'absolute', inset: 0, background: `rgba(11,12,13,${0.8 * lab})`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
								<div style={{fontFamily: F.display, fontWeight: 900, fontSize: 64, letterSpacing: '-0.03em', color: C.white, transform: `scale(${lerp(1.6, 1, lab)})`, opacity: lab}}>INCRÍVEL</div>
							</div>
						)}
					</div>
				</L3>,
			);
		}
	}
	return (
		<AbsoluteFill style={{opacity: 1 - out}}>
			<CameraRig cam={{perspective: 900, rz: Math.sin(f / 40) * 1.2, x: Math.sin(f / 33) * 30}}>{cards}</CameraRig>
		</AbsoluteFill>
	);
};

export const S6Infinite: React.FC<{f: number}> = ({f}) => {
	const mult = ['×1', '×4', '×16', '×64', '×256'];
	let L = 0;
	for (let k = 0; k < LEVELS.length; k++) if (f >= LEVELS[k]) L = k;
	const textOut = K.massa + 22;
	return (
		<AbsoluteFill>
			{f < PUSH + 24 && <Subdivide f={f} />}
			{f >= PUSH && <Corridor f={f} />}
			{f < PUSH + 10 && (
				<AbsoluteFill style={{top: 1700, alignItems: 'center'}}>
					<Mono style={{color: C.white, fontSize: 28}}>{mult[L]}</Mono>
				</AbsoluteFill>
			)}
			<AbsoluteFill
				style={{
					background: 'radial-gradient(ellipse 80% 26% at 50% 50%, rgba(11,12,13,0.94) 0%, rgba(11,12,13,0.6) 55%, rgba(11,12,13,0) 100%)',
					opacity: prog(f, K.incriveis - 10, K.incriveis, E.linear) * (1 - prog(f, textOut, textOut + 10, E.linear)),
				}}
			/>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
				<div style={{transform: 'translateY(-60px)'}}>
					<MaskReveal text="VÍDEOS INCRÍVEIS" f={f} start={K.incriveis - 8} stagger={1} out={textOut} style={{fontWeight: 900, fontSize: 96, letterSpacing: '-0.035em', textShadow: `0 0 ${20 + 40 * glowAt(f, K.incriveis + 6, 6, 24)}px rgba(244,243,238,0.4)`}} />
				</div>
				<div style={{transform: 'translateY(30px)'}}>
					<MaskReveal text="EM MASSA" f={f} start={K.massa - 8} stagger={1.4} out={textOut + 2} from="top" style={{fontWeight: 900, fontSize: 96, letterSpacing: '-0.035em', color: C.gray}} />
				</div>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
