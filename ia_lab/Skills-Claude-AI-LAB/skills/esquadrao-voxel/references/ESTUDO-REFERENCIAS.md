# Estudo de referências — 5 Reels de bonequinhos de bloco (30/10/2026)


Os 5 são do mesmo perfil (estilo idêntico ao nosso). Servem pra aprender a TÉCNICA; nada de copiar roteiro, cenário, personagem ou HUD.

| Reel | Duração | Gancho (fala) | Cenário-metáfora | Estrutura |
|---|---|---|---|---|
| Empresa no Claude Code | 60 s | "Eu tenho uma empresa inteira dentro do meu Claude Code." | prédio em corte, câmera sobe andar por andar | 13 agentes por departamento, contador 0/13 |
| Shark Tank | 33 s | "Montei um Shark Tank Brasil com 5 Claudes tubarões…" | estúdio de TV com 5 poltronas | você apresenta → perguntas → ofertas → fechou? |
| 3 skills pra começar | 37 s | "Se eu começasse hoje a usar o Claude Code, instalaria essas 3 skills." | fliperama, máquina de garra pega o boneco | a primeira / a segunda / a terceira, contador de instalações |
| 15 melhores skills | 42 s | "Essas são as 15 melhores skills do Claude Code…" | biblioteca com alas e placar de estrelas | 5 alas × 3 livros, contador de estrelas |
| Instagram Agent | 38 s | "O Claude acabou de matar o Instagram." | agência com uma sala temática por cargo | 13 cargos, "o que mais me impressionou" antes do último |

## O que funciona (e como a gente usa do NOSSO jeito)
1. **Cenário = metáfora do assunto.** Um lugar real que já é uma coleção ou um sistema (prédio, fliperama, biblioteca, estúdio de TV). Nosso: escolher OUTRA metáfora a cada vídeo — cozinha de restaurante (pedidos saindo), estação de trem (agenda), aeroporto (tráfego), oficina (conserto), feira livre (oferta), museu (portfólio), horta (crescimento), corpo de bombeiros (urgência), observatório (pesquisa), sala de cinema (vídeo). Nunca prédio de escritório em corte, fliperama, biblioteca de estantes, Shark Tank.
2. **Mostrar, não dizer.** Cada personagem faz a função na frente da câmera com um objeto + um painel 3D com o resultado: quadro com paleta "Aa" (design), balão com a pergunta que a skill faz, barra que vai de vermelho a verde (economia), celular que sai de 0 pra 9 posts, pilha que cresce até cair (excesso). Nosso: `b.gesto("mostra")` + `cenario.quadro/monitor` com textura do `telas.py`.
3. **Número de verdade que sobe.** Instalações, estrelas, custo R$ 0, % de cara de IA. Credibilidade + movimento. Nosso: `H.contadores` no estilo da skill (etiqueta limão), não pílula branca.
4. **Antes→depois em número** dentro da mesma cena (0% → 100%, 0/7 → 7/7). Bom pro formato "Antes × depois na mesma sala".
5. **Virada antes do último item** ("Mas o que mais me impressionou…", "Mas não instala as 15"). Segura a retenção no fim.
6. **Fechamento com o time inteiro junto** + CTA. Nosso: foto de grupo do ELENCO + "Comenta GUIA".
7. **Ritmo:** troca de plano a cada 1,5–3 s, uma frase curta por item, 33–42 s no total (o de 60 s é o que mais cansa).
8. **Câmera:** close 3/4 no personagem que fala, panorâmica lateral entre salas, subida vertical em prédio, chicote entre cenários, close enorme de rosto pra apresentar um personagem.
9. **Iluminação:** noite com neon funciona bem pra fliperama/telhado; de dia com janela pra sala de aula/praia. Cada sala com cor própria.

## O que é marca deles (NUNCA usar)
- Tarja de papel creme com fita adesiva no topo; legenda laranja serifada palavra por palavra; contador em pílula branca com ícone; fileira de abas de departamento (DIR DEV MKT…); coração gigante "Curtiu?"; notificação de DM no CTA; marca d'água no canto superior direito.
- Roteiro "Montei um time/empresa de N Claudes", "o primeiro / o segundo", "Curte esse vídeo e comenta X que eu te mando no direct".
- Personagens: chapéu de detetive xadrez + lupa, safari, boné azul, boina preta + claquete, óculos de tela com código, CEO de terno e gravata, homem das cavernas com porrete, velhinho de bigode branco, agente de óculos escuros, estagiário de boné azul, tubarões de terno. → Use o `ELENCO` (ver `ELENCO.md`).
