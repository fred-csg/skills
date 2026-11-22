# Interface — Maquete Viva premium (1080×1920)

Motor: `scripts/molde/mvo.py` (PIL desenhado em 2× e reduzido, pipe pro ffmpeg). Cada vídeo tem um `overlay.py` que monta um `Cfg` e chama `mvo.main(C)`.
Fontes (Windows): `segoeuib.ttf` (textos), `seguibl.ttf` (números/títulos), `consolab.ttf` (rótulos mono), `seguisym.ttf` (símbolos ✓ ✕ ♥ ▶ ✂ ◎ ⇕ — `txt()` troca de fonte sozinho).

## Área segura
Conteúdo essencial na safe zone v2 (`safe-zone/SAFE-ZONE.md`): y 240..1500, x 95..985, e x ≤ 870 abaixo de y 800. Legenda karaokê centrada em (495, 1150). Nunca título + legenda + cartão grande disputando a mesma região ao mesmo tempo.

## Elementos (padrão atual)
| Elemento | Onde | Como |
|---|---|---|
| **Barra de etapas** (`chip_style="stepper"`) | x 90..900, y 262..348 + barra de progresso fina embaixo | contêiner branco arredondado com sombra; etapa atual = pílula na cor do capítulo com número em círculo branco + nome; feitas = círculo colorido com ✓; futuras = cinza. A barra de baixo enche até a próxima etapa. Some durante o celular (`steps_hide`). No fim todas ✓ (`chips_all`). |
| **Placas de capítulo** | 3D, na cena (`titulos3d.py`) | ver estilo.md. O overlay não desenha título 2D (`titles=[]`); o título-palavra final ("IA NO BALCÃO") também é placa. |
| Cartão contador | x 90, y 378 (slot 0) / x 356 (slot 1) | branco, borda colorida, número mono 62 px, rótulo 21 px, "bump" ao mudar |
| Tag "ilustrativo" | direita, y 392 | pílula cinza translúcida, sempre que houver números de exemplo |
| Callouts | âncora 3D projetada + offset | pílula com linha-guia que cresce da âncora + bolinha; não repetir o que a placa 3D já diz |
| Checklist | direita, y≈520 | título mono + itens com caixinha que vira ✓ verde |
| Notificação | centro, y≈560–985 | cartão estilo iOS: ícone colorido, app • remetente, "agora", mensagem bold; entra deslizando |
| **Celular de app** (`phone_v2`) | centro, 440×900, y≈690 | aparelho com ilha, status 9:41, cabeçalho com avatar e nome do negócio, cartão de foto (visor com cantoneiras e botão → flash → "✓ foto ok"), linhas de opção com ícone + preço + chave liga/desliga animada, total somando e ficando verde, botão primário que "afunda" no toque, anel de toque do dedo em cada ação. Entra subindo com leve overshoot. |
| Selo REC / play | dentro do celular grande (`phone`) | quando a maquete "vira vídeo" |
| Flash | tela toda | 0,18 s em fotos |
| Vinheta colorida | tela toda | só em momento de "problema/perda" |
| **CTA padrão** | do fim da fala-síntese até o fim | fundo desfocado + véu creme; "Quer aprender a fazer / vídeos assim?" + pílula laranja "automático, usando IA"; pílula escura "me segue nas redes"; cartões com ícone desenhado das redes gravadas em `redes.json` (entram em sequência na palavra "redes") |

Todos os cartões com sombra suave (`shadow=True`).

## Cor
`grade=None` (padrão). Não aplicar saturação/contraste extra — o usuário recusou a versão saturada.

## Regras
- Conferir em miniatura (folha de contato) antes do render final.
- Exportar o master sem guias de QA.
- Mudança só de interface = re-rodar só o overlay.
