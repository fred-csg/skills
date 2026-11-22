# Motion do zero (100% motion, sem gravar nada)

Para quem não quer gravar vídeo falando: o usuário manda o TEMA e as especificações, a skill escreve o roteiro (se ele não tiver), monta o motion completo, sonoriza e renderiza. Exemplo aprovado: "Character Sheet" (9:16, 56 s, mascote KAI desenhado em código, narração sincronizada).

## 1. Briefing (perguntar o que faltar, em UMA rodada)
Quanto mais informação, mais certeiro o primeiro preview. Checklist:
- **Tema e mensagem central** (a frase que a pessoa tem que lembrar).
- **Objetivo:** educar, vender, gerar comentário, lançamento…
- **Público** e **tom** (didático, zoeiro, premium…).
- **Estilo de motion:** Jarvis padrão (Vidro/Holograma) ou **Cleanstill** (limpo e calmo, `references/cleanstill.md`). Sempre oferecer as duas; para anúncio de produto/ferramenta recomendar Cleanstill.
- **Formato e duração:** 9:16 / 1:1 / 16:9, 15–60 s.
- **Marca:** cores, logo, fonte (padrão Poppins), estilo (padrão Vidro/Holograma ou a paleta da marca).
- **Roteiro/narração:** já tem? Se não, a skill escreve.
- **Voz:** vai ter narração? (gravar, voz de IA, ou só texto na tela + trilha).
- **CTA final** (comenta X, link na bio…).
- **Referências** (vídeos/imagens que gosta) e o que NÃO quer.

## 2. Roteiro → `ROTEIRO.md`
Tabela de beats com tempo, texto na tela e o que a UI/cena faz: HOOK (0–4 s) → PROBLEMA → REVEAL → BUILD (shot herói) → 2–3 VANTAGENS → COMO USAR → CTA/FINAL. Um visual por ideia; texto curto na tela (2–6 palavras por cartela, palavra-chave na cor de destaque). Marcar timestamps-chave (cliques, giros, carimbos) para som e voz.

## 3. Narração → `NARRACAO.md` (se houver voz)
Tabela com início, janela máxima e fala de cada trecho, sincronizada aos eventos do roteiro (ritmo-base ~2,8 palavras/s). O usuário grava ou gera a voz (ex.: voz de IA) seguindo esse arquivo e manda o áudio; a skill transcreve (`assets/legenda-template/scripts/transcrever.py`), ajusta os tempos das cenas à fala real e mixa.

## 4. Motion
- Remotion (preferido, preview na timeline) ou HTML/GSAP com `seek(t)` + render por quadros. Personagens, cards e UI em código; 3D com `assets/remotion-3d-template/`.
- Se o estilo for **Cleanstill**: partir de `assets/cleanstill-template/` e seguir `references/cleanstill.md` (a estrutura de 12 beats do item 7 serve de molde de roteiro).
- Linguagem do exemplo aprovado (estilo Jarvis padrão): fundo quase preto, destaque limão `#D7FF3A` (solução) e vermelho `#FF3B4E` (problema), painéis de vidro arredondados, cursor clicando, toggles, contadores, carimbos, carrossel 3D, câmera atravessando planos. Easing sempre; nada linear.
- Números ilustrativos marcados como "simulação" na tela.

## 5. Som
Sonorização com a biblioteca do usuário (`pasta_sfx`, ver `references/sfx.md`; nunca por código) nos timestamps do roteiro + trilha do usuário + voz com ducking. Entregar mix e stems.

## 6. Entrega
Preview primeiro → aprovação → render final. Entregar MP4, `ROTEIRO.md`, `NARRACAO.md`, sugestão de legenda do post e o SRT da narração.
