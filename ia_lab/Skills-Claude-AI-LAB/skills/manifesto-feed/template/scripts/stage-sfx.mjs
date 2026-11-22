// Prepara os SFX em public/ocular (wav 48k estéreo) e mede duração/pico de cada um.
// Ordem de busca da biblioteca: variável SFX_ROOT → "roots" do sfx-sources.json (Windows/Mac do Lucas).
// Sem a biblioteca Ocular (ex.: comprador do pack), cada som é SINTETIZADO por ffmpeg com o mesmo id,
// pra o vídeo renderizar igual. Para trocar por sons seus: aponte SFX_ROOT e edite "files".
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import ffmpeg from 'ffmpeg-static';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = JSON.parse(fs.readFileSync(path.join(here, 'sfx-sources.json'), 'utf8'));
const outDir = path.join(here, '..', 'public', 'ocular');
fs.mkdirSync(outDir, {recursive: true});

const roots = [process.env.SFX_ROOT, ...(src.roots ?? [])].filter(Boolean);
const root = roots.find((r) => fs.existsSync(r));
console.log(root ? `biblioteca: ${root}` : 'biblioteca Ocular não encontrada → sintetizando os SFX');

// receitas de síntese (lavfi) por família de som; d = duração em s
const SYN = {
	click: (d) => `anoisesrc=d=${d}:c=white:a=0.9,highpass=f=2500,afade=t=out:st=0.004:d=${d - 0.004}`,
	pop: (d) => `sine=f=900:d=${d},afade=t=out:st=0.01:d=${d - 0.01}`,
	beep: (d) => `sine=f=2200:d=${d},afade=t=out:st=0.03:d=${d - 0.03}`,
	whip: (d) => `anoisesrc=d=${d}:c=pink:a=0.8,bandpass=f=1800:w=1500,afade=t=in:d=${d * 0.6},afade=t=out:st=${d * 0.6}:d=${d * 0.4}`,
	swipe: (d) => `anoisesrc=d=${d}:c=brown:a=0.9,highpass=f=300,afade=t=in:d=${d * 0.5},afade=t=out:st=${d * 0.5}:d=${d * 0.5}`,
	air: (d) => `anoisesrc=d=${d}:c=white:a=0.5,lowpass=f=6000,afade=t=in:d=${d * 0.4},afade=t=out:st=${d * 0.5}:d=${d * 0.5}`,
	impact: (d) => `sine=f=55:d=${d},afade=t=out:st=0.02:d=${d - 0.02}`,
	tonal: (d) => `sine=f=698:d=${d},afade=t=in:d=0.01,afade=t=out:st=0.05:d=${d - 0.05}`,
	riser: (d) => `sine=f=440:d=${d},vibrato=f=8:d=0.3,afade=t=in:d=${d * 0.9}`,
	tick: (d) => `sine=f=3000:d=${d},apulsator=hz=8:amount=1,volume=0.5`,
	bed: (d) => `sine=f=196:d=${d},volume=0.25`,
};
const FAM = {
	click_short: ['click', 0.15], click_single: ['click', 0.15], click_metal: ['click', 0.1], pop_soft: ['pop', 0.12], snap_elastic: ['click', 0.2],
	beep_tick: ['beep', 0.15], whip_a: ['whip', 0.45], whip_b: ['whip', 0.4], whip_c: ['whip', 0.5], whip_d: ['whip', 0.4],
	swipe_paper: ['swipe', 0.6], swipe_rl: ['swipe', 0.7], swipe_sand: ['swipe', 0.7], whoosh_exhale: ['air', 0.9], reverse_swell: ['riser', 1.6],
	airy_sweep: ['air', 2.5], impact_soft: ['impact', 1.2], impact_low: ['impact', 2.0], gears: ['tick', 2.0], ticking_loop: ['tick', 6.0],
	mech_lock: ['click', 0.35], tonal_accent: ['tonal', 2.0], riser_pulse: ['riser', 6.0], riser_sparkle: ['riser', 1.5], glitch: ['click', 0.3],
	final_hit: ['impact', 2.5], sub_tail: ['impact', 2.5], bed: ['bed', 20],
};

const meta = {};
for (const [id, rel] of Object.entries(src.files)) {
	const out = path.join(outDir, `${id}.wav`);
	const inPath = root ? path.join(root, rel) : null;
	if (inPath && fs.existsSync(inPath)) {
		execFileSync(ffmpeg, ['-nostdin', '-y', '-loglevel', 'error', '-i', inPath, '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', out]);
	} else {
		const [fam, d] = FAM[id] ?? ['click', 0.15];
		if (root) console.error('FALTA na biblioteca, sintetizando:', id);
		execFileSync(ffmpeg, ['-nostdin', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', SYN[fam](d), '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', out]);
	}
	const buf = fs.readFileSync(out);
	const dataIdx = buf.indexOf('data') + 8;
	const n = Math.floor((buf.length - dataIdx) / 4);
	let peak = 1, peakAt = 0, firstLoud = 0;
	for (let i = 0; i < n; i++) {
		const v = Math.max(Math.abs(buf.readInt16LE(dataIdx + i * 4)), Math.abs(buf.readInt16LE(dataIdx + i * 4 + 2)));
		if (v > peak) { peak = v; peakAt = i; }
	}
	for (let i = 0; i < n; i++) if (Math.abs(buf.readInt16LE(dataIdx + i * 4)) > peak * 0.25) { firstLoud = i; break; }
	meta[id] = {
		source: inPath && fs.existsSync(inPath) ? rel : `sintetizado (${(FAM[id] ?? ['click'])[0]})`,
		duration: +(n / 48000).toFixed(3),
		peakSec: +(peakAt / 48000).toFixed(3),
		onsetSec: +(firstLoud / 48000).toFixed(3),
		peakDb: +(20 * Math.log10(peak / 32768)).toFixed(1),
	};
	console.log(id.padEnd(15), JSON.stringify(meta[id]).slice(0, 140));
	// variantes com posição estéreo (L/R) para os sons espaciais
	if (src.panned.includes(id)) {
		execFileSync(ffmpeg, ['-nostdin', '-y', '-loglevel', 'error', '-i', out, '-af', 'pan=stereo|c0=1.0*c0+0.35*c1|c1=0.35*c1', path.join(outDir, `${id}_L.wav`)]);
		execFileSync(ffmpeg, ['-nostdin', '-y', '-loglevel', 'error', '-i', out, '-af', 'pan=stereo|c0=0.35*c0|c1=1.0*c1+0.35*c0', path.join(outDir, `${id}_R.wav`)]);
	}
}
fs.writeFileSync(path.join(here, '..', 'src', 'data', 'sfx-meta.json'), JSON.stringify(meta, null, 2));
