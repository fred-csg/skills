import {E, track} from '../lib/motion';
import {K} from '../data/script';

// Mundo compartilhado entre a cena 1 (comentários) e a cena 2 (sistema).
// Os comentários têm exatamente o tamanho de um "tile" do sistema; no recuo,
// cada comentário encaixa no seu slot e vira um elemento da grade.
export const TILE_W = 860;
export const TILE_H = 330;
export const PITCH_X = 940;
export const PITCH_Y = 410;

/** slots (col, row) que os três comentários ocupam na grade */
export const COMMENT_SLOTS: [number, number][] = [
	[0, -1],
	[0, 0],
	[0, 1],
];

/** tile escolhido para o mergulho que vira o card de vídeo da cena 3 */
export const DIVE_SLOT: [number, number] = [1, -4];

/** zoom da câmera da cena 2 (também usado pela cena 1 no recuo) */
export const s2Zoom = (f: number) =>
	track(f, [
		[K.recoil, 1],
		[K.recoil + 50, 0.1, E.recoil],
		[K.maior, 0.088, E.cameraSoft],
		[K.maior + 28, 0.062, E.outExpo],
		[K.diveIn, 0.06, E.linear],
		[K.diveIn + 26, 1.25, E.inExpo],
	]);

/** centro da câmera (mundo) na cena 2 */
export const s2Center = (f: number) => {
	const tx = DIVE_SLOT[0] * PITCH_X;
	const ty = DIVE_SLOT[1] * PITCH_Y;
	return {
		x: track(f, [
			[K.recoil, 0],
			[K.recoil + 60, -PITCH_X * 0.5, E.camera],
			[K.diveIn - 6, tx * 0.4, E.cameraSoft],
			[K.diveIn + 22, tx, E.camera],
		]),
		y: track(f, [
			[K.recoil, 60],
			[K.recoil + 60, PITCH_Y * 2, E.camera],
			[K.diveIn - 6, ty * 0.5, E.cameraSoft],
			[K.diveIn + 22, ty, E.camera],
		]),
	};
};

// Card central do feed (cena 3), em coordenadas de tela
export const FEED_CARD = {w: 620, h: 1040, cx: 540, cy: 900};
