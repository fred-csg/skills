import React from 'react';
import {Audio, Sequence, interpolate, staticFile} from 'remotion';
import {BED, CUES, Cue, VOICEOVER} from '../data/sfx-cues';
import {VO} from '../data/script';
import meta from '../data/sfx-meta.json';
import {FPS} from '../lib/timing';
import {WARPED_DURATION as DURATION, unwarp} from '../lib/timewarp';

/** ducking: SFX e trilha abaixam enquanto a voz fala (só quando há locução) */
const duckAt = (frame: number) => {
	if (!VOICEOVER.enabled) return 1;
	const t = frame / FPS;
	return VO.some((l) => t >= unwarp(l.start * FPS) / FPS - 0.1 && t <= unwarp(l.end * FPS) / FPS + 0.15) ? VOICEOVER.duck : 1;
};

const CueAudio: React.FC<{c: Cue; i: number}> = ({c}) => {
	const m = meta[c.sfx];
	const trim = Math.round((c.trimSec ?? 0) * FPS);
	const offset = c.align === 'start' ? 0 : Math.round(m.peakSec * FPS);
	// o evento visual foi marcado no relógio original: converte para o novo; o som toca na velocidade natural
	const at = Math.round(unwarp(c.at));
	let from = at - offset;
	let trimBefore = trim;
	if (from < 0) {
		trimBefore += -from;
		from = 0;
	}
	const natural = Math.ceil(m.duration * FPS) - trimBefore;
	const maxDur = c.maxDur === undefined ? undefined : Math.max(4, Math.round(unwarp(c.at + c.maxDur) - unwarp(c.at)));
	const dur = Math.max(1, Math.min(natural, maxDur ?? natural, DURATION - from));
	const fi = c.fadeIn ?? 0;
	const fo = Math.min(c.fadeOut ?? (c.maxDur ? 6 : 0), Math.floor(dur / 2));
	const src = staticFile(`ocular/${c.sfx}${c.pan ? `_${c.pan}` : ''}.wav`);
	return (
		<Sequence from={from} durationInFrames={dur} layout="none">
			<Audio
				src={src}
				trimBefore={trimBefore || undefined}
				volume={(lf) => {
					const env = Math.min(fi ? interpolate(lf, [0, fi], [0, 1], {extrapolateRight: 'clamp'}) : 1, fo ? interpolate(lf, [dur - fo, dur], [1, 0], {extrapolateLeft: 'clamp'}) : 1);
					return c.vol * env * duckAt(from + lf);
				}}
			/>
		</Sequence>
	);
};

export const SoundTrack: React.FC = () => {
	const frames = BED.env.map((e) => unwarp(e[0]));
	const vols = BED.env.map((e) => e[1]);
	return (
		<>
			<Audio src={staticFile(`ocular/${BED.sfx}.wav`)} loop volume={(f) => interpolate(f, frames, vols, {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) * duckAt(f)} />
			{CUES.map((c, i) => (
				<CueAudio key={i} c={c} i={i} />
			))}
			{VOICEOVER.enabled && <Audio src={staticFile(VOICEOVER.file)} volume={VOICEOVER.vol} />}
		</>
	);
};
