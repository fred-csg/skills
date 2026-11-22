import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, F} from '../lib/theme';
import {E, SPR, hash, kick, lerp, prog, sp} from '../lib/motion';
import {Chars} from '../components/KineticTypography';
import {K} from '../data/script';

const LINE: React.CSSProperties = {fontFamily: F.display, fontWeight: 900, letterSpacing: '-0.04em', lineHeight: 1};

export const S9Care: React.FC<{f: number}> = ({f}) => {
	// câmera: aproximação lenta e contínua + pequeno overshoot no impacto final
	const push = lerp(0.97, 1.03, prog(f, K.fazer - 10, K.end, E.cameraSoft)) + kick(f, K.importar + 2, 0.012, 0.45, 0.18);

	// 1. QUASE NINGUÉM — composição tipográfica: letras chegam de posições distintas
	const fazer = (
		<Chars
			text="QUASE NINGUÉM"
			style={{...LINE, fontSize: 112, color: C.white}}
			charStyle={(i) => {
				const p = sp(f, K.fazer - 6 + i * 0.9, SPR.ui);
				const dx = (i - 6) * 70 * (1 - p);
				const dy = (hash(i + 70) - 0.5) * 220 * (1 - p);
				return {transform: `translate(${dx}px, ${dy}px) rotate(${(hash(i + 9) - 0.5) * 30 * (1 - p)}deg)`, opacity: Math.min(1, p * 2)};
			}}
		/>
	);

	// 2. FAZ ALGUÉM — surge do espaço negativo: um bloco branco com as palavras vazadas (NINGUÉM × ALGUÉM)
	const bar = sp(f, K.alguem - 4, {damping: 20, stiffness: 200, mass: 0.7});
	const reveal = prog(f, K.alguem, K.alguem + 12, E.outExpo);
	const alguem = (
		<div style={{position: 'relative', height: 128, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
			<div style={{position: 'absolute', top: 0, bottom: 0, left: '50%', width: 800 * bar, transform: 'translateX(-50%)', background: C.white, borderRadius: 4}} />
			<div style={{position: 'relative', clipPath: `inset(0 ${(1 - reveal) * 50}% 0 ${(1 - reveal) * 50}%)`}}>
				<Chars text="FAZ ALGUÉM" style={{...LINE, fontSize: 112, color: C.bg}} charStyle={(i) => ({letterSpacing: `${(1 - reveal) * 0.2}em`})} />
			</div>
		</div>
	);

	// 3. SE IMPORTAR. — maior peso, cor de destaque, revelação por máscara
	const imp = (
		<Chars
			text="SE IMPORTAR."
			mask
			style={{...LINE, fontSize: 140, color: C.orange}}
			charStyle={(i, n) => {
				const p = prog(f, K.importar - 4 + i * 1.1, K.importar + 12 + i * 1.1, E.outExpo);
				const dot = i === n - 1 ? 1 + kick(f, K.importar + 34, 0.35, 0.6, 0.2) : 1;
				return {transform: `translateY(${(1 - p) * 130}%) scale(${dot})`, transformOrigin: '50% 80%'};
			}}
		/>
	);
	const impScale = lerp(1.1, 1, prog(f, K.importar - 4, K.importar + 22, E.outQuart));

	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
			<div style={{transform: `scale(${push})`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22}}>
				{fazer}
				{alguem}
				<div style={{transform: `scale(${impScale})`}}>{imp}</div>
			</div>
		</AbsoluteFill>
	);
};
