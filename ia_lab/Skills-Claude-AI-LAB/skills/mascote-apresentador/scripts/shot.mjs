import {chromium} from 'playwright-core';
import {pathToFileURL} from 'node:url';
const [file, out, w, h] = process.argv.slice(2);
const b = await chromium.launch({executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
const p = await b.newPage({viewport: {width: +w, height: +h}});
await p.goto(pathToFileURL(file).href); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
await p.screenshot({path: out, type: 'jpeg', quality: 90}); await b.close();
