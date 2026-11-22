import {FPS} from './timing';

// Ritmo do vídeo: cada trecho da timeline ORIGINAL (45 s) toca numa velocidade.
// [início s, fim s, velocidade]. 1 = como foi animado; 1.4 = 40% mais rápido.
// Todas as cenas continuam escritas no relógio original; só o tempo de exibição muda.
export const SPEED: [number, number, number][] = [
	[0, 5.5, 1.2], // 01 comentários: precisam ser lidos
	[5.5, 9, 1.35], // 02 uma mudança maior
	[9, 13, 1.3], // 03 consumir / deslizar / esquecer
	[13, 17.3, 1.45], // 04 publicar mais vs esperar o perfeito
	[17.3, 22.5, 1.35], // 05 três forças
	[22.5, 27.4, 1.3], // 06 universo de conteúdo
	[27.4, 32, 1.25], // 07 paradoxo (a pausa continua existindo)
	[32, 40.4, 1.45], // 08 bifurcação
	[40.4, 43.6, 1.2], // 09 frase final
	[43.6, 45, 1], // repouso final para leitura
];

type Seg = {oa: number; ob: number; v: number; na: number; nb: number};
const SEGS: Seg[] = (() => {
	let acc = 0;
	return SPEED.map(([a, b, v]) => {
		const oa = a * FPS;
		const ob = b * FPS;
		const seg = {oa, ob, v, na: acc, nb: acc + (ob - oa) / v};
		acc = seg.nb;
		return seg;
	});
})();

export const WARPED_DURATION = Math.round(SEGS[SEGS.length - 1].nb);

/** frame novo (exibido) → frame original (onde as cenas foram animadas) */
export const warp = (nf: number) => {
	for (const s of SEGS) if (nf <= s.nb) return s.oa + (Math.max(nf, s.na) - s.na) * s.v;
	return SEGS[SEGS.length - 1].ob;
};

/** frame original → frame novo (para posicionar SFX, voz e trilha) */
export const unwarp = (of: number) => {
	for (const s of SEGS) if (of <= s.ob) return s.na + (Math.max(of, s.oa) - s.oa) / s.v;
	return SEGS[SEGS.length - 1].nb;
};
