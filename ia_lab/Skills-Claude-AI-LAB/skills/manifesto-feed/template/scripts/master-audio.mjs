// Masteriza o áudio do render: ganho + limitador (true peak -1.5 dBFS) e remux sem re-encodar o vídeo.
// uso: node scripts/master-audio.mjs entrada.mp4 saida.mp4 [ganho_dB]
import {execFileSync} from 'node:child_process';
import ffmpeg from 'ffmpeg-static';

const [inp, out, gain = '9'] = process.argv.slice(2);
execFileSync(ffmpeg, ['-nostdin', '-y', '-loglevel', 'error', '-i', inp, '-c:v', 'copy', '-af', `volume=${gain}dB,alimiter=limit=0.7:attack=3:release=60:level=disabled`, '-c:a', 'aac', '-b:a', '256k', out], {stdio: 'inherit'});
const r = execFileSync(ffmpeg, ['-nostdin', '-hide_banner', '-i', out, '-af', 'ebur128=peak=true', '-f', 'null', '-'], {encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe']}).toString();
console.log(r);
