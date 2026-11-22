// CLEANSTILL — tokens, fontes e easings. Ver references/cleanstill.md na skill.
import {Easing, interpolate, useVideoConfig} from 'remotion';
import {loadFont as loadHead} from '@remotion/google-fonts/BricolageGrotesque';
import {loadFont as loadSerif} from '@remotion/google-fonts/InstrumentSerif';
import {loadFont as loadBody} from '@remotion/google-fonts/Inter';

export const FONT_HEAD = loadHead('normal', {weights: ['600', '700', '800'], subsets: ['latin', 'latin-ext']}).fontFamily;
export const FONT_SERIF = loadSerif('italic', {weights: ['400'], subsets: ['latin', 'latin-ext']}).fontFamily;
export const FONT_BODY = loadBody('normal', {weights: ['500', '600'], subsets: ['latin', 'latin-ext']}).fontFamily;

// Paleta medida no vídeo de referência
export const C = {
  bg: '#F3F4FB', // off-white azulado (fundo base)
  hazeLav: '#E4DDFB', // névoa lavanda
  hazeBlue: '#D8E5FA', // névoa azul-bebê
  hazePeach: '#F9E4DF', // névoa pêssego
  ink: '#363948', // texto principal (nunca preto puro)
  inkSoft: '#A3A7B6', // kicker / palavras fantasma
  blue: '#3764E0', // palavra-chave
  blueHi: '#6F93F0', // brilho da palavra-chave
  pill: '#3B6FF0', // pill de preço / botão
  sky1: '#0A6CCB', // céu topo
  sky2: '#5DB2F2', // céu base
  night: '#040714', // cena escura
  planet: '#2F55E8', // brilho do arco
  rim: '#CEF3FF', // linha fina do arco
  cyan: '#5FD8FF', // borda do blob
  warm: '#E7986B', // acento quente (1 ícone por cena, no máximo)
};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// Curvas do estilo: entradas "out quint" (chegam rápido e assentam macio), câmera inOut.
export const easeOut = Easing.bezier(0.22, 1, 0.36, 1);
export const easeIn = Easing.bezier(0.64, 0, 0.78, 0);
export const easeInOut = Easing.bezier(0.65, 0, 0.35, 1);
export const outBack = Easing.out(Easing.back(1.6));

export const prog = (f: number, a: number, b: number, ease = easeOut) =>
  interpolate(f, [a, b], [0, 1], {...clamp, easing: ease});
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

// RNG semeado (nada de Math.random)
export const rng = (seed: number) => () => {
  seed = (seed * 16807) % 2147483647;
  return (seed - 1) / 2147483646;
};

// Unidade: tudo é desenhado para a menor dimensão = 1080 (16:9 ou 9:16)
export const useUnit = () => {
  const {width, height} = useVideoConfig();
  return {u: Math.min(width, height) / 1080, width, height, vertical: height > width};
};
