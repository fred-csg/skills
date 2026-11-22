# Jarvis — instalação

Skill para Claude Code que edita vídeo com motion graphics (decupagem, corte, punch-ins, glitch, tracking, HUD, UI) e cria animações 3D reais com Remotion + three.js, com preview na timeline do Remotion Studio e render local.

Autor: Lucas Sena.

## Pré-requisitos
- **Claude Code desktop** (app Claude, aba Code) — ou Claude Code no terminal/VS Code.
- **Node.js 18+** (gratuito): se não estiver instalado, o próprio Claude instala no primeiro uso (winget no Windows, Homebrew ou instalador oficial no Mac). Manual: https://nodejs.org
- Só isso. O resto (Remotion, three.js, ffmpeg completo via `ffmpeg-static`, OpenCV via `@techstark/opencv-js`) a própria skill instala com `npm` dentro de cada projeto.
- Recomendado: placa de vídeo dedicada (NVIDIA/AMD). Sem GPU funciona, só renderiza mais devagar.
- Opcional: Python 3.10+ — só para o recorte da pessoa no caminho já validado (elementos atrás da cabeça). Sem Python, a skill tenta a rota em Node ou faz a edição sem esse recurso.

## Instalação
1. Copie a pasta inteira `skill-do-jarvis` para a pasta de skills do Claude Code:
   - Windows: `C:\Users\<seu-usuário>\.claude\skills\skill-do-jarvis`
   - macOS/Linux: `~/.claude/skills/skill-do-jarvis`
2. Confira que dentro dela existe o `SKILL.md` (não deixe uma pasta dentro de outra).
3. Abra uma conversa nova no Claude Code. A skill aparece como `skill-do-jarvis`.

## Primeiro uso
- Peça algo como: *"usa a skill-do-jarvis pra editar este vídeo"* ou *"faz uma planta 3D animada"*.
- Na primeira vez, o Claude pergunta suas pastas (projetos e entregas — o padrão das entregas é a sua Área de Trabalho), a cor de acento, o look padrão (vidro ou holograma) e o idioma, e grava um `config.json` dentro da pasta da skill. Para mudar depois, edite esse arquivo ou peça ao Claude.
- O modelo dos campos está em `config.example.json`.
- Os efeitos sonoros são gerados por código (nada para baixar). Se você tiver sua própria biblioteca de SFX, é só pedir para usar.
- O primeiro projeto roda `npm install` (baixa Remotion, three.js e ffmpeg; alguns minutos). O preview abre no painel do navegador do Claude.

## O que vem na pasta
| Caminho | O quê |
|---|---|
| `SKILL.md` | fluxo principal |
| `references/` | estilo visual, motor Remotion 3D, plano de motion, tracking, recorte, ícones 3D, SFX, master em camadas |
| `assets/sfx-gen/` | gerador de efeitos sonoros por código (Node puro) |
| `assets/remotion-3d-template/` | projeto Remotion pronto (planta 3D com looks vidro, fosco, cromado e holograma) |
| `config.example.json` | modelo de configuração |

## Para quem vai redistribuir
Não inclua o seu `config.json` nem `assets/remotion-3d-template/node_modules` no pacote (o `config.json` tem os seus caminhos pessoais).
