import {K} from './script';
import {EMITS} from '../scenes/S4Loop';
import meta from './sfx-meta.json';

// Mapa de SFX. Todos os arquivos vêm da biblioteca Ocular Sounds (Ultimate Sound FX Bundle),
// copiados por scripts/stage-sfx.mjs (origem exata em src/data/sfx-meta.json).
// `at` = frame do EVENTO visual; o PICO do som é alinhado a esse frame.

export type SfxId = keyof typeof meta;
export type Cue = {
	scene: string;
	at: number;
	sfx: SfxId;
	vol: number;
	pan?: 'L' | 'R';
	fadeIn?: number; // frames
	fadeOut?: number; // frames
	maxDur?: number; // corta o som após N frames (com fadeOut)
	align?: 'peak' | 'start';
	trimSec?: number; // pula o começo do arquivo
	why: string;
};

// V2: o fluxo descartável vira um tique mecânico repetitivo (mesma cadência dos cards), só à esquerda
const stream: Cue[] = [];
for (let t = K.fork + 12, k = 0; t < K.futuro; t += 6, k++)
	stream.push({scene: '08', at: t, sfx: 'click_metal', vol: k % 4 === 0 ? 0.1 : 0.06, pan: 'L', why: 'V2 · fluxo descartável: tique repetitivo e baixo no canal esquerdo (substitui os whips da V1)'});
stream.push({scene: '08', at: K.fork + 20, sfx: 'whip_b', vol: 0.1, pan: 'L', why: 'primeira passagem do fluxo'});

const belt: Cue[] = EMITS.filter((_, i) => i % 3 === 0).map((t, i) => ({
	scene: '04',
	at: t,
	sfx: 'click_metal' as const,
	vol: 0.16 + Math.min(0.1, i * 0.01),
	pan: i % 2 ? ('R' as const) : undefined,
	why: 'carimbo de saída da máquina (1 a cada 3 cards, cresce com a cadência)',
}));

export const CUES: Cue[] = [
	// 01 — OPINION STORM
	{scene: '01', at: 2, sfx: 'click_single', vol: 0.5, why: 'primeiro comentário já entra no frame 0: clique de UI seco'},
	{scene: '01', at: K.realista + 1, sfx: 'pop_soft', vol: 0.32, why: 'bloco branco varre "REALISTA"'},
	{scene: '01', at: K.card2 + 5, sfx: 'whip_b', vol: 0.42, pan: 'R', why: 'comentário 2 chega pela direita'},
	{scene: '01', at: K.card2 + 7, sfx: 'snap_elastic', vol: 0.36, why: 'impacto: card 1 é empurrado em profundidade'},
	{scene: '01', at: K.fortuna + 1, sfx: 'pop_soft', vol: 0.32, pan: 'R', why: '"FORTUNA" destacada'},
	{scene: '01', at: K.card3 + 6, sfx: 'whip_c', vol: 0.36, why: 'comentário 3 sobe de baixo'},
	{scene: '01', at: K.card3 + 9, sfx: 'snap_elastic', vol: 0.42, why: 'assentamento elástico do card 3'},
	{scene: '01', at: K.empregos + 1, sfx: 'pop_soft', vol: 0.36, pan: 'L', why: '"EMPREGOS" destacada'},
	{scene: '01', at: K.recoil + 6, sfx: 'reverse_swell', vol: 0.5, why: 'reverse swell que puxa o recuo violento da câmera'},
	{scene: '01', at: K.realista + 7, sfx: 'click_metal', vol: 0.1, why: 'V2 · micro: curtida acende no card 1'},
	{scene: '01', at: K.fortuna + 7, sfx: 'click_metal', vol: 0.1, pan: 'R', why: 'V2 · micro: curtida acende no card 2'},
	{scene: '01', at: K.empregos + 7, sfx: 'click_metal', vol: 0.11, pan: 'L', why: 'V2 · micro: curtida acende no card 3'},
	// 02 — THE BIGGER CHANGE
	{scene: '02', at: K.recoil + 20, sfx: 'whoosh_exhale', vol: 0.32, why: 'ar do recuo revelando o sistema'},
	{scene: '02', at: K.recoil + 30, sfx: 'impact_low', vol: 0.34, fadeOut: 30, maxDur: 75, why: 'acento grave: a escala do sistema'},
	{scene: '02', at: K.maior + 6, sfx: 'tonal_accent', vol: 0.26, fadeOut: 30, maxDur: 70, why: '"MAIOR" se expande (expansão sutil, tonal)'},
	{scene: '02', at: K.maior + 10, sfx: 'impact_soft', vol: 0.32, fadeOut: 20, maxDur: 50, why: 'peso do "MAIOR" assentando'},
	{scene: '02', at: K.diveIn + 22, sfx: 'whip_a', vol: 0.42, why: 'mergulho no tile que vira card de vídeo'},
	// 03 — SCROLL CULTURE
	{scene: '03', at: K.diveIn + 46, sfx: 'swipe_paper', vol: 0.26, why: 'rolagem passiva inicial do feed'},
	{scene: '03', at: K.consumir + 10, sfx: 'swipe_sand', vol: 0.3, pan: 'L', why: 'CONSUMIR: laterais sugadas para o centro'},
	{scene: '03', at: K.consumir + 14, sfx: 'click_short', vol: 0.34, why: 'letras de CONSUMIR travam no centro'},
	{scene: '03', at: K.deslizar + 4, sfx: 'swipe_rl', vol: 0.5, why: 'DESLIZAR: swipe da composição inteira'},
	{scene: '03', at: K.deslizar + 9, sfx: 'whip_d', vol: 0.22, pan: 'R', why: 'camada lateral que chega depois (parallax sonoro)'},
	{scene: '03', at: K.esquecer + 22, sfx: 'airy_sweep', vol: 0.2, fadeIn: 10, fadeOut: 16, maxDur: 40, why: 'ESQUECER: o card perde foco, ar sem transiente'},
	// 04 — PRODUCTION LOOP
	{scene: '04', at: K.toBelt + 6, sfx: 'whoosh_exhale', vol: 0.26, why: 'o feed deita e vira esteira'},
	{scene: '04', at: K.toBelt + 8, sfx: 'ticking_loop', vol: 0.16, align: 'start', fadeIn: 14, fadeOut: 14, maxDur: K.contract - K.toBelt - 8, why: 'ritmo mecânico da produção contínua'},
	...belt,
	{scene: '04', at: K.esperar + 10, sfx: 'gears', vol: 0.2, fadeOut: 12, maxDur: 60, why: 'engrenagens finas: o card isolado sendo refinado'},
	{scene: '04', at: K.esperar + 2, sfx: 'click_short', vol: 0.12, why: 'V2 · micro: guias de grade aparecem no card isolado'},
	{scene: '04', at: K.esperar + 22, sfx: 'beep_tick', vol: 0.1, why: 'V2 · micro: camada de tipografia aplicada'},
	{scene: '04', at: K.perfeito, sfx: 'click_single', vol: 0.46, why: 'cantoneiras laranja travam (precisão)'},
	{scene: '04', at: K.perfeito + 2, sfx: 'tonal_accent', vol: 0.2, pan: 'R', fadeOut: 20, maxDur: 40, why: 'acento tonal do "perfeito"'},
	{scene: '04', at: K.contract + 16, sfx: 'whip_b', vol: 0.36, why: 'contração em três formas'},
	// 05 — THREE FORCES
	{scene: '05', at: K.velocidade + 4, sfx: 'whip_a', vol: 0.5, pan: 'R', why: 'VELOCIDADE: disparo direcional com rastros'},
	{scene: '05', at: K.velocidade + 14, sfx: 'whip_b', vol: 0.28, pan: 'L', why: 'retorno da forma'},
	{scene: '05', at: K.velocidade + 22, sfx: 'click_metal', vol: 0.14, pan: 'R', why: 'V2 · micro: ícone de velocidade assenta após o overshoot'},
	{scene: '05', at: K.custo + 2, sfx: 'snap_elastic', vol: 0.42, why: 'CUSTO MENOR: camadas colapsam'},
	{scene: '05', at: K.custo + 8, sfx: 'click_metal', vol: 0.3, why: 'contração final do quadrado'},
	{scene: '05', at: K.qualidade + 14, sfx: 'beep_tick', vol: 0.3, why: 'QUALIDADE: o traço fecha o círculo'},
	{scene: '05', at: K.qualidade + 10, sfx: 'click_short', vol: 0.32, why: 'guias de precisão encaixam'},
	{scene: '05', at: K.lock + 8, sfx: 'riser_sparkle', vol: 0.28, fadeIn: 6, why: 'atração magnética (o pico do riser termina no travamento)'},
	{scene: '05', at: K.lock + 9, sfx: 'mech_lock', vol: 0.5, why: 'travamento mecânico do emblema'},
	{scene: '05', at: K.lock + 9, sfx: 'sub_tail', vol: 0.3, fadeOut: 30, maxDur: 70, why: 'sub sob o travamento'},
	// 06 — INFINITE CONTENT
	{scene: '06', at: K.produce, sfx: 'pop_soft', vol: 0.34, why: '1 card nasce do sistema'},
	{scene: '06', at: K.produce + 13, sfx: 'click_single', vol: 0.32, why: '×4'},
	{scene: '06', at: K.produce + 25, sfx: 'click_short', vol: 0.34, why: '×16'},
	{scene: '06', at: K.produce + 36, sfx: 'click_metal', vol: 0.36, why: '×64'},
	{scene: '06', at: K.produce + 46, sfx: 'beep_tick', vol: 0.3, why: '×256'},
	{scene: '06', at: K.produce + 62, sfx: 'whoosh_exhale', vol: 0.42, why: 'câmera atravessa a grade e entra no corredor'},
	{scene: '06', at: K.produce + 52, sfx: 'riser_pulse', vol: 0.34, align: 'start', trimSec: 2.4, fadeIn: 8, fadeOut: 10, maxDur: K.incrivelWall + 18 - (K.produce + 52), why: 'pulsos rítmicos e build-up do universo de conteúdo (corta seco antes do silêncio)'},
	{scene: '06', at: K.produce + 80, sfx: 'whip_c', vol: 0.24, pan: 'L', why: 'passagem espacial (parede esquerda)'},
	{scene: '06', at: K.produce + 94, sfx: 'whip_a', vol: 0.24, pan: 'R', why: 'passagem espacial (parede direita)'},
	{scene: '06', at: K.massa - 10, sfx: 'whip_d', vol: 0.26, pan: 'L', why: 'aceleração'},
	{scene: '06', at: K.massa + 2, sfx: 'impact_low', vol: 0.38, fadeOut: 24, maxDur: 50, why: '"EM MASSA"'},
	// 07 — PARADOX
	{scene: '07', at: K.incrivelWall + 18, sfx: 'airy_sweep', vol: 0.18, fadeIn: 20, fadeOut: 24, maxDur: 60, why: 'textura que sobe enquanto INCRÍVEL se multiplica… e some no silêncio'},
	{scene: '07', at: K.dissolve + 4, sfx: 'glitch', vol: 0.16, why: 'INCRÍVEL se desfaz em unidades tipográficas'},
	{scene: '07', at: K.dissolve + 14, sfx: 'swipe_sand', vol: 0.12, pan: 'R', why: 'poeira de letras'},
	{scene: '07', at: K.diferencial + 4, sfx: 'sub_tail', vol: 0.2, fadeOut: 30, maxDur: 60, why: 'peso discreto em "DIFERENCIAL"'},
	// 08 — THE SPLIT
	{scene: '08', at: K.splitLine + 2, sfx: 'click_short', vol: 0.3, why: 'o ponto que inicia a linha'},
	{scene: '08', at: K.fork + 10, sfx: 'swipe_rl', vol: 0.3, pan: 'L', why: 'bifurcação: varredura estéreo para a esquerda'},
	{scene: '08', at: K.fork + 16, sfx: 'swipe_sand', vol: 0.3, pan: 'R', why: 'bifurcação: varredura estéreo para a direita'},
	...stream,
	{scene: '08', at: K.outro + 2, sfx: 'pop_soft', vol: 0.18, pan: 'R', why: 'V2 · micro: o card se desprende da corrente'},
	{scene: '08', at: K.outro + 2, sfx: 'whoosh_exhale', vol: 0.3, pan: 'R', why: 'o card da direita sai da corrente'},
	{scene: '08', at: K.parar, sfx: 'impact_soft', vol: 0.42, pan: 'R', fadeOut: 24, maxDur: 60, why: 'o card para'},
	{scene: '08', at: K.parar + 2, sfx: 'tonal_accent', vol: 0.3, pan: 'R', fadeOut: 30, maxDur: 70, why: 'separação tonal: atenção'},
	// 09 — MAKE THEM CARE
	{scene: '09', at: K.futuro + 10, sfx: 'airy_sweep', vol: 0.18, pan: 'L', fadeIn: 10, fadeOut: 16, maxDur: 40, why: 'o fluxo se afasta'},
	{scene: '09', at: K.suficiente + 2, sfx: 'swipe_paper', vol: 0.34, why: 'risco atravessa "PRODUZIR MAIS"'},
	{scene: '09', at: K.suficiente + 44, sfx: 'reverse_swell', vol: 0.42, why: 'dolly para dentro do card'},
	{scene: '09', at: K.fazer + 2, sfx: 'click_single', vol: 0.36, why: 'FAZER compõe'},
	{scene: '09', at: K.alguem + 2, sfx: 'snap_elastic', vol: 0.38, why: 'ALGUÉM surge do espaço negativo'},
	{scene: '09', at: K.importar + 4, sfx: 'final_hit', vol: 0.55, fadeOut: 26, maxDur: 52, why: 'warm tonal hit + cauda aérea'},
	{scene: '09', at: K.importar + 4, sfx: 'sub_tail', vol: 0.4, fadeOut: 26, maxDur: 52, why: 'soft sub sob o impacto final'},
];

// Trilha: textura tonal da própria biblioteca Ocular (Granular Drones), discreta.
export const BED = {
	sfx: 'bed' as SfxId,
	// envelope [frame, volume]
	env: [
		[0, 0],
		[20, 0.1],
		[K.incrivelWall - 10, 0.12],
		[K.tudoIncrivel, 0.04],
		[K.still, 0],
		[K.splitLine, 0],
		[K.fork + 10, 0.07],
		[K.futuro, 0.09],
		[K.importar, 0.12],
		[1338, 0],
	] as [number, number][],
	why: 'cama tonal clara; some no paradoxo para o silêncio ter peso',
};

// Locução: coloque o arquivo em public/audio/voiceover.wav e mude para true.
export const VOICEOVER = {enabled: false, file: 'audio/voiceover.wav', vol: 1, duck: 0.55};
