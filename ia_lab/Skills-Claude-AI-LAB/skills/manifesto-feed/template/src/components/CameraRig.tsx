import React from 'react';
import {AbsoluteFill} from 'remotion';

export type Cam = {
	x?: number;
	y?: number;
	z?: number; // positivo = câmera avança (objetos crescem)
	rx?: number;
	ry?: number;
	rz?: number;
	zoom?: number; // dolly 2D (escala)
	perspective?: number;
};

/**
 * Câmera 2.5D: o mundo tem origem no centro da tela. Os filhos usam <L3> com
 * coordenadas de mundo. A câmera aplica a inversa da sua pose ao mundo.
 */
export const CameraRig: React.FC<{cam: Cam; children: React.ReactNode; style?: React.CSSProperties}> = ({
	cam,
	children,
	style,
}) => {
	const {x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0, zoom = 1, perspective = 1800} = cam;
	return (
		<AbsoluteFill style={{perspective, perspectiveOrigin: '50% 50%', overflow: 'hidden', ...style}}>
			<div
				style={{
					position: 'absolute',
					left: '50%',
					top: '50%',
					width: 0,
					height: 0,
					transformStyle: 'preserve-3d',
					transform: `scale(${zoom}) translateZ(${z}px) rotateX(${rx}deg) rotateY(${ry}deg) rotateZ(${rz}deg) translate3d(${-x}px, ${-y}px, 0px)`,
				}}
			>
				{children}
			</div>
		</AbsoluteFill>
	);
};

/** Camada posicionada no mundo 3D, centrada em (x, y, z). */
export const L3: React.FC<{
	x?: number;
	y?: number;
	z?: number;
	rx?: number;
	ry?: number;
	rz?: number;
	s?: number;
	w?: number;
	h?: number;
	opacity?: number;
	style?: React.CSSProperties;
	children?: React.ReactNode;
}> = ({x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0, s = 1, w = 0, h = 0, opacity = 1, style, children}) => (
	<div
		style={{
			position: 'absolute',
			left: -w / 2,
			top: -h / 2,
			width: w || undefined,
			height: h || undefined,
			transformStyle: 'preserve-3d',
			transform: `translate3d(${x}px, ${y}px, ${z}px) rotateX(${rx}deg) rotateY(${ry}deg) rotateZ(${rz}deg) scale(${s})`,
			opacity,
			...style,
		}}
	>
		{children}
	</div>
);
