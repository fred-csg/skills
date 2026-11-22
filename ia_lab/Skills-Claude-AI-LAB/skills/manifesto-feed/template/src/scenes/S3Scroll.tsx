import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, F} from '../lib/theme';
import {E, SPR, clamp, hash, lerp, noise, prog, sp, track} from '../lib/motion';
import {CameraRig, L3} from '../components/CameraRig';
import {Chars, Mono} from '../components/KineticTypography';
import {FeedCard} from '../components/FeedCards';
import {K} from '../data/script';
import {CORRIDOR_IMAGES, FEED_IMAGES} from '../data/morphix-assets';
import {OrbitLight, glowAt} from '../components/FX';
import {FEED_CARD} from './shared';

const PITCH = 1130;
const SIDE_X = 760;

/** palavra com interpretação visual própria */
const Word: React.FC<{f: number}> = ({f}) => {
	const glow = Math.max(glowAt(f, K.consumir + 12, 8, 20), glowAt(f, K.deslizar + 8, 6, 20), glowAt(f, K.esquecer + 6, 6, 16));
	const base: React.CSSProperties = {fontFamily: F.display, fontWeight: 900, fontSize: 158, letterSpacing: '-0.04em', lineHeight: 1, textShadow: `0 0 ${18 + 50 * glow}px rgba(244,243,238,${0.18 + 0.4 * glow})`};
	const swipe = sp(f, K.deslizar - 2, {damping: 20, stiffness: 140, mass: 0.8});
	const nodes: React.ReactNode[] = [];
	// CONSUMIR: letras convergem para o centro
	if (f >= K.consumir - 4 && f < K.deslizar + 16) {
		const n = 8;
		nodes.push(
			<div key="c" style={{position: 'absolute', transform: `translateX(${-swipe * 900}px) skewX(${swipe * 14}deg)`, filter: `blur(${clamp(swipe * (1 - swipe) * 4) * 14}px)`}}>
				<Chars
					text="CONSUMIR"
					style={base}
					charStyle={(i) => {
						const p = prog(f, K.consumir - 4 + Math.abs(i - (n - 1) / 2) * 1.2, K.consumir + 14 + Math.abs(i - (n - 1) / 2) * 1.2, E.outExpo);
						const spread = (i - (n - 1) / 2) * 120;
						return {transform: `translate(${spread * (1 - p)}px, ${(hash(i + 3) - 0.5) * 260 * (1 - p)}px) scale(${lerp(0.4, 1, p)})`, opacity: p};
					}}
				/>
			</div>,
		);
	}
	// DESLIZAR: chega com o swipe da composição inteira
	if (f >= K.deslizar - 2 && f < K.esquecer + 6) {
		const out = prog(f, K.esquecer - 6, K.esquecer + 4, E.inQuart);
		nodes.push(
			<div
				key="d"
				style={{
					position: 'absolute',
					transform: `translateX(${(1 - swipe) * 900}px) skewX(${(1 - swipe) * -16}deg)`,
					filter: `blur(${clamp((1 - swipe) * 2) * 12}px)`,
					opacity: 1 - out,
				}}
			>
				<Chars text="DESLIZAR" style={base} charStyle={(i) => ({transform: `translateX(${(1 - swipe) * i * 30}px)`})} />
			</div>,
		);
	}
	// ESQUECER: aparece nítida e perde foco letra por letra
	if (f >= K.esquecer - 4) {
		nodes.push(
			<div key="e" style={{position: 'absolute'}}>
				<Chars
					text="ESQUECER"
					style={base}
					charStyle={(i) => {
						const pin = prog(f, K.esquecer - 4 + i * 0.8, K.esquecer + 8 + i * 0.8, E.outExpo);
						const order = hash(i + 41);
						const fade = prog(f, K.esquecer + 14 + order * 16, K.esquecer + 34 + order * 16, E.inOutSine);
						return {
							opacity: pin * (1 - fade * 0.94),
							filter: `blur(${fade * 16}px)`,
							transform: `translateY(${(1 - pin) * 40 - fade * 30}px)`,
						};
					}}
				/>
			</div>,
		);
	}
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', top: 1560 - 960}}>
			{nodes}
		</AbsoluteFill>
	);
};

// laterais: alternam a 6ª imagem do feed com imagens do corredor (prévia do que vem)
const sideImage = (k: number, side: number) => {
	const pool = [...FEED_IMAGES.slice(5), ...CORRIDOR_IMAGES];
	if (!pool.length) return null;
	return `morphix/${pool[(((k + 1) * 2 + (side > 0 ? 1 : 0)) * 3) % pool.length]}`;
};

export const S3Scroll: React.FC<{f: number}> = ({f}) => {
	// pull-back que revela o feed; depois cada gesto rola com inércia
	const zoom = track(f, [
		[K.diveIn + 26, 1],
		[K.diveIn + 56, 0.6, E.camera],
		[K.consumir, 0.58, E.linear],
		[K.consumir + 12, 0.64, E.outExpo],
		[K.esquecer, 0.62, E.cameraSoft],
		[K.toBelt + 12, 0.5, E.camera],
	]);
	const g1 = sp(f, K.diveIn + 40, {damping: 24, stiffness: 70, mass: 1.1}); // rolagem lenta inicial (consumo passivo)
	const g2 = sp(f, K.deslizar - 2, {damping: 20, stiffness: 140, mass: 0.8});
	const scroll = (g1 * 0.12 * (1 - g2) + g2) * PITCH;
	const sideLag = (g1 * 0.16 + sp(f, K.deslizar + 2, {damping: 18, stiffness: 110, mass: 0.9})) * PITCH;
	const sideLead = (g1 * 0.1 + sp(f, K.deslizar - 5, {damping: 22, stiffness: 170, mass: 0.7})) * PITCH;

	// CONSUMIR: laterais convergem para o card central
	const conv = prog(f, K.consumir - 2, K.consumir + 16, E.inOutSine) * (1 - prog(f, K.deslizar - 6, K.deslizar + 10, E.outQuart));
	const absorb = 1 + Math.sin(prog(f, K.consumir + 6, K.consumir + 26, E.linear) * Math.PI) * 0.05;

	// ESQUECER: o card em foco perde nitidez
	const forget = prog(f, K.esquecer + 2, K.esquecer + 26, E.inOutSine);

	// passagem para a esteira (cena 4): o feed deita
	const tilt = prog(f, K.toBelt - 4, K.toBelt + 12, E.inQuart);
	const fadeAll = 1 - prog(f, K.toBelt + 2, K.toBelt + 12, E.linear);

	const cam = {
		x: noise(f / 50, 2) * 20,
		y: (960 - FEED_CARD.cy) / zoom + scroll,
		zoom,
		rx: tilt * 58 + noise(f / 40, 4) * 1.5,
		ry: noise(f / 55, 6) * 3,
		perspective: 1600,
	};
	const intro = prog(f, K.diveIn + 30, K.diveIn + 54, E.outQuart);
	const items: React.ReactNode[] = [];
	for (let k = -1; k <= 3; k++) {
		const focus = k === 1 ? forget : 0;
		items.push(
			<L3 key={`m${k}`} x={0} y={k * PITCH} z={0} s={k === 0 ? absorb : 1} w={FEED_CARD.w} h={FEED_CARD.h} opacity={(k === 0 ? 1 : intro) * (1 - focus * 0.75)} style={{filter: focus > 0.01 ? `blur(${focus * 22}px) grayscale(${focus})` : undefined}}>
				<FeedCard seed={3 + k * 11} image={FEED_IMAGES.length ? `morphix/${FEED_IMAGES[(k + 5) % 5 === 4 ? 4 : k]}` : null} w={FEED_CARD.w} h={FEED_CARD.h} progress={k === 0 ? clamp((f - 270) / 80) : 0.2 + hash(k) * 0.6} />
			</L3>,
		);
		for (const side of [-1, 1]) {
			const off = side < 0 ? sideLag - scroll : sideLead - scroll;
			const cx = side * SIDE_X * (1 - conv * 0.85);
			const yy = k * PITCH + 380 * side - off + conv * (0 - (k * PITCH + 380 * side - off)) * 0.6;
			items.push(
				<L3 key={`s${side}${k}`} x={cx} y={yy} z={-340 - conv * 200} s={1 - conv * 0.55} w={FEED_CARD.w} h={FEED_CARD.h} opacity={intro * (1 - conv * 0.7) * 0.75}>
					<FeedCard seed={50 + k * 7 + side * 3} image={sideImage(k, side)} w={FEED_CARD.w} h={FEED_CARD.h} progress={hash(k + side * 9)} />
				</L3>,
			);
		}
	}

	// luzes circulando o card em foco: na absorção (CONSUMIR), na chegada (DESLIZAR) e antes de deitar na esteira
	items.push(
		<L3 key="o0" x={0} y={0} w={FEED_CARD.w} h={FEED_CARD.h} s={absorb}>
			<OrbitLight f={f} start={K.consumir - 6} dur={28} w={FEED_CARD.w} h={FEED_CARD.h} r={34} laps={1.4} runners={2} width={6} />
		</L3>,
		<L3 key="o1" x={0} y={PITCH} w={FEED_CARD.w} h={FEED_CARD.h}>
			<OrbitLight f={f} start={K.deslizar + 6} dur={20} w={FEED_CARD.w} h={FEED_CARD.h} r={34} laps={1} runners={1} width={6} />
			<OrbitLight f={f} start={K.toBelt - 22} dur={26} w={FEED_CARD.w} h={FEED_CARD.h} r={34} laps={1.6} runners={3} width={6} />
		</L3>,
	);

	return (
		<AbsoluteFill style={{opacity: fadeAll}}>
			<CameraRig cam={cam}>{items}</CameraRig>
			<AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(11,12,13,0) 62%, rgba(11,12,13,0.9) 76%, rgba(11,12,13,0.9) 88%, rgba(11,12,13,0) 100%)', opacity: intro}} />
			<AbsoluteFill style={{alignItems: 'center', top: 1400}}>
				<Mono style={{opacity: prog(f, K.consumir - 26, K.consumir - 12, E.linear) * (1 - prog(f, K.toBelt - 6, K.toBelt + 4, E.linear))}}>
					A INTERNET NOS TREINOU PARA
				</Mono>
			</AbsoluteFill>
			<Word f={f} />
		</AbsoluteFill>
	);
};
