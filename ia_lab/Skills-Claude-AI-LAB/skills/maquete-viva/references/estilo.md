# Estilo visual — Maquete Viva

## PADRÃO ATUAL: modo premium (out/2026)
Referência visual: "architectural microcosm" (prédio da Nike aberto, cidade isométrica em miniatura).
- **Render**: Cycles GPU, 32 amostras + denoiser OptiX, AgX "Punchy". Sem saturação extra no pós.
- **Luz**: HDRI de céu (Poly Haven CC0, força 0,45) + sol quente `#FFE9CF` energia 4,6, ângulo 2,5° (sombra firme). Luzes de área quentes dentro de cada andar aberto.
- **Material**: um só, guiado por `obj.color`, com bevel shader (raio 0,025 → quinas arredondadas em tudo) + grão de ruído leve no relevo.
- **Desfoque de miniatura**: foco no alvo da câmera, abertura = 4 / distância (mín. 0,05). Em aéreas a cidade fica com topo/pé desfocados; nas placas o foco puxa pra placa.
- **Prédio-herói**: cor da marca do vídeo (ex. roxo `#7B5BD6`), cantos arredondados, lajes salientes com borda arredondada, frente e lateral direita abertas, guarda-corpo cinza claro, letreiro deitado no telhado em branco, ar-condicionado, térreo com vitrine iluminada e toldos.
- **Cidade**: asfalto `#6B6E75`, quarteirões `#D9D3C9` com meio-fio, faixas brancas, zebras; prédios Kenney (altos ao fundo, baixos na frente da câmera), carros andando, pedestres, postes e semáforos.
- **Árvores**: "brócolis" de 11 esferas com material de folha (variação de cor + relevo Voronoi), verdes `#3F9A36 #4FAE3E #2E8A33 #5DBB45`.
- **Placas de capítulo 3D**: placa branca (contorno arredondado extrudado), disco colorido com número branco, "ETAPA N · TEMA" na cor, título preto (Segoe UI Black), descrição cinza escuro. Entra girando 80°→0 com overshoot, sai girando e encolhendo. Presa à câmera a 2,6 m, 86 % da largura.
- **Cores de capítulo**: roxo `#7B5BD6` · vermelho `#E5484D` · azul `#2F7CF6` · laranja `#F08A3C` · verde `#25A55F` · amarelo `#F2B33D` · rosa `#E86A8C` · teal `#3FB8AF`.

---

## (legado) primeira versão — EEVEE, cores lisas

## Clima
Maquete em miniatura, clara, limpa, "brinquedo premium". Luz de dia suave, sombras leves, pouco contraste. A cor saturada aparece só nos elementos-herói e na UI.

## Paleta 3D (hex sRGB)
- Chão: `#EFE6D2` (bege) · calçada/avenida `#E6E3DD` · meio-fio `#D3CFC6` · praça `#ECE7DE` · parque `#DCE6C8`
- Prédios (quase brancos): `#F2F1EE #E9E6E0 #DDE2E6 #ECE5D8 #E4E7E1 #F0EBE3`, topo `#D9D6CF`
- Faixa de janelas (vidro): `#BCCDD9`, lajes `#FAF9F6`
- Árvores: copa icosfera subdiv 1 (facetada) `#6DB35A #78BD62 #62A851`, tronco `#8A6A48`
- Herói (ex.: loja): laranja `#F08A3C`, toldo branco com listras `#E86A2A`, placa `#2B2F36` com texto branco
- Mundo/fundo: `#F6F1E8`, força 0.72 · Sol `#FFF6EA`, energia 3.4, ângulo 14°

## Cores de capítulo (UI e acentos 3D)
laranja `#F07F2E` · vermelho `#E5484D` · roxo `#7B5BD6` · azul `#2F7CF6` · verde `#25A55F` · amarelo `#F2B33D` · escuro `#1E1E22`

## Personagens "bloquinho"
- Pernas: caixa 0.16×0.18×0.82 com pivô no quadril (z=0.82), afastadas ±0.105
- Tronco: caixa 0.46×0.26×0.62 (z 0.80→1.42) · braços: caixa 0.12×0.14×0.58, pivô no ombro (±0.29, z=1.38)
- Cabeça: esfera suave 0.16 (z=1.60) · cabelo: esfera achatada · variações: cartola (época antiga), boné
- Camisas: `#F2B33D #3DAA5A #9AA0A8 #E8E8E8 #3C7DD9 #E5484D #F08A3C #7B5BD6 #5FB7C9 #D9D2C5`
- Calças: `#3B4A63 #4A4F57 #2F3A4F #6B6F78 #8A7A63` · Pele: `#EBC6A3 #D9A57E #B98058 #8D5A3B #F1D2B6`
- Caminhada: perna ±0.5·sin(fase), braço ∓0.38·sin(fase), fase avança por distância (passada 1.15 m)
- Entrar/sumir: escala → 0 em 0.3 s. Aparecer: easeOutBack.

## Câmera
- Lente 30 mm, sensor vertical 36 mm. Keyframes `(t, posição, alvo, lente, up)` interpolados com smootherstep (nunca linear).
- Linguagem: close no herói → sobe pra revelar o contexto → desce no detalhe (ex.: lixeira) → top-down com "up" girado pra virar tela de celular → aérea alta no fechamento.
- Sempre conferir que a câmera não atravessa prédios.

## Movimento (preferência do usuário, meu-estilo.md)
Sempre com ease in/out. Elementos entram crescendo com leve overshoot, saem com fade. Nada linear ou travado.
