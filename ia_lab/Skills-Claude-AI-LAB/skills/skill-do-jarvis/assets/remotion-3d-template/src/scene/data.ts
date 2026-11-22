// Planta do apartamento em metros. x = largura (esq → dir), z = profundidade (topo da planta → base).
// Área interna: x[-4, 4] · z[-5, 5] = 80 m²

export type Seg = [number, number, number, number];

export const WALL_H = 2.6;
export const WALL_T = 0.16;

// Paredes (com vãos de porta já descontados)
export const WALLS: Seg[] = [
  [-4, -5, 4, -5], // fundo
  [-4, -5, -4, 5], // esquerda
  [4, -5, 4, 5], // direita
  [-4, 5, -3.2, 5], // frente (antes da janela)
  [-0.2, 5, 4, 5], // frente (depois da janela)
  [-4, 0.5, 0.5, 0.5], // quarto | sala
  [0.5, -5, 0.5, -1.6], // quarto | banho/hall
  [0.5, -0.6, 0.5, 0.5], // quarto | hall (depois da porta)
  [0.5, -2.2, 1.4, -2.2], // banho | hall
  [2.2, -2.2, 4, -2.2], // banho | hall (depois da porta)
  [3.2, 0.5, 4, 0.5], // mureta hall | cozinha
];

export const GLASS: Seg[] = [[-3.2, 5, -0.2, 5]];

export type FloorKind = 'wood' | 'tile' | 'stone';
export type Room = {
  name: string;
  area: string;
  x: [number, number];
  z: [number, number];
  floor: FloorKind;
  label: [number, number];
};

export const ROOMS: Room[] = [
  {name: 'QUARTO', area: '24,7 m²', x: [-4, 0.5], z: [-5, 0.5], floor: 'wood', label: [-1.75, -2.0]},
  {name: 'BANHO', area: '9,8 m²', x: [0.5, 4], z: [-5, -2.2], floor: 'tile', label: [2.25, -3.4]},
  {name: 'HALL', area: '9,4 m²', x: [0.5, 4], z: [-2.2, 0.5], floor: 'stone', label: [2.25, -0.8]},
  {name: 'SALA', area: '24,7 m²', x: [-4, 1.5], z: [0.5, 5], floor: 'wood', label: [-1.4, 2.0]},
  {name: 'COZINHA', area: '11,2 m²', x: [1.5, 4], z: [0.5, 5], floor: 'stone', label: [2.6, 1.3]},
];

export type MatKey =
  | 'white'
  | 'graphite'
  | 'wood'
  | 'woodDark'
  | 'fabric'
  | 'fabricDark'
  | 'lime'
  | 'metal'
  | 'ceramic'
  | 'glass'
  | 'plant'
  | 'screen'
  | 'lamp';

// box: p = [x, base y, z], s = [w, h, d] · cyl: s = [raio, altura] · sph: p = centro, s = [raio]
export type Part =
  | {t: 'box'; p: [number, number, number]; s: [number, number, number]; m: MatKey}
  | {t: 'cyl'; p: [number, number, number]; s: [number, number]; m: MatKey}
  | {t: 'sph'; p: [number, number, number]; s: [number]; m: MatKey};

export type Item = {
  name: string;
  x: number;
  z: number;
  fp: [number, number]; // pegada na planta (w, d)
  mode: 'rise' | 'drop';
  parts: Part[];
};

const B = (x: number, y: number, z: number, w: number, h: number, d: number, m: MatKey): Part => ({
  t: 'box',
  p: [x, y, z],
  s: [w, h, d],
  m,
});
const C = (x: number, y: number, z: number, r: number, h: number, m: MatKey): Part => ({
  t: 'cyl',
  p: [x, y, z],
  s: [r, h],
  m,
});
const S = (x: number, y: number, z: number, r: number, m: MatKey): Part => ({t: 'sph', p: [x, y, z], s: [r], m});

// Ordem = ordem de montagem
export const ITEMS: Item[] = [
  // tapetes primeiro (base da composição)
  {name: 'tapete-sala', x: -2.2, z: 3.2, fp: [3.0, 2.2], mode: 'rise', parts: [B(0, 0, 0, 3.0, 0.025, 2.2, 'fabricDark')]},
  {name: 'tapete-quarto', x: -2.0, z: -1.7, fp: [2.4, 1.3], mode: 'rise', parts: [B(0, 0, 0, 2.4, 0.025, 1.3, 'fabric')]},
  // quarto
  {
    name: 'cama',
    x: -2.0,
    z: -3.8,
    fp: [1.9, 2.3],
    mode: 'rise',
    parts: [
      B(0, 0, 0.1, 1.7, 0.32, 2.1, 'woodDark'),
      B(0, 0.32, 0.15, 1.6, 0.22, 1.95, 'white'),
      B(0, 0.54, 0.5, 1.66, 0.07, 1.3, 'fabricDark'),
      B(-0.4, 0.54, -0.6, 0.6, 0.14, 0.34, 'white'),
      B(0.4, 0.54, -0.6, 0.6, 0.14, 0.34, 'white'),
      B(0, 0.54, -0.35, 0.5, 0.12, 0.22, 'lime'),
      B(0, 0, -1.05, 1.9, 1.05, 0.1, 'fabric'),
    ],
  },
  {
    name: 'criado-e',
    x: -3.4,
    z: -4.6,
    fp: [0.5, 0.45],
    mode: 'drop',
    parts: [B(0, 0, 0, 0.5, 0.45, 0.42, 'wood'), C(0, 0.45, 0, 0.05, 0.28, 'metal'), S(0, 0.86, 0, 0.14, 'lamp')],
  },
  {
    name: 'criado-d',
    x: -0.6,
    z: -4.6,
    fp: [0.5, 0.45],
    mode: 'drop',
    parts: [B(0, 0, 0, 0.5, 0.45, 0.42, 'wood'), C(0, 0.45, 0, 0.05, 0.28, 'metal'), S(0, 0.86, 0, 0.14, 'lamp')],
  },
  {
    name: 'guarda-roupa',
    x: -3.6,
    z: -1.3,
    fp: [0.62, 2.3],
    mode: 'rise',
    parts: [
      B(0, 0, 0, 0.62, 2.3, 2.3, 'white'),
      B(0.32, 0.9, -0.38, 0.03, 0.5, 0.03, 'metal'),
      B(0.32, 0.9, 0.38, 0.03, 0.5, 0.03, 'metal'),
    ],
  },
  // banho
  {
    name: 'vaso',
    x: 1.3,
    z: -4.55,
    fp: [0.45, 0.65],
    mode: 'drop',
    parts: [B(0, 0, 0.05, 0.38, 0.42, 0.55, 'ceramic'), B(0, 0, -0.24, 0.42, 0.78, 0.16, 'ceramic')],
  },
  {
    name: 'pia',
    x: 2.5,
    z: -4.65,
    fp: [1.2, 0.5],
    mode: 'rise',
    parts: [
      B(0, 0, 0, 1.2, 0.85, 0.5, 'wood'),
      B(0, 0.85, 0.02, 0.5, 0.1, 0.36, 'ceramic'),
      B(0, 1.15, -0.23, 0.9, 0.75, 0.025, 'glass'),
    ],
  },
  {
    name: 'chuveiro',
    x: 3.45,
    z: -3.0,
    fp: [1.0, 1.3],
    mode: 'rise',
    parts: [
      B(0, 0, 0, 1.0, 0.06, 1.3, 'ceramic'),
      B(-0.5, 0.06, 0, 0.025, 1.95, 1.3, 'glass'),
      C(0.35, 2.05, 0, 0.13, 0.03, 'metal'),
    ],
  },
  // hall
  {
    name: 'aparador',
    x: 2.6,
    z: -1.95,
    fp: [1.4, 0.36],
    mode: 'drop',
    parts: [B(0, 0, 0, 1.4, 0.8, 0.36, 'wood'), C(0.4, 0.8, 0, 0.09, 0.32, 'lime'), S(-0.3, 0.92, 0, 0.12, 'ceramic')],
  },
  // sala
  {
    name: 'sofa',
    x: -2.2,
    z: 4.35,
    fp: [2.8, 1.0],
    mode: 'rise',
    parts: [
      B(0, 0, 0, 2.7, 0.42, 0.95, 'fabric'),
      B(0, 0.42, 0.38, 2.7, 0.45, 0.2, 'fabric'),
      B(-1.27, 0.42, 0, 0.16, 0.22, 0.95, 'fabric'),
      B(1.27, 0.42, 0, 0.16, 0.22, 0.95, 'fabric'),
      B(-0.75, 0.45, 0.18, 0.42, 0.38, 0.12, 'lime'),
      B(0.6, 0.45, 0.18, 0.42, 0.38, 0.12, 'fabricDark'),
    ],
  },
  {
    name: 'mesa-centro',
    x: -2.2,
    z: 3.1,
    fp: [1.1, 0.6],
    mode: 'drop',
    parts: [B(0, 0, 0, 0.9, 0.3, 0.42, 'graphite'), B(0, 0.3, 0, 1.1, 0.06, 0.6, 'wood'), S(0.25, 0.43, 0, 0.07, 'lime')],
  },
  {
    name: 'rack-tv',
    x: -2.2,
    z: 0.82,
    fp: [2.2, 0.42],
    mode: 'rise',
    parts: [B(0, 0, 0, 2.2, 0.45, 0.42, 'graphite'), B(0, 0.75, -0.08, 1.65, 0.95, 0.05, 'screen')],
  },
  {
    name: 'planta',
    x: -3.5,
    z: 4.5,
    fp: [0.5, 0.5],
    mode: 'drop',
    parts: [C(0, 0, 0, 0.22, 0.45, 'graphite'), S(0, 0.95, 0, 0.42, 'plant'), S(0.12, 1.35, 0.05, 0.28, 'plant')],
  },
  {
    name: 'luminaria',
    x: -0.5,
    z: 4.5,
    fp: [0.4, 0.4],
    mode: 'drop',
    parts: [C(0, 0, 0, 0.16, 0.03, 'metal'), C(0, 0, 0, 0.02, 1.5, 'metal'), S(0, 1.62, 0, 0.18, 'lamp')],
  },
  // cozinha
  {
    name: 'bancada',
    x: 3.68,
    z: 2.4,
    fp: [0.62, 3.2],
    mode: 'rise',
    parts: [
      B(0, 0, 0, 0.6, 0.88, 3.2, 'white'),
      B(0, 0.88, 0, 0.64, 0.04, 3.24, 'graphite'),
      B(0, 0.92, 0.6, 0.5, 0.01, 0.55, 'screen'),
      B(0, 0.9, -0.7, 0.42, 0.03, 0.5, 'metal'),
    ],
  },
  {name: 'geladeira', x: 3.62, z: 4.5, fp: [0.72, 0.72], mode: 'rise', parts: [B(0, 0, 0, 0.72, 1.95, 0.72, 'metal')]},
  {
    name: 'ilha',
    x: 2.25,
    z: 2.6,
    fp: [0.96, 1.9],
    mode: 'rise',
    parts: [B(0, 0, 0, 0.9, 0.9, 1.9, 'wood'), B(0, 0.9, 0, 0.98, 0.05, 1.98, 'white')],
  },
  {
    name: 'banquetas',
    x: 1.45,
    z: 2.6,
    fp: [0.4, 1.6],
    mode: 'drop',
    parts: [
      C(0, 0, -0.6, 0.17, 0.68, 'graphite'),
      C(0, 0, 0, 0.17, 0.68, 'graphite'),
      C(0, 0, 0.6, 0.17, 0.68, 'graphite'),
    ],
  },
];
