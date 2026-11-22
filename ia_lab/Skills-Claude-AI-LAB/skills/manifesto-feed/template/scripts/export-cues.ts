// Exporta o mapa de SFX para CSV (SFX_CUES.csv). Rodar: npm run cues
import fs from 'node:fs';
import {CUES, BED} from '../src/data/sfx-cues';
import meta from '../src/data/sfx-meta.json';

const tc = (fr: number) => `${Math.floor(fr / 30 / 60)}:${String(Math.floor(fr / 30) % 60).padStart(2, '0')}.${String(fr % 30).padStart(2, '0')}`;
const rows = [['cena', 'frame_evento', 'timecode', 'id', 'arquivo_ocular', 'volume', 'pan', 'fade_in_fr', 'fade_out_fr', 'duracao_max_fr', 'justificativa']];
for (const c of [...CUES].sort((a, b) => a.at - b.at)) {
	rows.push([c.scene, String(c.at), tc(c.at), c.sfx, meta[c.sfx].source, c.vol.toFixed(2), c.pan ?? 'C', String(c.fadeIn ?? 0), String(c.fadeOut ?? 0), String(c.maxDur ?? ''), c.why]);
}
rows.push(['todas', '0', '0:00.00', BED.sfx, meta[BED.sfx].source, 'envelope', 'C', '', '', '', BED.why]);
fs.writeFileSync('SFX_CUES.csv', rows.map((r) => r.map((v) => `"${v.replace(/"/g, '""')}"`).join(',')).join('\n'));
console.log(rows.length - 1, 'cues');
