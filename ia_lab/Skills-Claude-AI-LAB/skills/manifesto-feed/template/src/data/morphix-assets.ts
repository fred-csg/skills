// Imagens reais nos cards (opcional). Coloque os arquivos em public/morphix/ (Morphix, Higgsfield, fotos — tanto faz).
// Tudo vazio/null = os cards usam as thumbnails procedurais (cinza abstratas), que já funcionam sozinhas.

// Card protagonista (o "refinado" da cena 4 e o card que para na cena 8). Ex.: 'morphix/hero.png'
export const HERO_IMAGE: string | null = null;

// Feed da cena 3 (o 1º também é o card que nasce do tile na cena 2). Ex.: ['f_cidade.jpg', 'f_skate.jpg', ...]
export const FEED_IMAGES: string[] = [];

// Cards do corredor infinito da cena 6. Ex.: ['c_astronauta.jpg', 'c_carro.jpg', ...]
export const CORRIDOR_IMAGES: string[] = [];

// fração dos cards do corredor que recebem um asset real (0..1)
export const CORRIDOR_SHARE = 0.75;
