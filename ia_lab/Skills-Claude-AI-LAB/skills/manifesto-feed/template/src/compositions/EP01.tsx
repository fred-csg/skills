import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C} from '../lib/theme';
import {E, prog} from '../lib/motion';
import {SCENES, SceneId} from '../lib/timing';
import {warp} from '../lib/timewarp';
import {K} from '../data/script';
import {Atmosphere} from '../components/Atmosphere';
import {Mono} from '../components/KineticTypography';
import {SoundTrack} from '../components/SoundTrack';
import {Flashes} from '../components/FX';
import {FLASHES} from '../data/fx';
import {S1Opinion} from '../scenes/S1Opinion';
import {S2Bigger} from '../scenes/S2Bigger';
import {S3Scroll} from '../scenes/S3Scroll';
import {S4Loop} from '../scenes/S4Loop';
import {S5Forces} from '../scenes/S5Forces';
import {S6Infinite} from '../scenes/S6Infinite';
import {S7Paradox} from '../scenes/S7Paradox';
import {S8Split} from '../scenes/S8Split';
import {S9Care} from '../scenes/S9Care';

// Ordem de empilhamento: a primeira fica embaixo.
const LAYERS: [SceneId, React.FC<{f: number}>][] = [
	['s3Scroll', S3Scroll],
	['s2Bigger', S2Bigger],
	['s1Opinion', S1Opinion],
	['s4Loop', S4Loop],
	['s5Forces', S5Forces],
	['s6Infinite', S6Infinite],
	['s7Paradox', S7Paradox],
	['s8Split', S8Split],
	['s9Care', S9Care],
];

/** assinatura discreta do episódio (some no silêncio do paradoxo) */
const Slate: React.FC<{f: number}> = ({f}) => {
	const op = 0.75 * (1 - prog(f, K.incrivelWall, K.incrivelWall + 20, E.linear));
	if (op <= 0) return null;
	return (
		<AbsoluteFill style={{top: 150, paddingLeft: 80, paddingRight: 80, flexDirection: 'row', justifyContent: 'space-between', opacity: op}}>
			<Mono style={{fontSize: 20}}>EP.01</Mono>
			<Mono style={{fontSize: 20}}>O FUTURO ESTÁ FICANDO DESCARTÁVEL</Mono>
		</AbsoluteFill>
	);
};

export const EP01: React.FC = () => {
	// as cenas vivem no relógio original; o ritmo final vem do time-warp
	const f = warp(useCurrentFrame());
	return (
		<AbsoluteFill style={{background: C.bg}}>
			{LAYERS.map(([id, Scene]) => {
				const [a, b] = SCENES[id];
				return f >= a && f < b ? <Scene key={id} f={f} /> : null;
			})}
			<Flashes f={f} events={FLASHES} />
			<Slate f={f} />
			<Atmosphere />
			<SoundTrack />
		</AbsoluteFill>
	);
};
