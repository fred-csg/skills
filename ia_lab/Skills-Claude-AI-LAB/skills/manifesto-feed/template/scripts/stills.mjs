// Renderiza frames de referência com um único bundle e monta uma folha de contato.
// uso: node scripts/stills.mjs <pasta-saida> <frame1> <frame2> ...   (frames do vídeo FINAL, após o time-warp)
import path from 'node:path';
import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import ffmpeg from 'ffmpeg-static';

const [out, ...frames] = process.argv.slice(2);
fs.mkdirSync(out, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const composition = await selectComposition({serveUrl, id: 'EP01'});
const files = [];
for (const fr of frames.map(Number)) {
	if (fr >= composition.durationInFrames) {
		console.log(`(pulando ${fr}: o vídeo tem ${composition.durationInFrames} frames)`);
		continue;
	}
	const file = path.resolve(out, `f${String(fr).padStart(4, '0')}.jpg`);
	await renderStill({serveUrl, composition, frame: fr, output: file, imageFormat: 'jpeg', scale: 0.4});
	files.push(file);
	process.stdout.write(`${fr} `);
}
// folha de contato (lista concat em vez de glob: funciona no Windows e no Mac)
const cols = Math.min(6, files.length);
const list = path.join(out, 'lista.txt');
fs.writeFileSync(list, files.map((f) => `file '${f.split(path.sep).join('/')}'`).join('\n'));
execFileSync(ffmpeg, ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-vf', `scale=270:480,tile=${cols}x${Math.ceil(files.length / cols)}:padding=6:color=gray`, '-frames:v', '1', path.join(out, 'sheet.jpg')]);
console.log(`\nok → ${path.join(out, 'sheet.jpg')}`);
