// Linha do tempo mestre. TODA cena e todo SFX leem daqui.
// Para sincronizar com a narração gravada: ajuste os valores em segundos
// de `VO` (src/data/script.ts) e as janelas de `SCENES` abaixo.

export const FPS = 30;
export const W = 1080;
export const H = 1920;
export const DURATION = 1350; // 45 s

export const s = (sec: number) => Math.round(sec * FPS);

// [início, fim] de cada sequência, em frames. As cenas se sobrepõem nas
// transições (a cena seguinte nasce do último estado da anterior).
export const SCENES = {
	s1Opinion: [0, 186],
	s2Bigger: [168, 282],
	s3Scroll: [270, 402],
	s4Loop: [390, 540],
	s5Forces: [528, 684],
	s6Infinite: [672, 880],
	s7Paradox: [810, 972],
	s8Split: [960, 1262],
	s9Care: [1240, 1350],
} as const satisfies Record<string, readonly [number, number]>;

export type SceneId = keyof typeof SCENES;
