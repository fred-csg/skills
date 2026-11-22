import {Composition, Folder} from 'remotion';
import {Planta3D} from './Planta3D';
import {LookName} from './scene/looks';

const LOOK_NAMES: LookName[] = ['vidro', 'fosco', 'cromado', 'holograma'];
const base = {component: Planta3D, durationInFrames: 450, fps: 30, width: 1080, height: 1920};

export const Root = () => (
  <>
    <Composition id="Planta3D" {...base} defaultProps={{look: 'vidro' as LookName}} />
    <Folder name="Looks">
      {LOOK_NAMES.map((l) => (
        <Composition key={l} id={`Planta3D-${l}`} {...base} defaultProps={{look: l}} />
      ))}
    </Folder>
  </>
);
