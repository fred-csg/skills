import React from 'react';
import {Composition} from 'remotion';
import {EP01} from './compositions/EP01';
import {FPS, H, W} from './lib/timing';
import {WARPED_DURATION} from './lib/timewarp';

export const RemotionRoot: React.FC = () => (
	<Composition id="EP01" component={EP01} durationInFrames={WARPED_DURATION} fps={FPS} width={W} height={H} />
);
