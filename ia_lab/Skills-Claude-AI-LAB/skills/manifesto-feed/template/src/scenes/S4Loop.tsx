import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, F} from '../lib/theme';
import {E, SPR, clamp, kick, lerp, noise, prog, sp} from '../lib/motion';
import {MaskReveal, Mono} from '../components/KineticTypography';
import {FeedCard, Thumb} from '../components/FeedCards';
import {K} from '../data/script';
import {HERO_IMAGE} from '../data/morphix-assets';
import {Img, staticFile} from 'remotion';
import {OrbitLight, glowAt} from '../components/FX';

// Layout (tela)
export const S4_LAYOUT = {beltY: 560, machineX: 150, dividerY: 870, cardCY: 1240, cardW: 300, cardH: 520};

// Emissões da máquina: cada vez mais rápidas (frames)
export const EMITS: number[] = (() => {
	const out: number[] = [];
	let t = K.toBelt + 10;
	let gap = 9;
	while (t < K.contract) {
		out.push(Math.round(t));
		t += gap;
		gap = Math.max(3.2, gap * 0.9);
	}
	return out;
})();

const TRAVEL = 30; // frames que um card leva na esteira

const Belt: React.FC<{f: number; on: number}> = ({f, on}) => {
	const {beltY, machineX} = S4_LAYOUT;
	const speed = (f - K.toBelt) * 22;
	return (
		<div style={{position: 'absolute', left: 0, top: beltY - 160, width: 1080, height: 320, perspective: 900, perspectiveOrigin: '50% 10%'}}>
			{/* superfície da esteira */}
			<div
				style={{
					position: 'absolute',
					left: -200,
					top: 150,
					width: 1480,
					height: 160,
					transform: 'rotateX(62deg)',
					transformOrigin: '50% 0%',
					background: `repeating-linear-gradient(90deg, ${C.struct} 0 3px, transparent 3px 46px)`,
					backgroundPositionX: speed,
					boxShadow: `inset 0 0 0 2px ${C.struct}`,
					opacity: on,
				}}
			/>
			{/* cards saindo da máquina */}
			{EMITS.map((t, i) => {
				const p = (f - t) / TRAVEL;
				if (p < 0 || p > 1.2) return null;
				const x = lerp(machineX + 60, 1240, E.inQuart(clamp(p)) * 0.45 + clamp(p) * 0.55);
				const pop = sp(f, t, SPR.elastic);
				return (
					<div key={i} style={{position: 'absolute', left: x - 70, top: 160 - 250 + 140, transform: `scale(${lerp(0.2, 1, pop)}) rotate(${(1 - pop) * -8}deg)`, transformOrigin: '50% 100%', opacity: on}}>
						<FeedCard seed={200 + i * 5} w={140} h={250} meta={false} radius={20} />
					</div>
				);
			})}
			{/* máquina */}
			<div
				style={{
					position: 'absolute',
					left: machineX - 90,
					top: 30,
					width: 180,
					height: 300,
					borderRadius: 26,
					background: C.panel2,
					boxShadow: `inset 0 0 0 2px ${C.struct}, 0 30px 60px rgba(0,0,0,0.6), 0 0 ${36 * glowAt(f, EMITS.filter((t) => t <= f).pop() ?? -99, 0, 6)}px rgba(244,243,238,0.45)`,
					transform: `scaleY(${1 + kick(f, EMITS.filter((t) => t <= f).pop() ?? -99, 0.04, 1.2, 0.4)})`,
					transformOrigin: '50% 100%',
					opacity: on,
				}}
			>
				<div style={{position: 'absolute', right: -2, top: 120, width: 14, height: 150, background: C.bg, borderRadius: 4}} />
				<div style={{position: 'absolute', left: 30, top: 34, width: 120, height: 6, borderRadius: 3, background: C.struct}}>
					<div style={{height: '100%', width: `${((f * 7) % 100)}%`, background: C.white, borderRadius: 3}} />
				</div>
				<div style={{position: 'absolute', left: 30, top: 56, display: 'flex', gap: 8}}>
					{[0, 1, 2].map((d) => (
						<div key={d} style={{width: 10, height: 10, borderRadius: 9, background: Math.floor(f / 3) % 3 === d ? C.white : C.struct}} />
					))}
				</div>
			</div>
		</div>
	);
};

/** card isolado, sendo refinado em camadas */
const RefinedCard: React.FC<{f: number}> = ({f}) => {
	const {cardW: w, cardH: h} = S4_LAYOUT;
	const st = K.esperar - 6;
	const grid = prog(f, st + 6, st + 22, E.outQuart);
	const rich = prog(f, st + 16, st + 34, E.inOutSine);
	const type = prog(f, st + 26, st + 40, E.outExpo);
	const marks = sp(f, K.perfeito, SPR.lock);
	const corner = (rot: number, left: boolean, top: boolean) => (
		<div
			style={{
				position: 'absolute',
				[left ? 'left' : 'right']: -18 - (1 - marks) * 30,
				[top ? 'top' : 'bottom']: -18 - (1 - marks) * 30,
				width: 34,
				height: 34,
				borderTop: `4px solid ${C.orange}`,
				borderLeft: `4px solid ${C.orange}`,
				transform: `rotate(${rot}deg)`,
				opacity: marks,
			}}
		/>
	);
	return (
		<div style={{position: 'relative', width: w, height: h}}>
			<div style={{position: 'absolute', inset: 0, borderRadius: 26, overflow: 'hidden', background: C.panel2, boxShadow: `0 30px 70px rgba(0,0,0,0.6), 0 0 ${90 * marks}px rgba(255,99,62,${0.35 * marks})`}}>
				<div style={{position: 'absolute', inset: 0, opacity: 0.35 * (1 - rich), filter: 'grayscale(1) contrast(0.5)'}}>
					<Thumb seed={404} w={w} h={h} detail={0} />
				</div>
				<div style={{position: 'absolute', inset: 0, opacity: rich}}>
					{HERO_IMAGE ? <Img src={staticFile(HERO_IMAGE)} style={{width: w, height: h, objectFit: 'cover', display: 'block'}} /> : <Thumb seed={9} w={w} h={h} accent />}
				</div>
				{/* guias de grade (construção) */}
				<svg width={w} height={h} style={{position: 'absolute', inset: 0, opacity: (1 - rich * 0.7) * 0.8}}>
					{[1, 2].map((k) => (
						<React.Fragment key={k}>
							<line x1={(w / 3) * k} y1={0} x2={(w / 3) * k} y2={h * grid} stroke={C.white} strokeWidth={1.2} opacity={0.5} />
							<line x1={0} y1={(h / 3) * k} x2={w * grid} y2={(h / 3) * k} stroke={C.white} strokeWidth={1.2} opacity={0.5} />
						</React.Fragment>
					))}
					<circle cx={w / 2} cy={h / 2} r={(w / 2.4) * grid} fill="none" stroke={C.white} strokeWidth={1.2} opacity={0.4} />
				</svg>
				<div style={{position: 'absolute', left: 26, right: 26, bottom: 30, opacity: type, transform: `translateY(${(1 - type) * 20}px)`}}>
					<div style={{height: 12, width: '72%', borderRadius: 6, background: 'rgba(244,243,238,0.85)', marginBottom: 10}} />
					<div style={{height: 10, width: '46%', borderRadius: 6, background: 'rgba(244,243,238,0.4)', marginBottom: 20}} />
					<div style={{height: 4, borderRadius: 3, background: 'rgba(244,243,238,0.2)'}}>
						<div style={{height: '100%', width: `${marks * 100}%`, background: C.orange, borderRadius: 3}} />
					</div>
				</div>
			</div>
			<OrbitLight f={f} start={K.perfeito - 4} dur={K.contract + 10 - (K.perfeito - 4)} w={w} h={h} r={26} laps={1.8} runners={2} color={C.orange} width={6} pad={10} />
			{corner(0, true, true)}
			{corner(90, false, true)}
			{corner(-90, true, false)}
			{corner(180, false, false)}
		</div>
	);
};

export const S4Loop: React.FC<{f: number}> = ({f}) => {
	const {beltY, dividerY, cardCY, cardH} = S4_LAYOUT;
	const on = prog(f, K.toBelt - 2, K.toBelt + 12, E.outQuart);
	const contract = prog(f, K.contract, K.contract + 18, E.inExpo);
	const count = EMITS.filter((t) => t + 4 <= f).length;
	const pct = Math.min(97, Math.floor(97 * prog(f, K.esperar - 4, K.perfeito - 2, E.outQuart)));
	const bottomOn = prog(f, K.publicar + 16, K.publicar + 34, E.outQuart);
	const refinePct = f >= K.perfeito ? 100 : pct;
	const camX = noise(f / 40, 12) * 10 + lerp(-24, 24, prog(f, K.toBelt, K.contract, E.linear));
	const shrink = (cy: number): React.CSSProperties => ({
		transform: `translate(${camX * (1 - contract)}px, ${(960 - cy) * contract * 0.5}px) scale(${1 - contract * 0.7})`,
		transformOrigin: `540px ${cy}px`,
		opacity: 1 - contract,
		filter: contract > 0.02 ? `blur(${contract * 10}px)` : undefined,
	});
	return (
		<AbsoluteFill>
			<AbsoluteFill style={shrink(beltY)}>
				<AbsoluteFill style={{top: 196, alignItems: 'center'}}>
					<Mono style={{opacity: on}}>DURANTE ANOS</Mono>
				</AbsoluteFill>
				<AbsoluteFill style={{top: 252, alignItems: 'center'}}>
					<MaskReveal text="PUBLICAR MAIS" f={f} start={K.publicar - 6} stagger={1.2} style={{fontWeight: 900, fontSize: 92, letterSpacing: '-0.035em'}} />
				</AbsoluteFill>
				<Belt f={f} on={on} />
				<AbsoluteFill style={{top: beltY + 190, alignItems: 'center'}}>
					<Mono style={{opacity: on, color: C.white}}>
						PUBLICADOS <span style={{color: C.gray}}>{String(count).padStart(4, '0')}</span>
					</Mono>
				</AbsoluteFill>
			</AbsoluteFill>
			{/* divisória */}
			<div
				style={{
					position: 'absolute',
					left: 540 - 420 * prog(f, K.esperar - 14, K.esperar + 4, E.outExpo),
					width: 840 * prog(f, K.esperar - 14, K.esperar + 4, E.outExpo),
					top: dividerY,
					height: 2,
					background: C.struct,
					opacity: 1 - contract,
				}}
			/>
			<AbsoluteFill style={shrink(cardCY)}>
				<AbsoluteFill style={{top: dividerY + 46, alignItems: 'center'}}>
					<MaskReveal text="ESPERAR O PERFEITO" f={f} start={K.esperar - 4} stagger={1} style={{fontWeight: 900, fontSize: 70, letterSpacing: '-0.03em'}} />
				</AbsoluteFill>
				<div
					style={{
						position: 'absolute',
						left: 540 - S4_LAYOUT.cardW / 2,
						top: cardCY - cardH / 2 + 50,
						opacity: bottomOn,
						transform: `translateY(${(1 - bottomOn) * 60}px) rotate(${noise(f / 30, 7) * 0.6}deg)`,
					}}
				>
					<RefinedCard f={f} />
				</div>
				<AbsoluteFill style={{top: cardCY + cardH / 2 + 84, alignItems: 'center'}}>
					<Mono style={{opacity: bottomOn, color: f >= K.perfeito ? C.white : C.gray}}>
						REFINANDO {String(refinePct).padStart(3, '0')}%{f >= K.perfeito ? <span style={{color: C.orange}}> ●</span> : null}
					</Mono>
				</AbsoluteFill>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
