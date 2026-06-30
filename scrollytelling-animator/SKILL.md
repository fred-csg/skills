---
name: scrollytelling-animator
description: Cria componentes ou landing pages para animação frame-a-frame vinculadas ao scroll (Scrollytelling). Acione esta skill SEMPRE que o usuário pedir por animações controladas por scroll, sequência de imagens, "controlar um vídeo com scroll" (pois a abordagem recomendada é usar frames via canvas) ou experiências de scrollytelling. A skill obriga o uso de HTML5 Canvas e Vanilla JavaScript focado em alta performance.
---

# Scrollytelling Animator

Esta skill fornece uma arquitetura limpa, hiper-otimizada e sem dependências para reproduzir sequências de imagens conforme a barra de rolagem (scroll) desce ou sobe na tela. Esta abordagem é imensamente superior ao uso de `<video>` tag sincronizado com scroll, evitando gargalos de I/O e garantindo 60 FPS consistentes.

Sua tarefa principal ao utilizar esta skill é traduzir as intenções criativas do usuário em um sistema performático utilizando o boilerplate abaixo.

## 1. Diretrizes Fundamentais

- **Sem Bibliotecas:** Utilize exclusivamente Vanilla HTML, CSS e JavaScript. Não importe Framer Motion, GSAP, Tailwind ou React, a menos que o usuário insista explicitamente.
- **Canvas over Image:** A renderização MUST ser feita no `<canvas>` usando o contexto `2d` com `drawImage`.
- **Preload Total:** Nenhum scroll listener deve ser ativado antes de 100% dos frames estarem em memória (via `new Image()`).
- **Scroll Ticking:** Sempre atrele a leitura de scroll e o `render()` ao `window.requestAnimationFrame` usando uma flag booleana de controle (ticking) para evitar enfileiramento de chamadas.
- **Device Pixel Ratio:** O canvas deve tratar nativamente o `window.devicePixelRatio` multiplicando seu `width` e `height` e rodando `ctx.scale()` para que não fique embaçado em monitores Retina/4K.

## 2. Padrão de Boilerplate

Sempre que gerar a solução, baseie-se nesta estrutura (que deve ficar em um `index.html` ou em arquivos separados se solicitado):

### CSS Essencial
O contêiner deve forçar o *sticky* do wrapper, de forma que o conteúdo da tela fique travado enquanto o usuário atravessa um espaço vazio enorme (o scroll-container) que determinará o tempo da animação.

```css
body, html { margin: 0; padding: 0; background-color: #E6E6E6; }
.scroll-container { height: 400vh; position: relative; } /* Controla a duração do scroll */
.sticky-wrapper { position: sticky; top: 0; height: 100vh; width: 100%; overflow: hidden; }
canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; }
```

### Lógica de Preload e Renderização

```javascript
const FRAME_COUNT = 120; // Substituir pela quantidade de frames requisitada pelo usuário
const images = [];
let loadedCount = 0;
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const scrollContainer = document.getElementById('scroll-container');

// 1. Preload Manager
for (let i = 0; i <= FRAME_COUNT; i++) { // Adapte o i se o usuário disser que começa no 1
    const img = new Image();
    const paddedIndex = String(i).padStart(5, '0'); // Adapte conforme o padrão fornecido
    img.src = `path/to/frames_${paddedIndex}.jpg`;
    img.onload = () => {
        loadedCount++;
        // TODO: Atualizar um percentual de loading na tela
        if (loadedCount === FRAME_COUNT + 1) init();
    };
    images.push(img);
}

// 2. Inicialização
let ticking = false;
function init() {
    // TODO: Esconder tela de loading
    resizeCanvas();
    window.addEventListener('resize', () => { resizeCanvas(); requestAnimationFrame(render); });
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => { render(); ticking = false; });
            ticking = true;
        }
    });
    render();
}

function resizeCanvas() {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = window.innerWidth * dpr;
    canvas.height = window.innerHeight * dpr;
    ctx.scale(dpr, dpr);
}

// 3. Render Loop Central
function render() {
    const scrollHeight = scrollContainer.offsetHeight - window.innerHeight;
    let progress = window.scrollY / scrollHeight;
    progress = Math.max(0, Math.min(1, progress));

    const frameIndex = Math.min(images.length - 1, Math.floor(progress * images.length));
    const img = images[frameIndex];
    
    if (img) {
        const displayWidth = window.innerWidth;
        const displayHeight = window.innerHeight;
        
        ctx.clearRect(0, 0, displayWidth, displayHeight);

        // Lógica de Fit/Cover/Contain
        const hRatio = displayWidth / img.width;
        const vRatio = displayHeight / img.height;
        
        // Exemplo: não expandir acima do tamanho original, usar Math.min(hRatio, vRatio, 1);
        const ratio = Math.min(hRatio, vRatio, 1);
        
        // Posicionamento (Adapte a gosto do usuário: centro, direita, etc)
        const shift_x = (displayWidth - img.width * ratio) / 2; // Centralizado X
        const shift_y = (displayHeight - img.height * ratio) / 2; // Centralizado Y

        ctx.drawImage(img, 0, 0, img.width, img.height, shift_x, shift_y, img.width * ratio, img.height * ratio);
    }
}
```

## 3. Instruções Finais de Engajamento

1. Antes de codificar, pergunte ativamente ao usuário:
   - Quantas imagens formam a sequência?
   - Qual a nomenclatura e extensão (ex: 00000.jpg, 0001.png)?
   - Como ele prefere o alinhamento da imagem? (Centro, Direita, não estourar resolução?)
   - Há textos/títulos que devem aparecer e desaparecer em certos pontos do scroll?
2. Caso hajam textos vinculados ao scroll, escreva uma função genérica de `useTransform(value, input[], output[])` para interpolar as opacidades e transformar elementos do DOM durante o `render()`.
3. Siga exatamente o padrão boilerplate para garantir 60 FPS, ele é uma arquitetura de referência robusta.
