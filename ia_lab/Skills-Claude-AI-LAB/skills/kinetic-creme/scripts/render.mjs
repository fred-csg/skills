// Render quadro a quadro: abre index.html no Chromium (headless), chama KC.seek(t) e manda cada PNG pro ffmpeg.
// uso: node render.mjs <pasta_com_index.html> <saida.mp4> [fps=30] [inicio=0] [fim=duração] [--frames dir] [--at 1,2.5,7]
//   --at  : só tira PNGs nesses instantes (pra revisar antes do render completo)
// Variáveis: CHROME (caminho do chrome.exe), FFMPEG (caminho do ffmpeg). Requer: npm i playwright-core
import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const args = process.argv.slice(2);
const flag = n => { const i = args.indexOf(n); if (i < 0) return null; const v = args[i + 1]; args.splice(i, 2); return v; };
const atList = flag('--at');
const [dir, out, fpsS = '30', t0S = '0', t1S] = args;
const fps = +fpsS;

function findChrome() {
  if (process.env.CHROME) return process.env.CHROME;
  const base = path.join(os.homedir(), 'AppData/Local/ms-playwright');
  // prefere o headless_shell (o chrome.exe completo pode ser bloqueado no Windows: "spawn UNKNOWN")
  if (fs.existsSync(base)) for (const d of fs.readdirSync(base).filter(d => /^chromium(_headless_shell)?-\d+$/.test(d)).sort((a, b) => (b.includes('headless') - a.includes('headless')) || b.localeCompare(a))) {
    for (const sub of ['chrome-headless-shell-win64/chrome-headless-shell.exe', 'chrome-headless-shell-linux64/chrome-headless-shell', 'chrome-win64/chrome.exe', 'chrome-win/chrome.exe', 'chrome-linux/chrome', 'chrome-mac/Chromium.app/Contents/MacOS/Chromium']) {
      const p = path.join(base, d, sub); if (fs.existsSync(p)) return p; } }
  return undefined; // deixa o playwright procurar
}
const FFMPEG = process.env.FFMPEG || 'ffmpeg';

const browser = await chromium.launch({ executablePath: findChrome(), args: ['--force-color-profile=srgb', '--disable-lcd-text'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.resolve(dir, 'index.html')).href + '?render=1');
await page.evaluate(() => window.KC_READY);
const dur = await page.evaluate(() => KC.duration);
fs.writeFileSync(path.join(path.dirname(path.resolve(out)), 'cues.json'), JSON.stringify(await page.evaluate(() => KC.cues), null, 1));

if (atList) {
  for (const t of atList.split(',').map(Number)) {
    await page.evaluate(t => KC.seek(t), t);
    await page.screenshot({ path: path.join(path.dirname(path.resolve(out)), `frame_${t.toFixed(2)}.png`) });
  }
  await browser.close(); process.exit(0);
}

const t0 = +t0S, t1 = t1S ? +t1S : dur, n = Math.round((t1 - t0) * fps);
const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const t = Date.now();
for (let i = 0; i < n; i++) {
  await page.evaluate(tt => KC.seek(tt), t0 + i / fps);
  const buf = await page.screenshot({ type: 'png' });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (i % 30 === 0) process.stdout.write(`\r${i}/${n}  ${((Date.now() - t) / 1000).toFixed(0)}s`);
}
ff.stdin.end(); await new Promise(r => ff.on('close', r));
await browser.close();
console.log(`\nok → ${out}  (${n} quadros em ${((Date.now() - t) / 1000).toFixed(0)}s)`);
