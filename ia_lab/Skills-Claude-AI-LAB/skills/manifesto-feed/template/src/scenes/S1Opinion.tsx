import React from 'react';
import {C, F} from '../lib/theme';
import {E, SPR, clamp, kick, lerp, noise, prog, sp, track} from '../lib/motion';
import {CameraRig, L3} from '../components/CameraRig';
import {Mono, WordStagger} from '../components/KineticTypography';
import {K} from '../data/script';
import {OrbitLight, glowAt} from '../components/FX';
import {COMMENT_SLOTS, PITCH_X, PITCH_Y, TILE_H, TILE_W, s2Center, s2Zoom} from './shared';

const COMMENTS = [
	{handle: '@cetico.digital', time: '2 min', text: 'A IA ainda não é realista.', key: 'realista', keyAt: K.realista, likes: 1284},
	{handle: '@producao.classica', time: '48 s', text: 'Vídeo com IA custa uma fortuna.', key: 'fortuna', keyAt: K.fortuna, likes: 932},
	{handle: '@medo_do_futuro', time: 'agora', text: 'Vai roubar todos os empregos.', key: 'empregos', keyAt: K.empregos, likes: 4107},
];

/** Palavra-chave: um bloco branco varre por trás e inverte o texto. */
const KeyWord: React.FC<{word: string; f: number; at: number}> = ({word, f, at}) => {
	const wipe = prog(f, at, at + 9, E.outExpo);
	const core = word.replace(/[.,]/g, '');
	const tail = word.slice(core.length);
	// a palavra "se levanta" letra a letra; o bloco branco revela a versão invertida por recorte
	const letters = (color: string) =>
		[...core.toUpperCase()].map((ch, i) => {
			const p = prog(f, at + 2 + i * 1.2, at + 12 + i * 1.2, E.overshoot);
			return (
				<span key={i} style={{display: 'inline-block', color, transform: `translateY(${(1 - p) * -0.16}em)`}}>
					{ch}
				</span>
			);
		});
	const clip = `inset(0 ${(1 - wipe) * 100}% 0 0)`;
	return (
		<span style={{position: 'relative', display: 'inline-block'}}>
			<span style={{position: 'relative'}}>{letters(C.white)}</span>
			<span style={{position: 'absolute', left: '-0.08em', right: '-0.08em', top: '0.06em', bottom: '0.02em', clipPath: clip}}>
				<span style={{position: 'absolute', inset: 0, background: C.white}} />
				<span style={{position: 'absolute', left: '0.08em', top: '-0.06em', whiteSpace: 'pre'}}>{letters(C.bg)}</span>
			</span>
			{tail}
		</span>
	);
};

const Heart: React.FC<{fill: string}> = ({fill}) => (
	<svg width="26" height="24" viewBox="0 0 26 24">
		<path d="M13 22 C2 14 1 9 3 5 C5 1 10 1 13 5 C16 1 21 1 23 5 C25 9 24 14 13 22Z" fill={fill} />
	</svg>
);

const CommentCard: React.FC<{i: number; f: number; enter: number; contentOpacity: number; glow?: number}> = ({i, f, enter, contentOpacity, glow = 0}) => {
	const c = COMMENTS[i];
	const likes = Math.round(c.likes * prog(f, enter, enter + 70, E.outQuart));
	const liked = f >= c.keyAt + 6;
	const heartPop = 1 + kick(f, c.keyAt + 6, 0.35, 0.7, 0.25);
	return (
		<div
			style={{
				width: TILE_W,
				height: TILE_H,
				borderRadius: 34,
				background: C.panel,
				boxShadow: `inset 0 0 0 ${1.5 + glow * 1.5}px rgba(244,243,238,${0.09 + glow * 0.5}), 0 0 ${70 * glow}px rgba(244,243,238,${0.32 * glow}), 0 40px 90px rgba(0,0,0,0.6)`,
				padding: '36px 42px',
				boxSizing: 'border-box',
				position: 'relative',
				overflow: 'hidden',
			}}
		>
			<div style={{opacity: contentOpacity}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 18, marginBottom: 20}}>
					<div style={{width: 54, height: 54, borderRadius: 99, background: `linear-gradient(135deg, #5E656C, ${C.struct})`}} />
					<Mono style={{fontSize: 23, color: C.white, opacity: 0.8, letterSpacing: '0.04em', textTransform: 'none'}}>{c.handle}</Mono>
					<Mono style={{fontSize: 21, letterSpacing: '0.04em', textTransform: 'none'}}>· {c.time}</Mono>
				</div>
				<WordStagger
					text={c.text}
					f={f}
					start={enter + 3}
					stagger={2}
					highlight={c.key}
					renderHighlight={(w) => <KeyWord word={w} f={f} at={c.keyAt} />}
					style={{fontFamily: F.display, fontWeight: 800, fontSize: 60, lineHeight: 1.04, color: C.white, letterSpacing: '-0.025em'}}
				/>
				<div style={{position: 'absolute', left: 42, bottom: 30, display: 'flex', alignItems: 'center', gap: 12}}>
					<div style={{transform: `scale(${heartPop})`, display: 'flex'}}>
						<Heart fill={liked ? C.white : C.struct} />
					</div>
					<Mono style={{fontSize: 22, color: liked ? C.white : C.gray, letterSpacing: '0.06em'}}>{likes.toLocaleString('pt-BR')}</Mono>
				</div>
			</div>
		</div>
	);
};

/** pose de um comentário em função do "nível" de profundidade (0 = frente) */
const pose = (lvl: number, i: number) => ({
	x: lerp(0, i === 0 ? -70 : 60, Math.min(1, lvl)) + (lvl > 1 ? (lvl - 1) * -40 : 0),
	y: 230 - 390 * lvl,
	z: -430 * lvl,
	rz: (i % 2 ? 1.6 : -1.8) * Math.min(1, lvl),
	ry: (i % 2 ? -7 : 8) * Math.min(1, lvl),
});

export const S1Opinion: React.FC<{f: number}> = ({f}) => {
	// entradas
	const e1 = sp(f, -6, SPR.ui); // já em movimento no frame 0 (sem fade-in)
	const e2 = sp(f, K.card2, {damping: 18, stiffness: 260, mass: 0.6});
	const e3 = sp(f, K.card3, SPR.elastic);
	// empurrões em profundidade quando o próximo chega
	const push2 = sp(f, K.card2 + 4, SPR.heavy);
	const push3 = sp(f, K.card3 + 5, SPR.heavy);
	const lvls = [push2 + push3, push3, 0];

	// recuo: cada card encaixa no slot da grade
	const tFlat = prog(f, K.recoil, K.recoil + 18, E.outQuart);
	const zoom2 = s2Zoom(f);
	const c2 = s2Center(f);
	const contentOpacity = 1 - prog(f, K.recoil + 8, K.recoil + 22, E.linear);

	// câmera da cena 1: deriva orgânica + avanço a cada comentário
	const drift = f / 45;
	const camS1 = {
		x: noise(drift, 3) * 26,
		y: track(f, [
			[0, 230],
			[K.card2 + 4, 40, E.cameraSoft],
			[K.card3 + 5, -150, E.cameraSoft],
		]),
		z: track(f, [
			[0, -160],
			[K.card2 - 2, 0, E.camera],
			[K.card3 - 2, 60, E.camera],
			[K.recoil, 120, E.cameraSoft],
		]),
		ry: noise(drift, 9) * 4 + track(f, [[0, 0], [K.card2, -3], [K.card3, 2.5]]),
		rx: noise(drift, 5) * 2 + 3,
		rz: kick(f, K.card2 + 6, 0.6) + kick(f, K.card3 + 8, -0.5),
	};
	// a câmera da cena 2 assume o controle no recuo (antecipação: recua 1 tique antes)
	const anticip = kick(f, K.recoil - 4, 0.05, 0.5, 0.35);
	const cam = {
		x: lerp(camS1.x, c2.x, tFlat),
		y: lerp(camS1.y, c2.y, tFlat),
		z: lerp(camS1.z, 0, tFlat),
		rx: lerp(camS1.rx, 0, tFlat),
		ry: lerp(camS1.ry, 0, tFlat),
		rz: lerp(camS1.rz, 0, tFlat),
		zoom: (f < K.recoil ? 1 + anticip : zoom2),
		perspective: 1500,
	};

	const enters = [e1, e2, e3];
	const enterFrames = [-6, K.card2, K.card3];

	return (
		<CameraRig cam={cam}>
			{[0, 1, 2].map((i) => {
				const e = enters[i];
				if (e <= 0.001 && i > 0) return null;
				const p = pose(lvls[i], i);
				// deslocamentos de entrada
				const off =
					i === 0
						? {x: 0, y: (1 - e) * 80, z: (1 - e) * -200, rx: (1 - e) * 24, ry: 0}
						: i === 1
							? {x: (1 - e) * 1250, y: (1 - e) * -40, z: 0, rx: 0, ry: (1 - e) * -40}
							: {x: 0, y: (1 - e) * 1300, z: 0, rx: (1 - e) * -30, ry: 0};
				const react = i === 0 ? kick(f, K.card2 + 5, 2.4) : i === 1 ? kick(f, K.card3 + 6, -2.2) : 0;
				const slot = COMMENT_SLOTS[i];
				const flat = {x: slot[0] * PITCH_X, y: slot[1] * PITCH_Y};
				const x = lerp(p.x + off.x, flat.x, tFlat);
				const y = lerp(p.y + off.y, flat.y, tFlat);
				const z = lerp(p.z + off.z, 0, tFlat);
				const blurV = i === 1 ? clamp((1 - e) * 2.2) * 10 : 0;
				return (
					<L3
						key={i}
						x={x}
						y={y}
						z={z}
						rx={lerp(off.rx, 0, tFlat)}
						ry={lerp(p.ry + off.ry, 0, tFlat)}
						rz={lerp(p.rz + react, 0, tFlat)}
						w={TILE_W}
						h={TILE_H}
						opacity={i === 0 ? clamp(e * 3) : 1}
						style={{filter: blurV > 0.3 ? `blur(${blurV}px)` : undefined}}
					>
						<CommentCard
							i={i}
							f={f}
							enter={Math.max(0, enterFrames[i])}
							contentOpacity={contentOpacity}
							glow={Math.max(glowAt(f, K.recoil + 2, 24, 14), i === 1 ? glowAt(f, K.card2 + 6, 4, 14) * 0.7 : 0, i === 2 ? glowAt(f, K.card3 + 8, 4, 14) * 0.7 : 0)}
						/>
						{/* luzes que circulam o card antes do recuo/morph (e na chegada de cada comentário) */}
						<OrbitLight f={f} start={K.recoil - 26} dur={32} w={TILE_W} h={TILE_H} r={34} laps={1.5} runners={2} />
						{i === 1 && <OrbitLight f={f} start={K.card2 + 4} dur={18} w={TILE_W} h={TILE_H} r={34} laps={0.9} runners={1} outline={0.2} />}
						{i === 2 && <OrbitLight f={f} start={K.card3 + 6} dur={18} w={TILE_W} h={TILE_H} r={34} laps={0.9} runners={1} outline={0.2} />}
					</L3>
				);
			})}
		</CameraRig>
	);
};
