// Render determinístico do index.html em 60 fps com motion blur real (subquadros + obturador 180°), via Edge.
// Projeto: <pasta>/index.html (cópia do template), <pasta>/fonts, <pasta>/audio e este script em <pasta>/scripts.
// uso:
//   node scripts/render.mjs stills <pasta> 0.5,3.2,8.0        → PNGs de conferência
//   node scripts/render.mjs cues   <arquivo.json>              → exporta as cues de SFX
//   node scripts/render.mjs all    <pastaFrames> <saida.mp4> [workers] [sub]
import {chromium} from 'playwright-core';
import path from 'node:path';
import fs from 'node:fs';
import {spawn, execFileSync} from 'node:child_process';
import {fileURLToPath, pathToFileURL} from 'node:url';
import ffmpeg from 'ffmpeg-static';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(here, '..');
// navegador: Edge/Chrome instalados (Windows/macOS/Linux) ou o Chromium do Playwright (npx playwright install chromium)
const BROWSERS = [process.env.BROWSER,
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', 'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Google/Chrome/Application/chrome.exe', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge', '/usr/bin/chromium', '/usr/bin/google-chrome'].filter(Boolean);
const EXE = BROWSERS.find((b) => fs.existsSync(b));
const FPS = +(process.env.FPS || 30), SHUTTER = +(process.env.SHUTTER || 0.9);
const [mode, out, a3, a4, a5, a6] = process.argv.slice(2);

async function open() {
  const browser = await chromium.launch({...(EXE ? {executablePath: EXE} : {}), args: ['--force-color-profile=srgb', '--hide-scrollbars', '--disable-lcd-text', '--font-render-hinting=none']});
  const page = await browser.newPage({viewport: {width: 1080, height: 1920}, deviceScaleFactor: 1});
  page.on('pageerror', (e) => console.error('PAGEERROR', e.message));
  page.on('console', (m) => m.type() === 'error' && console.error('CONSOLE', m.text()));
  await page.goto(pathToFileURL(path.join(root, process.env.PAGE || 'index.html')).href + '?render=1' + (process.env.Q ? '&' + process.env.Q : ''));
  await page.waitForFunction(() => window.ready);
  await page.evaluate(() => window.ready);
  return {browser, page};
}
const shot = (page, t, file, type = 'jpeg') =>
  page.evaluate((t) => window.seek(t), t).then(() =>
    page.screenshot({path: file, type, ...(type === 'jpeg' ? {quality: 94} : {}), clip: {x: 0, y: 0, width: 1080, height: 1920}}));

if (mode === 'stills') {
  fs.mkdirSync(out, {recursive: true});
  const {browser, page} = await open();
  for (const t of a3.split(',').map(Number)) await shot(page, t, path.join(out, `s_${t.toFixed(2).padStart(6, '0')}.png`), 'png');
  await browser.close();
} else if (mode === 'frames') { // interno: out, ini, fim, sub
  const SUB = +a5;
  const {browser, page} = await open();
  for (let i = +a3; i < +a4; i++)
    for (let k = 0; k < SUB; k++) {
      const t = i / FPS + ((k + 0.5) / SUB - 0.5) * SHUTTER / FPS;
      await shot(page, Math.max(0, t), path.join(out, `f_${String(i * SUB + k).padStart(6, '0')}.jpg`));
    }
  await browser.close();
} else if (mode === 'cues') {
  const {browser, page} = await open();
  const data = await page.evaluate(() => ({duration: window.DURATION, cues: window.CUES}));
  fs.writeFileSync(out, JSON.stringify(data, null, 1));
  console.log(`${data.cues.length} cues → ${out}`);
  await browser.close();
} else if (mode === 'all') {
  const {browser, page} = await open();
  const dur = await page.evaluate(() => window.DURATION);
  await browser.close();
  const total = Math.round(dur * FPS), W = +(a4 || 10), SUB = +(a5 || 8);
  fs.rmSync(out, {recursive: true, force: true});
  fs.mkdirSync(out, {recursive: true});
  const per = Math.ceil(total / W);
  const t0 = Date.now();
  await Promise.all([...Array(W)].map((_, w) => new Promise((res, rej) => {
    const ini = w * per, fim = Math.min(total, ini + per);
    const p = spawn(process.execPath, [path.join(here, 'render.mjs'), 'frames', out, String(ini), String(fim), String(SUB)], {stdio: 'inherit'});
    p.on('exit', (c) => (c ? rej(new Error('worker ' + w)) : res()));
  })));
  console.log(`${total} quadros × ${SUB} subquadros em ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  execFileSync(ffmpeg, ['-nostdin', '-y', '-loglevel', 'error', '-framerate', String(FPS * SUB), '-i', path.join(out, 'f_%06d.jpg'),
    '-vf', `tmix=frames=${SUB},select='eq(mod(n\,${SUB})\,${SUB - 1})',setpts=N/(${FPS}*TB)`, '-r', String(FPS),
    '-c:v', 'libx264', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-crf', '15', '-movflags', '+faststart', a3], {stdio: 'inherit'});
  console.log('vídeo →', a3);
}
