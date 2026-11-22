import {Config} from '@remotion/cli/config';

// GPU via ANGLE (Windows) para o three.js renderizar rápido
Config.setChromiumOpenGlRenderer('angle');
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
