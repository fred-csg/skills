import {Composition} from 'remotion';
import {DURATION, FPS, Legenda} from './Legenda';

export const Root = () => <Composition id="Legenda" component={Legenda} durationInFrames={DURATION} fps={FPS} width={1080} height={1920} />;
