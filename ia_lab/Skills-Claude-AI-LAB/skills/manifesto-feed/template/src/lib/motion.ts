import {Easing, spring} from 'remotion';
import {FPS} from './timing';

export const clamp = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const mix = lerp;

type Ease = (t: number) => number;

// Biblioteca de curvas: cada tipo de movimento tem a sua.
export const E = {
	linear: (t: number) => t,
	// objetos pequenos: resposta rápida, assentamento longo
	snap: Easing.bezier(0.16, 1, 0.3, 1),
	outExpo: Easing.bezier(0.19, 1, 0.22, 1),
	outQuart: Easing.bezier(0.25, 1, 0.5, 1),
	inQuart: Easing.bezier(0.5, 0, 0.75, 0),
	inExpo: Easing.bezier(0.7, 0, 0.84, 0),
	// câmera: aceleração e desaceleração controladas
	camera: Easing.bezier(0.65, 0, 0.35, 1),
	cameraSoft: Easing.bezier(0.45, 0, 0.2, 1),
	// recuo violento: arranca rápido, chega devagar
	recoil: Easing.bezier(0.85, 0, 0.15, 1),
	// antecipação: recua antes de ir
	anticipate: Easing.bezier(0.36, -0.35, 0.3, 1),
	overshoot: Easing.bezier(0.34, 1.56, 0.64, 1),
	inOutSine: Easing.bezier(0.37, 0, 0.63, 1),
} satisfies Record<string, Ease>;

/** progresso 0..1 entre os frames a e b com easing */
export const prog = (f: number, a: number, b: number, ease: Ease = E.outQuart) =>
	ease(clamp((f - a) / Math.max(1e-6, b - a)));

/** keyframes [frame, valor, easing do segmento que CHEGA nesse key] */
export type Key = [number, number, Ease?];
export const track = (f: number, keys: Key[]) => {
	if (f <= keys[0][0]) return keys[0][1];
	for (let i = 1; i < keys.length; i++) {
		const [fb, vb, eb] = keys[i];
		const [fa, va] = keys[i - 1];
		if (f <= fb) return lerp(va, vb, (eb ?? E.camera)(clamp((f - fa) / (fb - fa))));
	}
	return keys[keys.length - 1][1];
};

/** spring com parâmetros por elemento */
export const SPR = {
	ui: {damping: 16, stiffness: 220, mass: 0.6},
	elastic: {damping: 9, stiffness: 180, mass: 0.7},
	heavy: {damping: 22, stiffness: 90, mass: 1.4},
	lock: {damping: 30, stiffness: 400, mass: 0.5},
	soft: {damping: 200, stiffness: 60, mass: 1},
};
export const sp = (f: number, start: number, config = SPR.ui, durationInFrames?: number) =>
	f < start ? 0 : spring({frame: f - start, fps: FPS, config, durationInFrames});

/** RNG determinístico */
export const rng = (seed: number) => {
	let a = seed >>> 0;
	return () => {
		a = (a + 0x6d2b79f5) >>> 0;
		let t = a;
		t = Math.imul(t ^ (t >>> 15), t | 1);
		t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
};
export const hash = (n: number) => rng(n * 9301 + 49297)();

/** ruído suave 1D (value noise) para derivas orgânicas determinísticas */
export const noise = (x: number, seed = 0) => {
	const i = Math.floor(x);
	const fr = x - i;
	const a = hash(i + seed * 1013);
	const b = hash(i + 1 + seed * 1013);
	const u = fr * fr * (3 - 2 * fr);
	return lerp(a, b, u) * 2 - 1;
};

/** impulso que decai (reação a impacto) */
export const kick = (f: number, at: number, amp: number, freq = 0.55, decay = 0.16) => {
	if (f < at) return 0;
	const t = f - at;
	return amp * Math.sin(t * freq) * Math.exp(-t * decay);
};

/** janela de visibilidade com fade nas bordas (em frames) */
export const windowed = (f: number, a: number, b: number, fadeIn = 6, fadeOut = 6) =>
	Math.min(prog(f, a, a + fadeIn, E.linear), 1 - prog(f, b - fadeOut, b, E.linear));
