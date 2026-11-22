import React from 'react';
import {C, F} from '../lib/theme';
import {E, clamp, prog} from '../lib/motion';

type CharStyleFn = (i: number, n: number, ch: string) => React.CSSProperties;

/** Texto com cada caractere tratado individualmente. */
export const Chars: React.FC<{
	text: string;
	charStyle: CharStyleFn;
	style?: React.CSSProperties;
	mask?: boolean; // cada caractere dentro de uma máscara (clip)
}> = ({text, charStyle, style, mask}) => {
	const chars = [...text];
	return (
		<div style={{display: 'flex', whiteSpace: 'pre', fontFamily: F.display, color: C.white, ...style}}>
			{chars.map((ch, i) =>
				mask ? (
					<span key={i} style={{display: 'inline-block', overflow: 'hidden', paddingBottom: '0.04em', marginBottom: '-0.04em'}}>
						<span style={{display: 'inline-block', ...charStyle(i, chars.length, ch)}}>{ch}</span>
					</span>
				) : (
					<span key={i} style={{display: 'inline-block', ...charStyle(i, chars.length, ch)}}>
						{ch}
					</span>
				),
			)}
		</div>
	);
};

/** Revelação por máscara, caractere a caractere, de baixo para cima. */
export const MaskReveal: React.FC<{
	text: string;
	f: number;
	start: number;
	stagger?: number;
	dur?: number;
	out?: number; // frame de saída (sobe e some pela máscara)
	style?: React.CSSProperties;
	from?: 'bottom' | 'top';
}> = ({text, f, start, stagger = 1.6, dur = 16, out, style, from = 'bottom'}) => (
	<Chars
		text={text}
		mask
		style={style}
		charStyle={(i) => {
			const pin = prog(f, start + i * stagger, start + i * stagger + dur, E.outExpo);
			const pout = out === undefined ? 0 : prog(f, out + i * stagger * 0.6, out + i * stagger * 0.6 + dur * 0.8, E.inExpo);
			const dir = from === 'bottom' ? 1 : -1;
			return {transform: `translateY(${(dir * (1 - pin) - dir * pout) * 130}%)`};
		}}
	/>
);

/** Palavras com entrada escalonada (para frases de comentário). */
export const WordStagger: React.FC<{
	text: string;
	f: number;
	start: number;
	stagger?: number;
	style?: React.CSSProperties;
	highlight?: string;
	renderHighlight?: (word: string) => React.ReactNode;
}> = ({text, f, start, stagger = 2.5, style, highlight, renderHighlight}) => {
	const words = text.split(' ');
	return (
		<div style={{display: 'flex', flexWrap: 'wrap', columnGap: '0.26em', rowGap: '0.04em', ...style}}>
			{words.map((w, i) => {
				const p = prog(f, start + i * stagger, start + i * stagger + 14, E.outExpo);
				const isHi = highlight && w.toLowerCase().startsWith(highlight.toLowerCase());
				return (
					<span key={i} style={{display: 'inline-block', overflow: 'hidden', paddingBottom: '0.08em'}}>
						<span style={{display: 'inline-block', transform: `translateY(${(1 - p) * 105}%)`, opacity: clamp(p * 3)}}>
							{isHi && renderHighlight ? renderHighlight(w) : w}
						</span>
					</span>
				);
			})}
		</div>
	);
};

export const Mono: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
	<div
		style={{
			fontFamily: F.mono,
			fontSize: 24,
			letterSpacing: '0.12em',
			textTransform: 'uppercase',
			color: C.gray,
			whiteSpace: 'pre',
			...style,
		}}
	>
		{children}
	</div>
);
