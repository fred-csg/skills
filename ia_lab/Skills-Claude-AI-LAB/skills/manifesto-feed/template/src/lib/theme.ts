import {loadFont as loadInterTight} from '@remotion/google-fonts/InterTight';
import {loadFont as loadPlexMono} from '@remotion/google-fonts/IBMPlexMono';

const inter = loadInterTight('normal', {weights: ['500', '700', '800', '900'], subsets: ['latin', 'latin-ext']});
const mono = loadPlexMono('normal', {weights: ['400', '500'], subsets: ['latin', 'latin-ext']});

export const C = {
	bg: '#0B0C0D',
	white: '#F4F3EE',
	orange: '#FF633E',
	gray: '#8B9095',
	struct: '#282B2F',
	panel: '#141618',
	panel2: '#1B1E21',
};

export const F = {
	display: inter.fontFamily,
	mono: mono.fontFamily,
};
