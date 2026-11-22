// Roteiro visual da legenda. Posições em "u" = largura do rosto, a partir do centro do rosto.
// Tudo CENTRALIZADO em volta do rosto: nunca na frente do rosto, nunca colado nele, nunca no teto nem nas bordas.
// Zonas:
//   palavra-chave gigante → atrás da cabeça, na altura do topo (y ≈ −0.8)
//   palavras comuns      → ao lado do pescoço/ombros (y +0.85 / +1.35) e centro do peito (y +1.85)
//   ao lado da cabeça     → (y −0.75 / −0.25) só quando o bloco não tem chave atrás da cabeça
// Linhas: side L = borda direita da linha em x (à esquerda do rosto), R = borda esquerda em x, C = centralizada.

export type Line = {side: 'L' | 'R' | 'C'; x?: number; y: number; words: number[]; size?: number; rot?: number; italic?: boolean; accent?: boolean};
export type Key = {
  i: number;
  type: 'big' | 'arc' | 'scatter' | 'type';
  layer: 'behind' | 'front';
  x?: number;
  y?: number;
  size: number;
  rot?: number;
  arc?: {r: number; side: 'top' | 'bottom'};
  shake?: boolean;
  rgb?: boolean;
  text?: string; // texto exibido (maiúsculas, sem pontuação)
};
export type Bloco = {lines: Line[]; keys: Key[]; punch?: boolean};

const B1 = 0.85; // ao lado do pescoço
const B2 = 1.42; // ao lado dos ombros
const B3 = 2.02; // centro do peito
const S1 = -0.75; // ao lado da cabeça (alto)
const S2 = -0.25; // ao lado da cabeça (baixo)
const KEY_Y = -0.8; // palavra-chave gigante atrás do topo da cabeça

export const BLOCOS: Bloco[] = [
  // Só mais um teste dos MILHÕES que eu tô fazendo,
  {
    lines: [
      {side: 'L', y: B1, words: [0, 1]},
      {side: 'L', y: B2, words: [2, 3], size: 0.56},
      {side: 'R', y: B1, words: [4]},
      {side: 'R', y: B2, words: [6, 7, 8]},
      {side: 'C', y: B3, words: [9], size: 0.58, italic: true},
    ],
    keys: [{i: 5, type: 'big', layer: 'behind', y: KEY_Y, size: 1.3, text: 'MILHÕES'}],
    punch: true,
  },
  // a brincadeira tá começando a ficar DIVERTIDA.
  {
    lines: [
      {side: 'L', y: S1, words: [10]},
      {side: 'R', y: S1, words: [12]},
      {side: 'C', y: 0.95, words: [11], size: 0.6, rot: -4},
      {side: 'C', y: 1.45, words: [13, 14, 15], size: 0.5},
    ],
    keys: [{i: 16, type: 'scatter', layer: 'front', y: 2.1, size: 0.85, text: 'DIVERTIDA'}],
  },
  // Já montei o GPT Criador de Comando,
  {
    lines: [
      {side: 'L', y: B1, words: [17, 18]},
      {side: 'R', y: B1, words: [19]},
      {side: 'C', y: 1.55, words: [21, 22, 23], size: 0.54, italic: true},
    ],
    keys: [{i: 20, type: 'big', layer: 'behind', y: KEY_Y, size: 1.6, text: 'GPT'}],
    punch: true,
  },
  // tô literalmente só jogando a imagem de REFERÊNCIA,
  {
    lines: [
      {side: 'L', y: B1, words: [24]},
      {side: 'L', y: B2, words: [25], size: 0.52, rot: -4},
      {side: 'R', y: B1, words: [26]},
      {side: 'R', y: B2, words: [27]},
      {side: 'C', y: B3, words: [28, 29, 30], size: 0.52},
    ],
    keys: [{i: 31, type: 'big', layer: 'behind', y: -0.9, size: 0.95, rot: -7, rgb: true, text: 'REFERÊNCIA'}],
  },
  // ESCREVENDO um pouco do que eu QUERO,
  {
    lines: [
      {side: 'L', y: B1, words: [33, 34]},
      {side: 'R', y: B1, words: [35, 36, 37]},
    ],
    keys: [
      {i: 32, type: 'type', layer: 'front', y: 1.6, size: 0.6, text: 'ESCREVENDO'},
      {i: 38, type: 'big', layer: 'behind', y: KEY_Y, size: 1.4, text: 'QUERO'},
    ],
  },
  // o restante o próprio GPT FAZ,
  {
    lines: [
      {side: 'L', y: B1, words: [39, 40]},
      {side: 'R', y: B1, words: [41, 42]},
      {side: 'C', y: 1.55, words: [43], size: 0.7, accent: true},
    ],
    keys: [{i: 44, type: 'big', layer: 'behind', y: KEY_Y, size: 1.6, shake: true, text: 'FAZ'}],
    punch: true,
  },
  // cria a CENA, coloca as INTERAÇÕES,
  {
    lines: [
      {side: 'L', y: B1, words: [45, 46]},
      {side: 'R', y: B1, words: [48, 49]},
    ],
    keys: [
      {i: 47, type: 'big', layer: 'behind', y: KEY_Y, size: 1.5, text: 'CENA'},
      {i: 50, type: 'big', layer: 'front', y: 1.6, size: 0.62, text: 'INTERAÇÕES'},
    ],
  },
  // cria os movimentos de CÂMERA,
  {
    lines: [
      {side: 'L', y: B1, words: [51, 52]},
      {side: 'L', y: B2, words: [53], size: 0.54, rot: -5},
      {side: 'R', y: B1, words: [54]},
    ],
    keys: [{i: 55, type: 'arc', layer: 'behind', size: 0.85, arc: {r: 1.3, side: 'top'}, text: 'CÂMERA'}],
  },
  // tá ficando FÁCIL.
  {
    lines: [
      {side: 'L', y: B1, words: [56]},
      {side: 'R', y: B1, words: [57], size: 0.56, italic: true},
    ],
    keys: [{i: 58, type: 'scatter', layer: 'behind', y: KEY_Y, size: 1.35, text: 'FÁCIL'}],
    punch: true,
  },
  // DEMOREI pra pegar, demorei pra entender
  {
    lines: [
      {side: 'L', y: B1, words: [60]},
      {side: 'L', y: B2, words: [61], size: 0.54},
      {side: 'R', y: B1, words: [62], size: 0.54, italic: true},
      {side: 'R', y: B2, words: [63, 64]},
    ],
    keys: [{i: 59, type: 'big', layer: 'behind', y: KEY_Y, size: 1.2, text: 'DEMOREI'}],
  },
  // quais FERRAMENTAS usar,
  {
    lines: [
      {side: 'L', y: B1, words: [65]},
      {side: 'R', y: B1, words: [67], size: 0.58, italic: true},
    ],
    keys: [{i: 66, type: 'arc', layer: 'behind', size: 0.72, arc: {r: 1.45, side: 'top'}, text: 'FERRAMENTAS'}],
  },
  // mas daqui a pouco eu LITERALMENTE
  {
    lines: [
      {side: 'L', y: S1, words: [68, 69]},
      {side: 'L', y: S2, words: [70, 71], size: 0.52},
      {side: 'R', y: S1, words: [72]},
    ],
    keys: [{i: 73, type: 'big', layer: 'front', y: 1.3, size: 0.6, rot: 4, text: 'LITERALMENTE'}],
  },
  // nem vou mais usar uma CÂMERA,
  {
    lines: [
      {side: 'L', y: B1, words: [74, 75]},
      {side: 'L', y: B2, words: [76], size: 0.54},
      {side: 'R', y: B1, words: [77]},
      {side: 'R', y: B2, words: [78]},
    ],
    keys: [{i: 79, type: 'big', layer: 'behind', y: KEY_Y, size: 1.25, rgb: true, text: 'CÂMERA'}],
    punch: true,
  },
  // porque NÃO PRECISA mesmo.
  {
    lines: [
      {side: 'L', y: B1, words: [80]},
      {side: 'R', y: B1, words: [81], size: 0.66, accent: true},
      {side: 'C', y: B3, words: [83], size: 0.58, italic: true},
    ],
    keys: [{i: 82, type: 'big', layer: 'behind', y: KEY_Y, size: 1.25, shake: true, text: 'PRECISA'}],
    punch: true,
  },
];
