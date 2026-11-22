import {Config} from '@remotion/cli/config';

// máscaras e cópia do vídeo ficam fora do Dropbox
// public fora de pasta sincronizada: ajuste para a pasta temporária do projeto
Config.setPublicDir(process.env.LEGENDA_PUBLIC ?? 'public');
Config.setChromiumOpenGlRenderer('angle');
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
