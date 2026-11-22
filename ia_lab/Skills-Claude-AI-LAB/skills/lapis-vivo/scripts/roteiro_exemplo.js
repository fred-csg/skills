// Lápis Vivo — roteiro de exemplo SEM locução (tempos em segundos). Com locução, troque os números
// por w('palavra') / we('palavra') — ver references/roteiro-api.md.
LV.config({ tema: 'grafite', duracao: 27 });
LV.roteiro(({ p }) => {
  p.titulo('Regra de três', { at: .15 });
  p.sub('em 20 segundos');
  p.linha('O que cai na prova?', { cor: 'amarelo' });
  p.icone('📋', { x: 790, y: p.y - 150, size: 150 });
  p.linha('900 questões de 20 provas');
  p.grade({ total: 45, cheios: 38, cols: 9, rotulo: '*38* de 45' });

  const y0 = p.y;
  p.lista(['regra de três', 'porcentagem', 'juros']);
  p.y = y0;
  p.lista(['média', 'área', 'volume'], { x: 520 });

  p.secao('Enem 2012');
  p.linha('5 gotas para cada 2 kg');
  p.linha('a mãe deu 30 gotas');
  const q = p.linha('massa da criança?', { cor: 'amarelo' });
  p.sublinhar(q);

  p.pular(.5);
  const t = p.tabela([['gotas', 'quilos'], ['5', '2'], ['30', '?']], { x: 300, colW: 150 });
  p.chave(t.x0 - 22, t.meio(1), t.meio(2), { lado: 'esq', rotulo: '× 6' });
  p.chave(t.x1 + 22, t.meio(1), t.meio(2), { lado: 'dir', rotulo: '× 6' });
  p.linha('6 × 2 = *12 kg*', { centro: true, destaque: 'verde' });

  p.cta('Comenta AULA', 'que eu te mando *completa*', { seta: 'comentario' });
});
