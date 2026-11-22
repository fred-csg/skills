import {Easing, interpolate} from 'remotion';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export const inOut = Easing.inOut(Easing.cubic);
export const outCubic = Easing.out(Easing.cubic);
export const outExpo = Easing.out(Easing.exp);
export const outBack = Easing.out(Easing.back(1.5));
export const inOutSine = Easing.inOut(Easing.sin);

// 0→1 entre os frames a e b, com easing (nunca linear)
export const prog = (f: number, a: number, b: number, ease = inOut) =>
  interpolate(f, [a, b], [0, 1], {...clamp, easing: ease});

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

export const LIME = '#D7FF3A';
