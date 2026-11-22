import {useThree} from '@react-three/fiber';
import {useLayoutEffect, useMemo} from 'react';
import {Easing, useCurrentFrame} from 'remotion';
import * as THREE from 'three';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
import {inOut, inOutSine, lerp, outBack, outCubic, prog} from '../anim';
import {GLASS, ITEMS, Item, MatKey, Part, ROOMS, Room, Seg, WALLS, WALL_H, WALL_T} from './data';
import {Look, bgTexture} from './looks';
import {cotaTexture, labelTexture} from './textures';

// ─── Linha do tempo (frames @30fps) ───────────────────────────────────────
export const T = {
  draw: [8, 70] as const, // paredes desenhadas em linha
  cotas: [40, 75, 118, 145] as const, // entra, sai
  labels: [52, 86, 188, 220] as const,
  prints: [60, 96] as const, // pegada dos móveis
  orbit: [84, 182] as const, // planta deita e vira perspectiva
  walls: [138, 6, 30] as const, // início, stagger, duração
  floors: [178, 222] as const,
  furn: [214, 6, 24] as const,
  lights: [345, 385] as const,
};

type Mats = Record<MatKey, THREE.Material>;

// geometrias unitárias compartilhadas (escala no mesh): a aresta não precisa ser recalculada por frame
const UNIT_BOX = new THREE.BoxGeometry(1, 1, 1);
const UNIT_EDGES = new THREE.EdgesGeometry(UNIT_BOX);

// ─── Ambiente / luz ──────────────────────────────────────────────────────
const Env = ({look}: {look: Look}) => {
  const {gl, scene} = useThree();
  useLayoutEffect(() => {
    gl.toneMapping = THREE.NeutralToneMapping; // ACES lava o limão
    gl.toneMappingExposure = 1.0;
    const pm = new THREE.PMREMGenerator(gl);
    scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = look.name === 'cromado' ? 1.1 : 0.7;
    scene.background = bgTexture(look.bg);
    scene.fog = new THREE.Fog(look.bg[1], 28, 60);
  }, [gl, scene, look]);
  return null;
};

const Lights = ({f, look}: {f: number; look: Look}) => {
  const night = prog(f, T.lights[0], T.lights[1]);
  return (
    <>
      <hemisphereLight args={['#dfe8ff', '#0b1630', lerp(0.6, 0.35, night)]} />
      <directionalLight
        position={[7, 14, 9]}
        intensity={lerp(2.2, 1.3, night)}
        castShadow={look.shadows}
        shadow-mapSize={[2048, 2048]}
        shadow-camera-left={-9}
        shadow-camera-right={9}
        shadow-camera-top={9}
        shadow-camera-bottom={-9}
        shadow-bias={-0.0004}
        shadow-normalBias={0.02}
      />
      {/* rim frio por trás: desenha a borda do vidro/metal */}
      <directionalLight position={[-8, 7, -7]} intensity={1.2} color="#9cc8ff" />
      <directionalLight position={[-6, 4, 8]} intensity={0.5} color={look.accent} />
      {[
        [-3.4, 1.0, -4.5],
        [-0.6, 1.0, -4.5],
        [-0.5, 1.7, 4.3],
      ].map((p, i) => (
        <pointLight key={i} position={p as [number, number, number]} color="#ffcf8a" intensity={night * 6} distance={5} decay={2} />
      ))}
    </>
  );
};

// ─── Câmera: topo → gira → deita em perspectiva → órbita lenta ───────────
const CameraRig = ({f}: {f: number}) => {
  const camera = useThree((s) => s.camera) as THREE.PerspectiveCamera;
  const o = prog(f, T.orbit[0], T.orbit[1], inOut);
  const tail = prog(f, 160, 450, inOutSine);
  const theta = 0.8 * prog(f, 74, 182, inOut) + 0.45 * tail;
  const phi = lerp(0.002, 0.98, o) - 0.06 * tail;
  // vertical 9:16: a perspectiva precisa de mais distância que o topo pra caber a planta inteira
  const r = lerp(24, 22.6, prog(f, 0, 90, inOutSine)) + 7.4 * o + 3 * Math.sin(o * Math.PI) - 1.2 * tail;
  const ty = lerp(0, 0.7, o);
  // deslocamento em eixos de TELA (a câmera gira, então x/z do mundo não servem): sx = esquerda, sy = sobe
  const sx = 0.55 * o;
  const sy = 1.6 * o;
  const tx = sx * Math.cos(theta) + sy * Math.sin(theta);
  const tz = -sx * Math.sin(theta) + sy * Math.cos(theta);
  camera.fov = 40;
  camera.position.set(tx + r * Math.sin(phi) * Math.sin(theta), ty + r * Math.cos(phi), tz + r * Math.sin(phi) * Math.cos(theta));
  camera.lookAt(tx, ty, tz);
  camera.updateProjectionMatrix();
  return null;
};

// ─── Peças ───────────────────────────────────────────────────────────────
const segInfo = ([x1, z1, x2, z2]: Seg) => {
  const dx = x2 - x1;
  const dz = z2 - z1;
  return {len: Math.hypot(dx, dz), ang: -Math.atan2(dz, dx)};
};

// Paredes do fundo sobem inteiras; as do lado da câmera ficam em corte (vista "casa de boneca")
const FULL = new Set([0, 1]);
const CUT_H = 1.05;

type WallProps = {seg: Seg; i: number; f: number; wallMat: THREE.Material; capMat: THREE.Material; edgeMat: THREE.LineBasicMaterial | null; glass?: THREE.Material; shadows: boolean};

const Wall = ({seg, i, f, wallMat, capMat, edgeMat, glass, shadows}: WallProps) => {
  const {len, ang} = segInfo(seg);
  const order = glass ? 4 : i;
  const draw = prog(f, T.draw[0] + order * 4, T.draw[0] + order * 4 + 34, outCubic);
  const h = glass ? CUT_H : FULL.has(i) ? WALL_H : CUT_H;
  const rs = T.walls[0] + order * T.walls[1];
  const rise = prog(f, rs, rs + T.walls[2], outBack);
  const y = Math.max(rise, 0.0001) * h;
  const L = len + WALL_T;
  const th = glass ? 0.05 : WALL_T;
  if (draw <= 0) return null;
  return (
    <group position={[seg[0], 0, seg[1]]} rotation={[0, ang, 0]}>
      <group scale={[draw, 1, 1]}>
        {rise > 0 && (
          <>
            <mesh geometry={UNIT_BOX} position={[len / 2, y / 2, 0]} scale={[L, y, th]} castShadow={shadows && !glass} receiveShadow material={glass ?? wallMat} />
            {edgeMat && <lineSegments geometry={UNIT_EDGES} position={[len / 2, y / 2, 0]} scale={[L, y, th]} material={edgeMat} />}
          </>
        )}
        <mesh geometry={UNIT_BOX} position={[len / 2, y + 0.012, 0]} scale={[L, 0.024, th + 0.012]} material={capMat} />
      </group>
    </group>
  );
};

// piso: blueprint por cômodo, depois um piso único com linhas a cada 0.5 m
const Floors = ({f, floorMat, accent}: {f: number; floorMat: THREE.Material; accent: string}) => {
  const p = prog(f, T.floors[0], T.floors[1], inOut);
  floorMat.transparent = true;
  floorMat.opacity = p * (floorMat.userData.baseOpacity ?? (floorMat.userData.baseOpacity = 1));
  return (
    <group>
      {ROOMS.map((room) => {
        const w = room.x[1] - room.x[0];
        const d = room.z[1] - room.z[0];
        return (
          <mesh key={room.name} position={[(room.x[0] + room.x[1]) / 2, 0.004, (room.z[0] + room.z[1]) / 2]} rotation={[-Math.PI / 2, 0, 0]}>
            <planeGeometry args={[w - 0.04, d - 0.04]} />
            <meshBasicMaterial color={accent} transparent opacity={0.06 * prog(f, 20, 60) * (1 - p)} depthWrite={false} />
          </mesh>
        );
      })}
      {p > 0 && (
        <mesh position={[0, 0.006, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow material={floorMat}>
          <planeGeometry args={[8, 10]} />
        </mesh>
      )}
    </group>
  );
};

const Label = ({room, f, i, accent}: {room: Room; f: number; i: number; accent: string}) => {
  const tex = useMemo(() => labelTexture(room.name, room.area, accent), [room, accent]);
  const a = prog(f, T.labels[0] + i * 4, T.labels[1] + i * 4, outCubic) * (1 - prog(f, T.labels[2], T.labels[3]));
  if (a <= 0) return null;
  const s = lerp(0.85, 1, a);
  return (
    <mesh position={[room.label[0], 0.03, room.label[1]]} rotation={[-Math.PI / 2, 0, 0]} scale={[s, s, s]}>
      <planeGeometry args={[1.9, 1.9 * (300 / 1024)]} />
      <meshBasicMaterial map={tex} transparent opacity={a} depthWrite={false} toneMapped={false} />
    </mesh>
  );
};

const Line = ({x, z, w, d, op, color}: {x: number; z: number; w: number; d: number; op: number; color: string}) => (
  <mesh position={[x, 0.02, z]} rotation={[-Math.PI / 2, 0, 0]}>
    <planeGeometry args={[w, d]} />
    <meshBasicMaterial color={color} transparent opacity={op} depthWrite={false} toneMapped={false} />
  </mesh>
);

const Cotas = ({f, accent}: {f: number; accent: string}) => {
  const a = prog(f, T.cotas[0], T.cotas[1], outCubic) * (1 - prog(f, T.cotas[2], T.cotas[3]));
  const t8 = useMemo(() => cotaTexture('8,00 m', accent), [accent]);
  const t10 = useMemo(() => cotaTexture('10,00 m', accent), [accent]);
  if (a <= 0) return null;
  const k = 0.9 * a;
  const c = accent;
  return (
    <group>
      <Line x={0} z={-5.75} w={8 * a} d={0.025} op={k} color={c} />
      <Line x={-4} z={-5.75} w={0.025} d={0.3} op={k} color={c} />
      <Line x={4} z={-5.75} w={0.025} d={0.3} op={k} color={c} />
      <mesh position={[0, 0.02, -6.15]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[1.6, 0.4]} />
        <meshBasicMaterial map={t8} transparent opacity={a} depthWrite={false} toneMapped={false} />
      </mesh>
      <Line x={-4.75} z={0} w={0.025} d={10 * a} op={k} color={c} />
      <Line x={-4.75} z={-5} w={0.3} d={0.025} op={k} color={c} />
      <Line x={-4.75} z={5} w={0.3} d={0.025} op={k} color={c} />
      <mesh position={[-5.15, 0.02, 0]} rotation={[-Math.PI / 2, 0, Math.PI / 2]}>
        <planeGeometry args={[1.6, 0.4]} />
        <meshBasicMaterial map={t10} transparent opacity={a} depthWrite={false} toneMapped={false} />
      </mesh>
    </group>
  );
};

// pegada do móvel na planta: aparece no blueprint, pisca quando o móvel chega e some
const Footprint = ({it, f, start, accent}: {it: Item; f: number; start: number; accent: string}) => {
  const [w, d] = it.fp;
  const show = prog(f, T.prints[0], T.prints[1], outCubic);
  const flash = prog(f, start, start + 8, outCubic);
  const gone = prog(f, start + 10, start + 34, inOut);
  const op = (0.5 * show + 0.5 * flash) * (1 - gone);
  if (op <= 0.001) return null;
  const t = 0.03;
  return (
    <group position={[it.x, 0, it.z]}>
      <Line x={0} z={-d / 2} w={w} d={t} op={op} color={accent} />
      <Line x={0} z={d / 2} w={w} d={t} op={op} color={accent} />
      <Line x={-w / 2} z={0} w={t} d={d} op={op} color={accent} />
      <Line x={w / 2} z={0} w={t} d={d} op={op} color={accent} />
    </group>
  );
};

const PartMesh = ({p, mats, edgeMat, shadows}: {p: Part; mats: Mats; edgeMat: THREE.LineBasicMaterial | null; shadows: boolean}) => {
  const mat = mats[p.m];
  const geo = useMemo(
    () =>
      p.t === 'box'
        ? new THREE.BoxGeometry(...p.s)
        : p.t === 'cyl'
          ? new THREE.CylinderGeometry(p.s[0], p.s[0], p.s[1], 40)
          : new THREE.SphereGeometry(p.s[0], 40, 24),
    [p],
  );
  // arestas só em caixas e cilindros (em esfera vira malha poluída)
  const edges = useMemo(() => (edgeMat && p.t !== 'sph' ? new THREE.EdgesGeometry(geo, 25) : null), [geo, edgeMat, p.t]);
  const pos: [number, number, number] = p.t === 'sph' ? p.p : [p.p[0], p.p[1] + p.s[1] / 2, p.p[2]];
  return (
    <group position={pos}>
      <mesh geometry={geo} castShadow={shadows} receiveShadow={shadows} material={mat} />
      {edges && <lineSegments geometry={edges} material={edgeMat!} />}
    </group>
  );
};

const Furniture = ({it, f, start, mats, edgeMat, shadows}: {it: Item; f: number; start: number; mats: Mats; edgeMat: THREE.LineBasicMaterial | null; shadows: boolean}) => {
  const p = prog(f, start, start + T.furn[2], it.mode === 'rise' ? outBack : Easing.bounce);
  if (p <= 0) return null;
  const sy = it.mode === 'rise' ? Math.max(p, 0.001) : 1;
  const y = it.mode === 'drop' ? (1 - p) * 2.6 : 0;
  return (
    <group position={[it.x, y, it.z]} scale={[1, sy, 1]}>
      {it.parts.map((part, k) => (
        <PartMesh key={k} p={part} mats={mats} edgeMat={edgeMat} shadows={shadows} />
      ))}
    </group>
  );
};

// ─── Cena ────────────────────────────────────────────────────────────────
export const Scene = ({look}: {look: Look}) => {
  const f = useCurrentFrame();
  const mats = useMemo(() => look.mats(), [look]);
  const wallMat = useMemo(() => look.wall(), [look]);
  const capMat = useMemo(() => look.cap(), [look]);
  const floorMat = useMemo(() => look.floor(), [look]);
  const edgeMat = useMemo(
    () => (look.edges > 0 ? new THREE.LineBasicMaterial({color: look.accent, transparent: true, opacity: look.edges, toneMapped: false}) : null),
    [look],
  );
  (mats.lamp as THREE.MeshStandardMaterial).emissiveIntensity = 2.2 * prog(f, T.lights[0], T.lights[1]);
  const gridOp = look.gridOpacity * (prog(f, 0, 24) - 0.4 * prog(f, T.orbit[0], T.orbit[1]));

  return (
    <>
      <Env look={look} />
      <Lights f={f} look={look} />
      <CameraRig f={f} />

      <gridHelper args={[60, 120, look.grid, look.grid]} position={[0, -0.26, 0]}>
        <lineBasicMaterial attach="material" color={look.grid} transparent opacity={gridOp} depthWrite={false} />
      </gridHelper>

      {/* laje */}
      <mesh position={[0, -0.13, 0]} receiveShadow>
        <boxGeometry args={[8.5, 0.25, 10.5]} />
        <meshStandardMaterial color="#0a1328" roughness={0.35} metalness={0.6} />
      </mesh>

      <Floors f={f} floorMat={floorMat} accent={look.accent} />
      {ROOMS.map((r, i) => (
        <Label key={r.name} room={r} f={f} i={i} accent={look.accent} />
      ))}
      <Cotas f={f} accent={look.accent} />

      {WALLS.map((s, i) => (
        <Wall key={i} seg={s} i={i} f={f} wallMat={wallMat} capMat={capMat} edgeMat={edgeMat} shadows={look.shadows} />
      ))}
      {GLASS.map((s, i) => (
        <Wall key={'g' + i} seg={s} i={i} f={f} wallMat={wallMat} capMat={capMat} edgeMat={edgeMat} glass={mats.glass} shadows={look.shadows} />
      ))}

      {ITEMS.map((it, i) => {
        const start = T.furn[0] + i * T.furn[1];
        return (
          <group key={it.name}>
            <Footprint it={it} f={f} start={start} accent={look.accent} />
            <Furniture it={it} f={f} start={start} mats={mats} edgeMat={edgeMat} shadows={look.shadows} />
          </group>
        );
      })}
    </>
  );
};
