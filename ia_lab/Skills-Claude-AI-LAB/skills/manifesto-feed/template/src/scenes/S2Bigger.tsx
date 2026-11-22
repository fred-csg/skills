import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, F} from '../lib/theme';
import {E, SPR, clamp, hash, lerp, prog, sp} from '../lib/motion';
import {Chars, MaskReveal} from '../components/KineticTypography';
import {Thumb} from '../components/FeedCards';
import {K} from '../data/script';
import {FEED_IMAGES} from '../data/morphix-assets';
import {Img, staticFile} from 'remotion';
import {OrbitLight, glowAt} from '../components/FX';
import {COMMENT_SLOTS, DIVE_SLOT, FEED_CARD, PITCH_X, PITCH_Y, TILE_H, TILE_W, s2Center, s2Zoom} from './shared';

const isComment = (c: number, r: number) => COMMENT_SLOTS.some(([a, b]) => a === c && b === r);

/** O sistema: centenas de elementos organizados, revelados pelo recuo da câmera. */
export const S2Bigger: React.FC<{f: number}> = ({f}) => {
	const zoom = s2Zoom(f);
	const {x: cx, y: cy} = s2Center(f);
	const tw = TILE_W * zoom;
	const th = TILE_H * zoom;
	// raio de revelação (em tiles) cresce com o recuo: o sistema "acende" do centro para fora
	const reveal = lerp(0, 46, prog(f, K.recoil + 2, K.maior + 20, E.outQuart));
	const dive = prog(f, K.diveIn, K.diveIn + 24, E.inExpo);

	const cols = Math.ceil(540 / (PITCH_X * zoom)) + 2;
	const rows = Math.ceil(960 / (PITCH_Y * zoom)) + 2;
	const c0 = Math.round(cx / PITCH_X);
	const r0 = Math.round(cy / PITCH_Y);

	const rects: React.ReactNode[] = [];
	for (let c = c0 - cols; c <= c0 + cols; c++) {
		for (let r = r0 - rows; r <= r0 + rows; r++) {
			const sx = 540 + (c * PITCH_X - cx) * zoom - tw / 2;
			const sy = 960 + (r * PITCH_Y - cy) * zoom - th / 2;
			if (sx > 1080 || sy > 1920 || sx + tw < 0 || sy + th < 0) continue;
			const d = Math.hypot(c * 1.6, r);
			const h = hash(c * 131 + r * 7 + 1000);
			const vis = clamp((reveal - d) / 3 + h * 0.4);
			const comment = isComment(c, r);
			if (comment && f < 186) continue; // a cena 1 ainda desenha os comentários
			if (vis <= 0 && !comment) continue;
			const isDive = c === DIVE_SLOT[0] && r === DIVE_SLOT[1];
			if (isDive && f >= K.diveIn) continue; // vira o card que morfa
			// atividade: alguns tiles "publicam" (pulsam) em tempos diferentes
			const pulse = h > 0.86 ? Math.max(0, Math.sin((f + h * 200) / 7)) ** 6 : 0;
			let fill = h > 0.7 ? '#24282C' : '#191C1F';
			let op = vis * (1 - dive * 0.9);
			if (comment) {
				fill = C.white;
				op = lerp(0.95, 0.35, prog(f, K.recoil + 40, K.maior + 10, E.linear)) * (1 - dive);
			}
			rects.push(
				<g key={`${c}:${r}`} opacity={op}>
					<rect x={sx} y={sy} width={tw} height={th} rx={34 * zoom} fill={fill} />
					{pulse > 0.02 && <rect x={sx} y={sy} width={tw} height={th} rx={34 * zoom} fill={C.white} opacity={pulse * 0.55} />}
					{zoom > 0.07 && !comment && (
						<>
							<rect x={sx + 42 * zoom} y={sy + 120 * zoom} width={tw * (0.45 + h * 0.4)} height={44 * zoom} rx={8 * zoom} fill="#2E3237" />
							<rect x={sx + 42 * zoom} y={sy + 190 * zoom} width={tw * (0.25 + h * 0.3)} height={44 * zoom} rx={8 * zoom} fill="#2E3237" />
						</>
					)}
				</g>,
			);
		}
	}

	// tile do mergulho: morfa de retângulo de comentário para card de vídeo 9:16
	const dsx = 540 + (DIVE_SLOT[0] * PITCH_X - cx) * zoom;
	const dsy = 960 + (DIVE_SLOT[1] * PITCH_Y - cy) * zoom;
	const m = prog(f, K.diveIn, K.diveIn + 26, E.camera);
	const mw = lerp(tw, FEED_CARD.w, m);
	const mh = lerp(th, FEED_CARD.h, m);
	const mx = lerp(dsx, FEED_CARD.cx, m);
	const my = lerp(dsy, FEED_CARD.cy, m);

	// tipografia: UMA MUDANÇA / MAIOR
	const maiorS = sp(f, K.maior, {damping: 13, stiffness: 120, mass: 0.9});
	const maiorScale = lerp(0.06, 1, maiorS);
	const textOut = K.diveIn - 2;
	const bandOp = prog(f, K.maior - 30, K.maior - 10, E.linear) * (1 - prog(f, textOut, textOut + 14, E.linear));
	const lift = maiorScale * 150;

	return (
		<AbsoluteFill>
			{/* camada de pontos ao fundo: parallax mais lento que a grade */}
			<AbsoluteFill style={{opacity: 0.35 * prog(f, K.recoil + 10, K.recoil + 40, E.linear) * (1 - dive)}}>
				<svg width={1080} height={1920}>
					{Array.from({length: 13 * 22}).map((_, k) => {
						const gx = (k % 13) * 90 - ((cx * zoom * 0.25) % 90);
						const gy = Math.floor(k / 13) * 90 - ((cy * zoom * 0.25) % 90);
						return <circle key={k} cx={gx} cy={gy} r={1.6} fill={C.gray} />;
					})}
				</svg>
			</AbsoluteFill>
			<svg width={1080} height={1920} style={{position: 'absolute'}}>
				{rects}
			</svg>

			{/* banda escura para leitura da tipografia */}
			<AbsoluteFill
				style={{
					opacity: bandOp,
					background: 'linear-gradient(180deg, rgba(11,12,13,0) 28%, rgba(11,12,13,0.92) 42%, rgba(11,12,13,0.92) 62%, rgba(11,12,13,0) 76%)',
				}}
			/>
			{f < textOut + 20 && (
				<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
					<div style={{transform: `translateY(${-lift - 40}px)`}}>
						<MaskReveal
							text="UMA MUDANÇA"
							f={f}
							start={K.maior - 26}
							stagger={1.4}
							out={textOut}
							style={{fontWeight: 800, fontSize: 92, letterSpacing: '-0.02em', justifyContent: 'center'}}
						/>
					</div>
					<div style={{position: 'absolute', top: 960 - 130, transform: `scale(${maiorScale})`, opacity: f < K.maior ? 0 : 1}}>
						<MaskReveal
							text="MAIOR"
							f={f}
							start={K.maior - 40}
							stagger={0}
							dur={1}
							out={textOut}
							style={{fontWeight: 900, fontSize: 270, lineHeight: 1, letterSpacing: '-0.045em', justifyContent: 'center', textShadow: `0 0 ${60 * glowAt(f, K.maior + 8, 8, 30)}px rgba(244,243,238,0.55)`}}
						/>
					</div>
				</AbsoluteFill>
			)}

			{/* faísca circulando o tile escolhido antes do mergulho */}
			{f >= K.diveIn - 20 && f < K.diveIn + 2 && (
				<div style={{position: 'absolute', left: dsx - tw / 2, top: dsy - th / 2, width: tw, height: th}}>
					<div style={{position: 'absolute', inset: 0, borderRadius: 34 * zoom, background: C.white, opacity: 0.25 + 0.75 * glowAt(f, K.diveIn, 20, 2), boxShadow: `0 0 ${40}px rgba(244,243,238,0.6)`}} />
					<OrbitLight f={f} start={K.diveIn - 20} dur={22} w={tw} h={th} r={34 * zoom} laps={2} runners={2} width={3} pad={10} />
				</div>
			)}
			{/* card que nasce do tile */}
			{f >= K.diveIn && (
				<div
					style={{
						position: 'absolute',
						left: mx - mw / 2,
						top: my - mh / 2,
						width: mw,
						height: mh,
						borderRadius: lerp(34 * zoom, 34, m),
						overflow: 'hidden',
						background: '#24282C',
						boxShadow: `0 30px 80px rgba(0,0,0,${0.55 * m}), 0 0 ${90 * glowAt(f, K.diveIn + 14, 14, 16)}px rgba(244,243,238,0.4)`,
					}}
				>
					<div style={{opacity: prog(f, K.diveIn + 10, K.diveIn + 26, E.linear), width: FEED_CARD.w, height: FEED_CARD.h, transform: `scale(${mw / FEED_CARD.w}, ${mh / FEED_CARD.h})`, transformOrigin: '0 0'}}>
						{FEED_IMAGES.length ? <Img src={staticFile(`morphix/${FEED_IMAGES[0]}`)} style={{width: FEED_CARD.w, height: FEED_CARD.h, objectFit: 'cover', display: 'block'}} /> : <Thumb seed={3} w={FEED_CARD.w} h={FEED_CARD.h} />}
					</div>
				</div>
			)}
			{f >= K.diveIn && (
				<div style={{position: 'absolute', left: mx - mw / 2, top: my - mh / 2, width: mw, height: mh}}>
					<OrbitLight f={f} start={K.diveIn} dur={30} w={mw} h={mh} r={34} laps={1.3} runners={2} width={6} />
				</div>
			)}
			{/* MAIOR também tem um lado "técnico": contador de elementos */}
			<AbsoluteFill style={{alignItems: 'center', top: 1420, opacity: bandOp}}>
				<Chars
					text={`${Math.round(lerp(3, 2048, prog(f, K.recoil + 4, K.maior + 24, E.outQuart))).toString().padStart(4, '0')} ELEMENTOS`}
					style={{fontFamily: F.mono, fontSize: 24, letterSpacing: '0.2em', color: C.gray}}
					charStyle={() => ({})}
				/>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
