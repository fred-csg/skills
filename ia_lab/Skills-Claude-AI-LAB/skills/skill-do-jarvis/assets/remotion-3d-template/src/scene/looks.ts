import * as THREE from 'three';
import {MatKey} from './data';

export type LookName = 'vidro' | 'fosco' | 'cromado' | 'holograma';

export type Look = {
  name: LookName;
  label: string;
  accent: string; // borda/linhas/HUD
  bg: [string, string]; // gradiente do fundo (centro, borda)
  grid: string;
  gridOpacity: number;
  edges: number; // opacidade das arestas brilhantes (0 = sem)
  shadows: boolean;
  wall: () => THREE.Material;
  cap: () => THREE.Material;
  floor: () => THREE.Material;
  mats: () => Record<MatKey, THREE.Material>;
};

const phys = (p: THREE.MeshPhysicalMaterialParameters) => new THREE.MeshPhysicalMaterial(p);
const std = (p: THREE.MeshStandardMaterialParameters) => new THREE.MeshStandardMaterial(p);
const basic = (p: THREE.MeshBasicMaterialParameters) => new THREE.MeshBasicMaterial(p);

// vidro transmissivo: refrata o fundo azul de verdade (precisa de scene.background, não de canvas transparente)
const glass = (color: string, roughness: number, extra: THREE.MeshPhysicalMaterialParameters = {}) =>
  phys({
    color,
    transmission: 1,
    thickness: 0.35,
    ior: 1.45,
    roughness,
    metalness: 0,
    clearcoat: 1,
    clearcoatRoughness: 0.08,
    specularIntensity: 1,
    attenuationColor: '#9fc8ff',
    attenuationDistance: 3,
    ...extra,
  });

// textura de piso: placas finas com linhas claras (vale para todos os looks)
const floorLines = (base: string, line: string) => {
  const cv = document.createElement('canvas');
  cv.width = cv.height = 512;
  const c = cv.getContext('2d')!;
  c.fillStyle = base;
  c.fillRect(0, 0, 512, 512);
  c.strokeStyle = line;
  c.lineWidth = 2;
  for (let i = 0; i <= 512; i += 64) {
    c.beginPath();
    c.moveTo(i, 0);
    c.lineTo(i, 512);
    c.stroke();
    c.beginPath();
    c.moveTo(0, i);
    c.lineTo(512, i);
    c.stroke();
  }
  const t = new THREE.CanvasTexture(cv);
  t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(2, 2.5); // 64px = 0.5 m numa planta de 8x10
  t.anisotropy = 8;
  return t;
};

const NAVY: [string, string] = ['#13284f', '#050b1a'];

export const LOOKS: Record<LookName, Look> = {
  vidro: {
    name: 'vidro',
    label: 'VIDRO',
    accent: '#bfeaff',
    bg: NAVY,
    grid: '#ffffff',
    gridOpacity: 0.1,
    edges: 0.85,
    shadows: false,
    wall: () => glass('#e8f4ff', 0.04),
    cap: () => basic({color: '#e6f7ff', toneMapped: false, transparent: true}),
    floor: () => std({map: floorLines('#0c1a36', 'rgba(190,225,255,.16)'), roughness: 0.18, metalness: 0.55}),
    mats: () => ({
      white: glass('#f2f8ff', 0.08),
      graphite: glass('#7f93b8', 0.12),
      wood: glass('#cfe2ff', 0.25),
      woodDark: glass('#8ea6d4', 0.18),
      fabric: glass('#e6eefc', 0.45),
      fabricDark: glass('#6f84ad', 0.4),
      lime: std({color: '#D7FF3A', emissive: '#D7FF3A', emissiveIntensity: 0.6, roughness: 0.3, transparent: true}),
      metal: phys({color: '#dfe6f0', metalness: 1, roughness: 0.12, clearcoat: 1}),
      ceramic: glass('#ffffff', 0.05),
      glass: glass('#d8f0ff', 0.02),
      plant: glass('#b9f06a', 0.2, {attenuationColor: '#7fd23a', attenuationDistance: 0.6}),
      screen: phys({color: '#0a1022', metalness: 0.6, roughness: 0.08, clearcoat: 1}),
      lamp: std({color: '#fff6e0', emissive: '#ffd89a', emissiveIntensity: 0, transparent: true}),
    }),
  },
  fosco: {
    name: 'fosco',
    label: 'VIDRO FOSCO',
    accent: '#D7FF3A',
    bg: NAVY,
    grid: '#ffffff',
    gridOpacity: 0.1,
    edges: 0.55,
    shadows: true,
    wall: () => glass('#f4f8ff', 0.42, {thickness: 0.6}),
    cap: () => basic({color: '#D7FF3A', toneMapped: false, transparent: true}),
    floor: () => std({map: floorLines('#14254a', 'rgba(255,255,255,.12)'), roughness: 0.4, metalness: 0.3}),
    mats: () => ({
      white: glass('#f6f9ff', 0.5, {thickness: 0.8}),
      graphite: glass('#5e6f92', 0.45, {thickness: 0.8}),
      wood: glass('#e9d2b6', 0.5, {thickness: 0.8, attenuationColor: '#e2b98a', attenuationDistance: 1}),
      woodDark: glass('#9b8066', 0.5, {thickness: 0.8, attenuationColor: '#a07850', attenuationDistance: 1}),
      fabric: glass('#eef2fb', 0.6, {thickness: 1}),
      fabricDark: glass('#5a6a8c', 0.6, {thickness: 1}),
      lime: glass('#D7FF3A', 0.35, {attenuationColor: '#c6ff1a', attenuationDistance: 0.5, emissive: '#D7FF3A', emissiveIntensity: 0.25}),
      metal: phys({color: '#d7dde6', metalness: 1, roughness: 0.25}),
      ceramic: glass('#ffffff', 0.3),
      glass: glass('#d8f0ff', 0.1),
      plant: glass('#a6e05a', 0.4, {attenuationColor: '#6fbf2a', attenuationDistance: 0.6}),
      screen: phys({color: '#0a1022', metalness: 0.6, roughness: 0.1, clearcoat: 1}),
      lamp: std({color: '#fff6e0', emissive: '#ffd89a', emissiveIntensity: 0, transparent: true}),
    }),
  },
  cromado: {
    name: 'cromado',
    label: 'CROMADO',
    accent: '#D7FF3A',
    bg: NAVY,
    grid: '#ffffff',
    gridOpacity: 0.1,
    edges: 0,
    shadows: true,
    wall: () => phys({color: '#c9d1dc', metalness: 1, roughness: 0.22, clearcoat: 0.6}),
    cap: () => basic({color: '#D7FF3A', toneMapped: false, transparent: true}),
    floor: () => std({map: floorLines('#0f1626', 'rgba(255,255,255,.1)'), roughness: 0.12, metalness: 0.8}),
    mats: () => ({
      white: phys({color: '#e6ebf2', metalness: 1, roughness: 0.18}),
      graphite: phys({color: '#3a4250', metalness: 1, roughness: 0.3}),
      wood: phys({color: '#c9a27a', metalness: 1, roughness: 0.28}),
      woodDark: phys({color: '#6e5440', metalness: 1, roughness: 0.3}),
      fabric: phys({color: '#b8c0cc', metalness: 0.9, roughness: 0.45}),
      fabricDark: phys({color: '#2c3340', metalness: 0.9, roughness: 0.45}),
      lime: phys({color: '#D7FF3A', metalness: 0.9, roughness: 0.2, emissive: '#D7FF3A', emissiveIntensity: 0.2}),
      metal: phys({color: '#f0f3f7', metalness: 1, roughness: 0.06}),
      ceramic: phys({color: '#ffffff', metalness: 0.2, roughness: 0.08, clearcoat: 1}),
      glass: glass('#d8f0ff', 0.02),
      plant: phys({color: '#9cd34a', metalness: 0.8, roughness: 0.3}),
      screen: phys({color: '#05070c', metalness: 0.8, roughness: 0.05, clearcoat: 1}),
      lamp: std({color: '#fff6e0', emissive: '#ffd89a', emissiveIntensity: 0, transparent: true}),
    }),
  },
  holograma: {
    name: 'holograma',
    label: 'HOLOGRAMA',
    accent: '#7fe3ff',
    bg: ['#0f2348', '#040915'],
    grid: '#ffffff',
    gridOpacity: 0.12,
    edges: 1,
    shadows: false,
    wall: () => basic({color: '#7fe3ff', transparent: true, opacity: 0.12, depthWrite: false, side: THREE.DoubleSide}),
    cap: () => basic({color: '#cff4ff', toneMapped: false}),
    floor: () => basic({map: floorLines('#0b1d3d', 'rgba(127,227,255,.22)'), transparent: true, opacity: 0.9}),
    mats: () => {
      const h = (o: number) => basic({color: '#7fe3ff', transparent: true, opacity: o, depthWrite: false, side: THREE.DoubleSide});
      return {
        white: h(0.1),
        graphite: h(0.16),
        wood: h(0.12),
        woodDark: h(0.16),
        fabric: h(0.1),
        fabricDark: h(0.16),
        lime: basic({color: '#D7FF3A', transparent: true, opacity: 0.55, toneMapped: false}),
        metal: h(0.3),
        ceramic: h(0.14),
        glass: h(0.08),
        plant: basic({color: '#b6ff6a', transparent: true, opacity: 0.25, depthWrite: false}),
        screen: h(0.3),
        lamp: std({color: '#fff6e0', emissive: '#ffd89a', emissiveIntensity: 0, transparent: true}),
      };
    },
  },
};

// fundo como textura de cena (o vidro precisa enxergar algo atrás para refratar)
export const bgTexture = ([inner, outer]: [string, string]) => {
  const cv = document.createElement('canvas');
  cv.width = 540;
  cv.height = 960;
  const c = cv.getContext('2d')!;
  const g = c.createRadialGradient(270, 400, 40, 270, 480, 700);
  g.addColorStop(0, inner);
  g.addColorStop(1, outer);
  c.fillStyle = g;
  c.fillRect(0, 0, 540, 960);
  const t = new THREE.CanvasTexture(cv);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
};
