// Hand Drawing — roteiro de exemplo (demo da skill, 13 s).
// Tema: ?tema=papel | lousa-verde | lousa-preta na URL (render: --q tema=...), ou fixo em HD.config.
HD.config({ tema: new URLSearchParams(location.search).get('tema') || 'papel', duracao: 13.6 });

HD.roteiro(({ w, we, cena, legendas }) => {
  legendas({ destaques: ['desenhado', 'isso', 'copy', 'mão', 'desenha', 'after', 'effects', 'quadro', 'papel', 'verde', 'preta', 'comenta'] });

  // 1) GANCHO — quadro 0 já com a mão escrevendo
  let c = cena(0, 3.0);
  let tt = c.texto('PAGA EDITOR PRA\nVÍDEO DESENHADO?', { y: 360, size: 76, at: 0, dur: 1.9 });
  c.desenho('dinheiro', { y: 820, s: 1.35, at: tt.fim - .05, dur: .75 });
  c.desenho('xis', { y: 820, s: 1.7, cor: 'acc', at: w('desenhado') + .45, dur: .32 });

  // 2) PROVA — a copy (boneco com a lista, desenho gerado por IA e vetorizado) vira desenho
  c = cena(w('olha') - .12, w('sem') - .12);
  tt = c.texto('OLHA ISSO:', { y: 360, size: 80, at: w('olha'), dur: .5 });
  c.arte('boneco_lista', { x: 320, y: 880, w: 250, at: w('mando'), dur: 1.4 });
  c.desenho('seta-curva', { x: 560, y: 760, s: .7, at: w('desenha') - .1, dur: .3 });
  const md = c.texto('A MÃO\nDESENHA', { x: 730, y: 860, size: 60, cor: 'acc', at: w('desenha') + .15, dur: .7 });
  c.sublinhar(md.linhas[1], { y: md.linhas[1].base + 20, at: we('frase') - .25, dur: .25 });

  // 3) OBJEÇÃO — riscado
  c = cena(w('sem') - .12, w('escolhe') - .12);
  tt = c.texto('SEM AFTER\nEFFECTS', { y: 820, size: 104, at: w('sem'), dur: .9 });
  tt.linhas.forEach((ln, i) => c.riscar(ln, { y: ln.y, at: we('effects') - .05 + i * .2, dur: .18 }));

  // 4) ESCOLHA — três quadros
  c = cena(w('escolhe') - .12, w('comenta') - .12);
  c.texto('ESCOLHE O QUADRO:', { y: 360, size: 70, at: w('escolhe'), dur: .65 });
  const q = [{ d: 'M-80 -100 L80 -100 L80 100 L-80 100 Z' }];
  [['PAPEL', 'papel'], ['LOUSA\nVERDE', 'verde'], ['LOUSA\nPRETA', 'preta']].forEach(([rot, pal], i) => {
    const x = 225 + i * 260, t0 = w(pal) - .15;
    c.desenho(q, { x, y: 760, at: t0, dur: .32 });
    c.texto(rot, { x, y: 960, size: 40, cor: 'acc', at: t0 + .3, vel: .03, linha: 1.05 });
  });

  // 5) CTA
  c = cena(w('comenta') - .12, 13.6);
  c.texto('COMENTA', { y: 560, size: 96, at: w('comenta'), dur: .5 });
  const mao = c.texto('MÃO', { y: 820, size: 150, cor: 'acc', at: w('mão', 2) - .05, dur: .45 });
  c.circular(mao, { at: mao.fim + .02, dur: .35 });
  c.desenho('seta-baixo', { y: 1110, s: .9, at: w('mando', 2) - .1, dur: .3 });
});
