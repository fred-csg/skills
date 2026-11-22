// Lápis Vivo — vídeo de apresentação da skill (locução: audio/locucao.mp3 → words.js)
LV.config({ tema: 'grafite', duracao: 24.7 });
LV.roteiro(({ w, we, p }) => {
  // GANCHO: no quadro 0 o lápis já está no meio do título
  p.titulo('Escrito por um lápis', { at: -.75, dur: 1.9 });
  p.sub('quem segura o lápis?  *o Claude*', { at: w('quem'), dur: 1.75, destaque: '#F0895F' });

  const a = p.linha('Você manda o assunto', { cor: 'amarelo', at: w('voce'), dur: .85 });
  p.icone('💬', { x: 800, y: a.base - 22, size: 110, at: 6.12 });
  p.linha('e ele monta a aula no caderno:', { at: 6.14, dur: 1.3 });

  // lista em 2 colunas, cada item no tempo da palavra
  const item = (txt, x, y, t) => {
    p.desenho('check', { x: x + 18, y: y - 16, s: .3, cor: 'verde', at: t - .16, dur: .13, camera: false });
    return p.linha(txt, { x: x + 58, y, at: t + .02, dur: .34 });
  };
  const y1 = p.y, y2 = p.y + LV.PAUTA;
  item('título', 150, y1, w('titulo'));
  item('lista', 150, y2, w('lista'));
  item('tabela', 520, y1, w('tabela') + .06);
  item('conta', 520, y2, w('conta'));
  p.y = y2 + LV.PAUTA;

  // EXEMPLO: regra de três
  p.secao('Exemplo', { at: w('exemplo'), dur: .5 });
  p.linha('*3 vídeos* por semana', { at: w('3'), dur: .8, destaque: 'ink' });
  const t = p.tabela([['semanas', 'vídeos'], ['1', '3'], ['4', '?']], {
    x: 330, colW: 190, at: 12.28, durLinhas: .6,
    tempos: [[12.9, 13.24], [13.56, 13.7], [13.86, 14.12]] });
  p.chave(t.x0 - 24, t.meio(1), t.meio(2), { lado: 'esq', rotulo: '× 4', at: w('vezes'), dur: .28 });
  p.chave(t.x1 + 24, t.meio(1), t.meio(2), { lado: 'dir', rotulo: '× 4', at: 15.16, dur: .26 });
  p.linha('4 × 3 = *12 vídeos*', { centro: true, destaque: 'verde', at: 15.84, dur: .8 });

  // "no mês": 12 dias pintados de 30
  p.grade({ total: 30, cheios: 12, cols: 10, lado: 46, at: 16.74, durGrade: .42, dur: .55, rotulo: '*12* de 30 dias', atRotulo: 17.78 });

  // serve pra…
  const y3 = p.y;
  p.linha('matemática', { y: y3, at: 18.3, dur: .36, size: 48 });
  p.linha('finanças', { y: y3, x: 440, at: w('financas') + .08, dur: .34, size: 48 });
  p.linha('receita', { y: y3, x: 690, at: w('receita') + .04, dur: .32, size: 48 });
  p.y = y3 + LV.PAUTA;
  const q = p.linha('o que você quiser explicar', { cor: 'amarelo', at: w('o que'), dur: 1.0 });
  p.sublinhar(q, { at: 21.2, dur: .3 });

  p.cta('Comenta GUIA', 'que eu te mando', { at: w('comenta') - .05, seta: 'comentario' });
});
