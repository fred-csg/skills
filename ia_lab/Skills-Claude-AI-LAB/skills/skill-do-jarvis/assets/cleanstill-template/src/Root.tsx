import {Composition} from 'remotion';
import {CleanstillDemo, DEMO_FRAMES} from './CleanstillDemo';

// 16:9 = formato do vídeo de referência; 9:16 = Reels/Shorts (componentes se adaptam pela menor dimensão)
export const Root = () => (
  <>
    <Composition id="CleanstillDemo" component={CleanstillDemo} durationInFrames={DEMO_FRAMES} fps={30} width={1920} height={1080} />
    <Composition id="CleanstillDemo-9x16" component={CleanstillDemo} durationInFrames={DEMO_FRAMES} fps={30} width={1080} height={1920} />
  </>
);
