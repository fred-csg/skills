import * as THREE from 'three';

const canvasTex = (w: number, h: number, draw: (c: CanvasRenderingContext2D) => void, repeat?: [number, number]) => {
  const cv = document.createElement('canvas');
  cv.width = w;
  cv.height = h;
  draw(cv.getContext('2d')!);
  const tex = new THREE.CanvasTexture(cv);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  if (repeat) {
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(...repeat);
  }
  return tex;
};

// RNG semeado: textura idêntica em todo frame/processo de render
const rng = (seed: number) => () => {
  seed = (seed * 16807) % 2147483647;
  return (seed - 1) / 2147483646;
};

export const woodTexture = () =>
  canvasTex(
    512,
    512,
    (c) => {
      const r = rng(7);
      const plankH = 512 / 8;
      for (let i = 0; i < 8; i++) {
        const l = 34 + r() * 10;
        c.fillStyle = `hsl(28, 38%, ${l}%)`;
        c.fillRect(0, i * plankH, 512, plankH);
        // veios
        for (let k = 0; k < 14; k++) {
          c.strokeStyle = `rgba(40,22,10,${0.06 + r() * 0.08})`;
          c.lineWidth = 1 + r() * 2;
          const y = i * plankH + r() * plankH;
          c.beginPath();
          c.moveTo(0, y);
          c.bezierCurveTo(170, y + r() * 6 - 3, 340, y + r() * 6 - 3, 512, y);
          c.stroke();
        }
        // juntas
        c.fillStyle = 'rgba(20,12,6,.55)';
        c.fillRect(0, i * plankH, 512, 2);
        const cut = 80 + r() * 350;
        c.fillRect(cut, i * plankH, 2, plankH);
      }
    },
    [1, 1],
  );

export const tileTexture = (base: string, grout: string, n = 4) =>
  canvasTex(
    512,
    512,
    (c) => {
      const r = rng(3);
      c.fillStyle = grout;
      c.fillRect(0, 0, 512, 512);
      const s = 512 / n;
      for (let i = 0; i < n; i++)
        for (let j = 0; j < n; j++) {
          c.fillStyle = base;
          c.globalAlpha = 0.92 + r() * 0.08;
          c.fillRect(i * s + 2, j * s + 2, s - 4, s - 4);
        }
      c.globalAlpha = 1;
    },
    [1, 1],
  );

// Texto em canvas para colar no chão da planta (vira objeto 3D, gira junto com a cena)
export const labelTexture = (title: string, sub: string, color = '#D7FF3A') =>
  canvasTex(1024, 300, (c) => {
    c.textAlign = 'center';
    c.textBaseline = 'middle';
    c.fillStyle = '#F2F4EE';
    c.font = '800 120px Poppins';
    c.fillText(title, 512, 115);
    c.fillStyle = color;
    c.font = '600 72px Poppins';
    c.fillText(sub, 512, 230);
  });

export const cotaTexture = (txt: string, color = '#D7FF3A') =>
  canvasTex(512, 128, (c) => {
    c.textAlign = 'center';
    c.textBaseline = 'middle';
    c.fillStyle = color;
    c.font = '700 84px Poppins';
    c.fillText(txt, 256, 66);
  });
