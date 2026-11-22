// Mix final com trilha: voz na frente (atrasada OFF s), SFX ~9 dB abaixo, trilha ~13 dB abaixo com ducking pela voz.
// Master em -14 LUFS / limitador. uso: node scripts/mix-musica.mjs <video-mudo> <sfx.wav> <voz> <trilha> <saida> [offVoz=0.08]
import {execFileSync, spawnSync} from 'node:child_process';
import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path';
import ffmpeg from 'ffmpeg-static';
const [video, sfx, vo, mus, out, off = '0.08'] = process.argv.slice(2);
const lufs = (f) => { const r = spawnSync(ffmpeg, ['-nostdin', '-hide_banner', '-i', f, '-af', 'loudnorm=print_format=json', '-f', 'null', '-'], {encoding: 'utf8'}); const m = r.stderr.match(/"input_i"\s*:\s*"(-?[\d.]+)"/); return m ? +m[1] : -20; };
const dur = +spawnSync(ffmpeg.replace(/ffmpeg(\.exe)?$/, 'ffmpeg$1'), ['-i', video], {encoding: 'utf8'}).stderr.match(/Duration: (\d+):(\d+):([\d.]+)/).slice(1).reduce((a, v, i) => a + v * [3600, 60, 1][i], 0);
const gv = -15 - lufs(vo), gs = -24 - lufs(sfx), gm = -28 - lufs(mus);
const ms = Math.round(+off * 1000);
const tmp = path.join(os.tmpdir(), `pm_${process.pid}.wav`);
execFileSync(ffmpeg, ['-nostdin', '-y', '-loglevel', 'error', '-i', vo, '-i', sfx, '-i', mus, '-filter_complex',
  `[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,highpass=f=70,volume=${gv.toFixed(2)}dB,adelay=${ms}|${ms},apad,asplit=3[v][k1][k2];` +
  `[1:a]aresample=48000,volume=${gs.toFixed(2)}dB[s0];[s0][k1]sidechaincompress=threshold=0.05:ratio=2.5:attack=15:release=300[s];` +
  `[2:a]aresample=48000,volume=${gm.toFixed(2)}dB,afade=t=out:st=${(dur - 1.2).toFixed(2)}:d=1.2[m0];[m0][k2]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=400[m];` +
  `[v][s][m]amix=inputs=3:normalize=0:duration=longest,atrim=0:${dur.toFixed(3)}[o]`, '-map', '[o]', '-c:a', 'pcm_s24le', tmp]);
const g = -14 - lufs(tmp);
execFileSync(ffmpeg, ['-nostdin', '-y', '-loglevel', 'error', '-i', video, '-i', tmp, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
  '-af', `volume=${g.toFixed(2)}dB,alimiter=limit=0.84:attack=3:release=80:level=disabled`, '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', out]);
fs.rmSync(tmp);
console.log(`final ${lufs(out)} LUFS → ${out}`);
