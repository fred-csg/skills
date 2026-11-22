# Motor Remotion + 3D (Claude Code local)

Validado em 2026-10-08 com o teste "planta 3D" (o template `assets/remotion-3d-template/`): 15 s, 1080x1920, renderizado em ~28 s numa máquina com 2× RTX 4090.

## Máquina
- Testado em Windows 10, Node 24, Python 3.11, 2× RTX 4090 (24 GB). Funciona com qualquer GPU (com menos VRAM, baixar `--concurrency`); sem GPU dedicada também roda, só mais devagar. Conferir `node -v` (18+). Se o ffmpeg NÃO estiver no PATH: usar `npx remotion ffmpeg` / `npx remotion ffprobe`. Esse ffmpeg vem enxuto (sem `scale`, `hstack` e outros filtros); para filtros pesados, instalar o ffmpeg completo (`winget install Gyan.FFmpeg`).
- Projeto novo SEMPRE numa subpasta de `pasta_projetos` (config.json). Se `pasta_sincronizada` for true e for Dropbox, antes do `npm install` criar `node_modules` e marcar para o Dropbox ignorar:
  `Set-Content -Path node_modules -Stream com.dropbox.ignored -Value 1`
  (OneDrive/Google Drive: preferir `pasta_projetos` fora da pasta sincronizada.)
- Frames, stills e caches temporários ficam fora de pasta sincronizada (em `%TEMP%`).

## Setup do projeto
- Pacotes com a mesma versão exata do Remotion: `remotion`, `@remotion/cli`, `@remotion/three`, `@remotion/google-fonts` (testado 4.0.534, ver `package.json` do template) + `three` 0.186, `@react-three/fiber` 9.x, React 19.
- `remotion.config.ts`: `Config.setChromiumOpenGlRenderer('angle')` (é o que faz usar a GPU no Windows).
- Render: `npx remotion render <Comp> out/x.mp4 --gl=angle --concurrency=8 --crf=16`.
- Still para conferir: `npx remotion still <Comp> out.jpg --frame=N --gl=angle --scale=0.5`.

## Preview na timeline (sem VS Code)
- Subir o Studio em background: `npx remotion studio --port 3123 --no-open` (a porta 3000 costuma estar ocupada).
- Abrir no painel do navegador do Claude (`preview_start` com url `http://localhost:3123`). O usuário vê a timeline, arrasta o playhead e dá play ao lado do chat. Hot reload: salvou o código, o Studio atualiza.
- Também deixar `.claude/launch.json` com a config `remotion-studio`.

## Regras de cena 3D (three.js dentro do Remotion)
- Tudo deriva de `useCurrentFrame()`: nada de `useFrame`/relógio, nada de `Math.random` sem semente (RNG semeado nas texturas).
- Easing em tudo (`prog(f, a, b, ease)` com inOut cubic / out back / bounce). Nunca linear (estilo-visual.md).
- Câmera: rig em coordenadas esféricas (phi = inclinação, theta = giro, r = distância). Para vista de cima pura usar `phi ≈ 0.002` (não 0, senão o lookAt quebra).
- Somar curvas que se sobrepõem (órbita principal + deriva lenta começando antes de a primeira acabar) para a câmera nunca parar seca.
- Deslocar o enquadramento em eixos de TELA, não do mundo (a câmera gira): `tx = sx·cosθ + sy·sinθ`, `tz = −sx·sinθ + sy·cosθ`. O `sy` positivo sobe a cena no quadro.
- Vertical 9:16 com câmera 3/4: a cena precisa de bem mais distância que a vista de topo (a diagonal ocupa a largura). Conferir com stills no início, no meio e no fim antes de renderizar.
- Tone mapping `NeutralToneMapping` (o ACES lava o limão) + `RoomEnvironment` com PMREM em intensidade 0.5 + key light com sombra (mapSize 2048) + rim light limão.
- Contorno limão emissivo (`toneMapped:false`) no topo das paredes: assinatura visual e dá leitura da forma.
- Vista "casa de boneca": as paredes do fundo sobem inteiras; as do lado da câmera e as internas ficam em corte (~1.05 m). Assim aparecem "as duas paredes" e o interior.
- Texto preso na cena 3D (rótulos, cotas): `CanvasTexture` num plano deitado no chão; gira junto com a cena. Esperar a fonte (`loadFont().waitUntilDone()` + `delayRender`) antes de desenhar no canvas.
- HUD/UI 2D por cima do `ThreeCanvas` como HTML normal (`AbsoluteFill`): marca, etapa, bússola girando com o theta da câmera, card glass final com count-up.

## Regras de marca e visual (feedback aprovado, 2026-10-08)
- NUNCA escrever o nome do usuário (nem o nome da skill/autor) no HUD/vídeo. O topo leva só a etapa (01 · PLANTA BAIXA...).
- Paredes/objetos em branco chapado = reprovado ("branco surgindo do nada"). Preferir vidro transparente com borda iluminada, vidro fosco ou metal (looks em `looks.ts`).
- Fundo preferido para 3D: azul-escuro (gradiente #13284f → #050b1a, como `scene.background`) com grid branco fino (opacidade ~0.1). Preto puro também é aceito.
- Câmera do teste da planta APROVADA (topo → gira → deita → órbita lenta).

## Looks de material (`src/scene/looks.ts` no projeto da planta)
- **vidro**: `MeshPhysicalMaterial` com transmission 1, thickness .35, ior 1.45, roughness baixa, clearcoat + arestas claras (`EdgesGeometry`) em cor gelo #bfeaff. Sem sombras.
- **fosco**: o mesmo vidro com roughness .4–.6 e thickness maior (vidro leitoso) + borda limão.
- **cromado**: metalness 1, roughness .06–.3, environment mais forte (1.1).
- **holograma**: `MeshBasicMaterial` ciano transparente (opacidade .1–.3, depthWrite false) + arestas fortes.
- Pegadinha da transmissão: tudo que é opaco entra no passe de refração e aparece BORRADO dentro do vidro (contorno limão, abajures). Marcar esses materiais como `transparent: true` tira eles do passe.
- A transmissão precisa de `scene.background` (textura de gradiente); com canvas transparente o vidro refrata preto.
- Geometria unitária + `scale` (e `EdgesGeometry` dela compartilhada) para paredes que crescem; não recriar geometria por frame.
- Cada look vira uma `<Composition>` dentro de `<Folder name="Looks">`: o usuário compara no Studio trocando na barra lateral.

## Receita "planta → 3D" (aprovada como teste)
1. 0–2.5 s: vista de topo, grid limão fraco, paredes desenhadas como linha limão (scale.x 0→1 com stagger), cotas "8,00 m / 10,00 m", rótulos dos cômodos e pegadas dos móveis em contorno.
2. 2.5–6 s: câmera gira e deita de topo para 3/4 (inOut cubic); cotas somem.
3. 4.6–7.5 s: paredes sobem com out back (stagger de 6 frames); o pisos trocam de blueprint para material (madeira, porcelanato com texturas procedurais).
4. 7–11 s: móveis montam em sequência (`rise` = scale.y com out back; `drop` = cai de 2.6 m com bounce); a pegada pisca quando o móvel chega e some.
5. 11.5–15 s: órbita lenta, abajures acendem (emissive + pointLight quente), card "ÁREA TOTAL 80 m²" com chips.
- Dados (paredes, cômodos, móveis) ficam num `data.ts` separado: trocar a planta = trocar os dados.

## Armadilhas resolvidas (projeto jarvis-oceano, 2026-10-09)
- **1º frame diferente dos outros** = estado aplicado em `useEffect` (environment PMREM, setSize do composer). No render cada aba faz 1 advance por frame: o 1º frame sai sem o efeito e o still não bate com o vídeo. Aplicar no corpo do render / `useMemo`. Conferir sempre com um trecho sequencial (`--frames=300-316 --concurrency=1`), não só com still.
- **Bloom**: o `<EffectComposer>` do @react-three/postprocessing sai PRETO no render (o Remotion congela o setSize do r3f). Usar o `postprocessing` direto: composer em `useMemo` com `setSize(width, height)` explícito e `useFrame(() => composer.render(), 1)` (ver PostFX.tsx do projeto). @react-three/fiber >= 9.7.
- **Cards de UI sem `transmission`**: vários vidros refrativos sobrepostos estouram para branco. Vidro de UI = MeshPhysical escuro translúcido (metalness .65, envMapIntensity baixo) + anel fino gelo + reflexo diagonal. `transmission` só em 1 objeto herói (água-viva).
- `TTFLoader` do three importa o opentype de uma CDN e quebra o bundle: converter a fonte com o pacote npm `opentype.js` (ttf.ts do projeto). Poppins 3D via `@fontsource/poppins` (.woff).
- Texto 3D numa órbita de câmera: virar para a câmera (billboard por yaw) senão aparece de perfil.
- Glifos fora do subset latin (ex.: →) viram "?": usar só texto.
- Feedback do usuário (v1 reprovada): fonte grotesca pesada, botões limão sólidos, cores sem padrão e chão de textura pixelada = "horrível, sem match". Sempre: Poppins, um componente de card só, acento gelo, chão com reflexo + grid por shader, bloom.
- **Vidro sobre fundo escuro fica apagado** (refrata o azul-escuro e vira um bloco marrom/preto): subir envMapIntensity (~2.2), somar uma aresta fresnel aditiva (mesh irmão com a mesma geometria) e um emissivo baixo. Mascote/objeto colorido: transmission ~0.45 + emissivo da própria cor.
- **Desfoque de fundo (DOF)** no fecho: `DepthOfFieldEffect` do `postprocessing` num EffectPass separado antes do bloom, com `bokehScale` animado por frame e `focusDistance` em metros (distância câmera → texto). Dá ênfase no nome e no personagem.
- **Nunca passar um objeto colorido por trás/através de um lettering na revelação** (o usuário leu o mascote laranja atravessando "JARVIS" como um "blend mode vermelho"). Personagem entra pela lateral antes do texto.
- Tipografia aprovada na v3: Poppins ExtraBold (palavra de impacto), Bold (títulos), SemiBold e Regular (falas leves); nada de Thin/Light e nada de caixa alta forçada.
- Render direto para dentro de pasta do Dropbox pode falhar no rename final (arquivo travado pela sincronização): renderizar em %TEMP% e copiar.
- **Desfoque só no fundo (texto e personagem 100% nítidos)**: o CoC do DepthOfFieldEffect cresce a partir do foco (nítido só NA distância de foco). Colocar lettering e personagem na MESMA profundidade, foco nela e `focusRange` grande (~8 m); objetos translúcidos com `depthWrite:false` herdam a profundidade do fundo e desfocam junto: ligar `depthWrite` neles (pill "Em breve").
- **Pontinhos pretos/vermelhos** em brilhos especulares com bloom/DOF: inserir um pass de "sanitize" logo depois do RenderPass (troca NaN/Inf e limita o HDR a ~4). Também evitar polo de LatheGeometry com raio ~0 (normal nula).
- **Estúdio infinito** (chão emendando na parede): background em gradiente vertical cuja metade de baixo = cor da névoa (Fog 7–19 m) + DOF leve no fundo. Sem linha de horizonte.
- Mascote: o usuário preferiu fosco macio (sem vidro/gloss). Palavra-chave inicial dentro de balão de vidro (o mesmo balão vira o próximo elemento), sem glow estourado (bloom threshold ~0.78).

## Próximos testes sugeridos
- Pós-processamento (bloom no limão, DOF) com `@react-three/postprocessing`.
- Modelos GLB reais (móveis/objetos) no lugar de caixas.
- 2.5D com vídeo falado: mapa de profundidade (Depth Anything na GPU) + máscara da pessoa → parallax e elementos 3D atrás da pessoa.
