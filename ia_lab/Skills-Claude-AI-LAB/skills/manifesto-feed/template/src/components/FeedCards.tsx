import React from 'react';
import {Img, staticFile} from 'remotion';
import {C} from '../lib/theme';
import {rng} from '../lib/motion';

const TONES = ['#1D2023', '#24282C', '#2E3237', '#3A3F45', '#4A5057', '#5E656C', '#8B9095', '#C9C8C2'];

/** Thumbnail abstrata procedural (determinística pelo seed). */
export const Thumb: React.FC<{seed: number; w: number; h: number; accent?: boolean; detail?: number}> = ({
	seed,
	w,
	h,
	accent,
	detail = 1,
}) => {
	const r = rng(seed);
	const kind = Math.floor(r() * 5);
	const t = (k: number) => TONES[Math.floor(r() * TONES.length * k) % TONES.length];
	const bgA = t(0.5);
	const bgB = t(0.9);
	const id = `t${seed}`;
	const ang = Math.floor(r() * 360);
	const shapes: React.ReactNode[] = [];
	if (kind === 0) {
		// horizonte + sol
		const hy = h * (0.45 + r() * 0.25);
		shapes.push(<rect key="h" x={0} y={hy} width={w} height={h - hy} fill={t(1)} />);
		shapes.push(<circle key="s" cx={w * (0.3 + r() * 0.4)} cy={hy - h * 0.12} r={w * (0.12 + r() * 0.12)} fill={accent ? C.orange : '#C9C8C2'} opacity={0.9} />);
	} else if (kind === 1) {
		// blocos editoriais
		for (let i = 0; i < 3 + detail * 2; i++)
			shapes.push(<rect key={i} x={r() * w * 0.6} y={r() * h * 0.8} width={w * (0.2 + r() * 0.5)} height={h * (0.05 + r() * 0.2)} fill={t(1)} rx={6} />);
	} else if (kind === 2) {
		// anéis concêntricos
		const cx = w * (0.3 + r() * 0.4), cy = h * (0.3 + r() * 0.4);
		for (let i = 5; i > 0; i--) shapes.push(<circle key={i} cx={cx} cy={cy} r={i * w * 0.11} fill={i % 2 ? t(1) : bgA} />);
	} else if (kind === 3) {
		// figura (retrato abstrato)
		const cx = w * 0.5;
		shapes.push(<ellipse key="b" cx={cx} cy={h * 0.95} rx={w * 0.42} ry={h * 0.3} fill={t(1)} />);
		shapes.push(<circle key="c" cx={cx} cy={h * 0.48} r={w * 0.17} fill={t(1)} />);
	} else {
		// diagonais
		for (let i = 0; i < 4; i++)
			shapes.push(<polygon key={i} points={`${r() * w},0 ${w},${r() * h} ${r() * w},${h} 0,${r() * h}`} fill={t(1)} opacity={0.6} />);
	}
	return (
		<svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} style={{display: 'block'}}>
			<defs>
				<linearGradient id={id} gradientTransform={`rotate(${ang} .5 .5)`}>
					<stop offset="0" stopColor={bgA} />
					<stop offset="1" stopColor={bgB} />
				</linearGradient>
			</defs>
			<rect width={w} height={h} fill={`url(#${id})`} />
			{shapes}
		</svg>
	);
};

/** Card de vídeo vertical estilizado (sem copiar Instagram/TikTok). */
export const FeedCard: React.FC<{
	seed: number;
	w?: number;
	h?: number;
	progress?: number; // barra de duração 0..1
	accent?: boolean;
	image?: string | null; // asset em public/ (substitui a thumbnail procedural)
	radius?: number;
	meta?: boolean;
	style?: React.CSSProperties;
	children?: React.ReactNode;
}> = ({seed, w = 600, h = 1000, progress = 0.35, accent, image, radius = 34, meta = true, style, children}) => {
	const r = rng(seed + 77);
	const s = w / 600;
	return (
		<div
			style={{
				width: w,
				height: h,
				borderRadius: radius * s,
				overflow: 'hidden',
				position: 'relative',
				background: C.panel,
				boxShadow: `0 ${30 * s}px ${80 * s}px rgba(0,0,0,0.55), inset 0 0 0 ${Math.max(1, 1.5 * s)}px rgba(244,243,238,0.08)`,
				...style,
			}}
		>
			{image ? <Img src={staticFile(image)} style={{width: w, height: h, objectFit: 'cover', display: 'block'}} /> : <Thumb seed={seed} w={w} h={h} accent={accent} />}
			<div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(11,12,13,0) 55%, rgba(11,12,13,0.85) 100%)'}} />
			{meta && (
				<div style={{position: 'absolute', left: 36 * s, right: 36 * s, bottom: 40 * s}}>
					<div style={{display: 'flex', alignItems: 'center', gap: 16 * s, marginBottom: 22 * s}}>
						<div style={{width: 52 * s, height: 52 * s, borderRadius: 99, background: '#5E656C'}} />
						<div style={{height: 14 * s, width: (140 + r() * 120) * s, borderRadius: 8, background: 'rgba(244,243,238,0.75)'}} />
					</div>
					<div style={{height: 12 * s, width: `${70 + r() * 25}%`, borderRadius: 8, background: 'rgba(244,243,238,0.35)', marginBottom: 12 * s}} />
					<div style={{height: 12 * s, width: `${35 + r() * 25}%`, borderRadius: 8, background: 'rgba(244,243,238,0.25)', marginBottom: 30 * s}} />
					<div style={{height: 5 * s, borderRadius: 4, background: 'rgba(244,243,238,0.18)'}}>
						<div style={{height: '100%', width: `${progress * 100}%`, borderRadius: 4, background: accent ? C.orange : C.white}} />
					</div>
				</div>
			)}
			{children}
		</div>
	);
};
