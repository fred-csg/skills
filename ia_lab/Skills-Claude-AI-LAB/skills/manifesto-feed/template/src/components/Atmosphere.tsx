import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';

/** Grão de filme determinístico + vinheta. Dá textura sem poluir. */
export const Atmosphere: React.FC<{grain?: number}> = ({grain = 0.06}) => {
	const f = useCurrentFrame();
	const seed = (f % 12) + 1;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<AbsoluteFill
				style={{background: 'radial-gradient(ellipse 85% 70% at 50% 48%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)'}}
			/>
			<svg width="100%" height="100%" style={{position: 'absolute', opacity: grain, mixBlendMode: 'screen'}}>
				<filter id={`g${seed}`}>
					<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={seed} stitchTiles="stitch" />
					<feColorMatrix type="saturate" values="0" />
				</filter>
				<rect width="100%" height="100%" filter={`url(#g${seed})`} />
			</svg>
		</AbsoluteFill>
	);
};
