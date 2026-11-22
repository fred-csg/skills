// Hand Drawing — biblioteca de desenhos traçados à mão (vetor, zero crédito).
// Cada desenho = lista de traços {d, cor?, fill?, w?} em coordenadas centradas em 0,0 (≈ caixa de ±100).
// A ORDEM dos traços é a ordem em que a mão desenha. cor: 'acc' = destaque, sem cor = cor do item.
// Uso no roteiro: c.desenho('alvo', {x, y, s, at, dur}); com parâmetros: c.desenho('circulo', {params:[w, h]}).
(() => {
  const R = HD.rnd;
  const j = (a = 1.3) => (R() - .5) * 2 * a;
  // polilinha suavizada (Catmull-Rom → Bézier) com tremidinha de mão
  const L = (pts, o = {}) => {
    const jit = o.j ?? 1.2;
    const P = pts.map(([x, y], i) => (i === 0 || i === pts.length - 1) && !o.jEnds ? [x, y] : [x + j(jit), y + j(jit)]);
    if (P.length === 2) {
      const [a, b] = P;
      P.splice(1, 0, [a[0] + (b[0] - a[0]) * .5 + j(jit * .8), a[1] + (b[1] - a[1]) * .5 + j(jit * .8)]);
    }
    let d = `M${P[0][0].toFixed(1)} ${P[0][1].toFixed(1)}`;
    for (let i = 0; i < P.length - 1; i++) {
      const p0 = P[i - 1] || P[i], p1 = P[i], p2 = P[i + 1], p3 = P[i + 2] || p2;
      const t = o.reto ? 0 : .18;
      const c1 = [p1[0] + (p2[0] - p0[0]) * t, p1[1] + (p2[1] - p0[1]) * t];
      const c2 = [p2[0] - (p3[0] - p1[0]) * t, p2[1] - (p3[1] - p1[1]) * t];
      d += ` C${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
    }
    return { d, cor: o.cor, w: o.w, fill: o.fill };
  };
  // elipse à mão: começa em a0 (graus), passa um pouco do fechamento (sobra)
  const elip = (cx, cy, rx, ry, o = {}) => {
    const a0 = (o.a0 ?? -100) * Math.PI / 180, sobra = (o.sobra ?? 18) * Math.PI / 180, n = o.n || 26;
    const pts = [];
    for (let k = 0; k <= n; k++) {
      const a = a0 + (Math.PI * 2 + sobra) * k / n, r = 1 + j(.025) + (k / n) * (o.espiral ?? .05);
      pts.push([cx + Math.cos(a) * rx * r, cy + Math.sin(a) * ry * r]);
    }
    return L(pts, { j: 0, cor: o.cor, w: o.w });
  };
  const arco = (cx, cy, r, g0, g1, o = {}) => {
    const n = o.n || 12, pts = [];
    for (let k = 0; k <= n; k++) { const a = (g0 + (g1 - g0) * k / n) * Math.PI / 180; pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * (o.ry || r)]); }
    return L(pts, { j: o.j ?? .6, cor: o.cor, w: o.w });
  };
  // retângulo arredondado num traço só (começa no canto sup. esquerdo, sentido horário)
  const ret = (x, y, w, h, r = 10, o = {}) => {
    const k = .45;
    const pts = [[x + r, y], [x + w - r, y], [x + w - r * k, y + r * k], [x + w, y + r], [x + w, y + h - r], [x + w - r * k, y + h - r * k],
      [x + w - r, y + h], [x + r, y + h], [x + r * k, y + h - r * k], [x, y + h - r], [x, y + r], [x + r * k, y + r * k], [x + r + 2, y - .5]];
    return L(pts, { j: o.j ?? .9, cor: o.cor, w: o.w, reto: false });
  };
  const ponto = (cx, cy, r, cor) => ({ d: `M${cx - r} ${cy}a${r} ${r} 0 1 0 ${2 * r} 0a${r} ${r} 0 1 0 ${-2 * r} 0`, fill: true, cor });
  const seta = (x1, y1, x2, y2, o = {}) => {
    const a = Math.atan2(y2 - y1, x2 - x1), h = o.cab || 30, ab = .55;
    const meio = o.curva ? [[(x1 + x2) / 2 + o.curva * Math.sin(a), (y1 + y2) / 2 - o.curva * Math.cos(a)]] : [];
    return [L([[x1, y1], ...meio, [x2, y2]], { cor: o.cor, j: .8 }),
      L([[x2 - h * Math.cos(a - ab), y2 - h * Math.sin(a - ab)], [x2, y2], [x2 - h * Math.cos(a + ab), y2 - h * Math.sin(a + ab)]], { cor: o.cor, j: .5, reto: true })];
  };
  const boneco = (x = 0, y = 0, s = 1, o = {}) => {
    const P = (a, b) => [x + a * s, y + b * s];
    const r = [
      elip(...P(0, -112), 30 * s, 30 * s, { a0: -120, sobra: 12 }),
      ponto(...P(-10, -116), 3.6 * s), ponto(...P(10, -116), 3.6 * s),
      arco(...P(0, -104), 11 * s, 20, 160, { n: 6, j: .3 }),
      L([P(0, -82), P(1, -20), P(0, 25)]),
      L([P(-42, -30), P(-20, -55), P(0, -66), P(20, -55), P(44, -34)]),
      L([P(-30, 100), P(-16, 55), P(0, 25), P(16, 58), P(32, 100)]),
    ];
    if (o.feliz === false) r[3] = arco(...P(0, -92), 11 * s, 200, 340, { n: 6, j: .3 });
    return r;
  };

  HD.doodles = {
    // ----- marcações (usadas por c.circular / c.sublinhar / c.riscar) -----
    circulo: (w = 220, h = 90) => [elip(0, 0, w / 2 + 26, h / 2 + 20, { a0: -165, sobra: 24, espiral: .07 })],
    sublinhado: (w = 300) => [L([[-w / 2, 4], [-w / 6, -2], [w / 6, 3], [w / 2, -3]], { j: 1.5 })],
    risco: (w = 300) => [L([[-w / 2 - 10, 8], [w / 2 + 10, -8]], { j: 1 })],
    'sublinhado-duplo': (w = 300) => [L([[-w / 2, 0], [w / 2, -4]]), L([[-w / 2 + 20, 16], [w / 2 - 10, 12]])],

    // ----- sinais -----
    check: () => [L([[-55, -2], [-18, 40], [60, -55]], { j: 1, reto: true })],
    xis: () => [L([[-50, -50], [50, 50]]), L([[50, -50], [-50, 50]])],
    'seta-baixo': () => seta(0, -95, 0, 90),
    'seta-cima': () => seta(0, 95, 0, -90),
    'seta-dir': () => seta(-95, 0, 95, 0),
    'seta-esq': () => seta(95, 0, -95, 0),
    'seta-curva': () => seta(-90, 50, 85, 10, { curva: 70 }),
    brilho: () => {   // 3 estrelinhas de 4 pontas
      const est = (x, y, r) => L([[x, y - r], [x + r * .22, y - r * .22], [x + r, y], [x + r * .22, y + r * .22], [x, y + r], [x - r * .22, y + r * .22], [x - r, y], [x - r * .22, y - r * .22], [x, y - r]], { j: .4, reto: true });
      return [est(-30, -10, 42), est(48, -55, 24), est(42, 50, 18)];
    },
    raios: () => [L([[-50, -10], [-80, -20]]), L([[-30, -45], [-50, -75]]), L([[0, -55], [0, -88]]), L([[30, -45], [50, -75]]), L([[50, -10], [80, -20]])],
    interrogacao: () => [L([[-38, -48], [-30, -78], [0, -92], [32, -80], [40, -50], [18, -25], [2, -5], [0, 25]]), ponto(0, 62, 9)],
    exclamacao: () => [L([[0, -90], [-2, 0], [0, 30]], { w: 1.3 }), ponto(0, 68, 10)],
    coracao: () => [L([[0, 70], [-55, 18], [-75, -25], [-58, -62], [-22, -66], [0, -35], [22, -66], [58, -62], [75, -25], [55, 18], [0, 70]], { j: .8 })],
    cifrao: () => [L([[42, -48], [20, -66], [-18, -66], [-42, -45], [-30, -15], [0, -4], [32, 8], [44, 38], [22, 64], [-20, 64], [-45, 44]]), L([[0, -95], [0, 95]])],
    raio: () => [L([[20, -95], [-40, 10], [8, 10], [-20, 95], [45, -15], [0, -15], [20, -95]], { j: .5, reto: true })],

    // ----- objetos -----
    lampada: () => [
      L([[-25, 40], [-30, 15], [-52, -12], [-55, -50], [-30, -82], [0, -92], [30, -82], [55, -50], [52, -12], [30, 15], [25, 40]]),
      L([[-26, 52], [26, 52]]), L([[-22, 66], [22, 66]]), L([[-12, 80], [12, 80]]),
      L([[-12, 20], [-8, -15], [0, 0], [8, -15], [12, 20]], { j: .4 }),
      L([[-80, -92], [-95, -105]], { cor: 'acc' }), L([[0, -112], [0, -132]], { cor: 'acc' }), L([[80, -92], [95, -105]], { cor: 'acc' }),
      L([[-90, -40], [-110, -40]], { cor: 'acc' }), L([[90, -40], [110, -40]], { cor: 'acc' }),
    ],
    alvo: () => [
      elip(0, 0, 92, 92, { a0: -60, sobra: 10, espiral: .02 }), elip(0, 0, 62, 62, { a0: 150, sobra: 10, espiral: .02 }),
      elip(0, 0, 32, 32, { a0: 20, sobra: 8, espiral: .02, cor: 'acc' }), ponto(0, 0, 13, 'acc'),
      L([[0, 0], [95, -95]], { j: .4 }), L([[95, -95], [92, -125]]), L([[95, -95], [125, -98]]), L([[105, -105], [104, -132]]), L([[105, -105], [132, -106]]),
    ],
    celular: () => {
      const r = [ret(-62, -112, 124, 224, 18), L([[-18, -97], [18, -97]], { j: .3 }), ret(-46, -84, 92, 16, 6, { j: .4 })];
      for (let a = 0; a < 3; a++) for (let b = 0; b < 3; b++) r.push(ret(-46 + a * 33, -56 + b * 46, 26, 36, 5, { j: .4 }));
      r.push(ret(-46 + 33, -56, 26, 36, 5, { j: .3, cor: 'acc' }));
      return r;
    },
    prancheta: () => {
      const r = [ret(-72, -95, 144, 195, 12), ret(-30, -110, 60, 28, 8)];
      for (let k = 0; k < 4; k++) { r.push(ret(-50, -55 + k * 38, 20, 20, 4, { j: .3 })); r.push(L([[-18, -45 + k * 38], [48, -45 + k * 38]])); }
      r.push(L([[-48, -45], [-40, -36], [-26, -60]], { cor: 'acc', j: .3, reto: true }));
      return r;
    },
    lupa: () => [elip(-15, -15, 58, 58, { a0: -40, sobra: 12, espiral: .02 }), L([[28, 28], [82, 82]], { w: 2 }), arco(-15, -15, 38, 200, 260, { cor: 'acc' })],
    nuvem: () => [L([[-80, 20], [-100, -10], [-80, -45], [-45, -55], [-25, -85], [15, -88], [40, -62], [80, -60], [100, -25], [85, 15], [50, 25], [10, 35], [-35, 30], [-80, 20]], { j: 1 }),
      elip(-55, 55, 12, 10, { sobra: 5 }), elip(-75, 82, 7, 6, { sobra: 5 })],
    boneco: () => boneco(),
    'boneco-triste': () => boneco(0, 0, 1, { feliz: false }),
    grupo: () => [...boneco(-75, 18, .62), ...boneco(0, 0, .72), ...boneco(78, 18, .62)],
    cronometro: () => [elip(0, 12, 82, 82, { a0: -80, sobra: 10, espiral: .02 }), L([[0, -70], [0, -88]]), ret(-16, -108, 32, 18, 5),
      L([[56, -52], [70, -66]]), L([[0, 12], [0, -45]], { cor: 'acc' }), L([[0, 12], [32, 30]], { cor: 'acc' }), ponto(0, 12, 6, 'acc')],
    porta: () => [L([[-60, 110], [-60, -110], [60, -110], [60, 110]], { reto: true, j: .6 }), L([[60, 110], [-10, 90], [-10, -95], [60, -110]], { j: .6 }), ponto(5, 0, 6)],
    etiqueta: () => [L([[-30, -80], [70, -80], [70, 50], [10, 95], [-50, 50], [-50, -60], [-30, -80]], { reto: true, j: .6 }),
      elip(10, -50, 10, 10, { sobra: 6 }), L([[25, -2], [10, -12], [-4, -4], [0, 10], [18, 18], [22, 32], [8, 42], [-8, 34]], { cor: 'acc', j: .4 }), L([[10, -22], [8, 52]], { cor: 'acc', j: .3 })],
    trofeu: () => [L([[-55, -80], [55, -80], [50, -20], [25, 15], [0, 22], [-25, 15], [-50, -20], [-55, -80]], { j: .6 }),
      L([[-55, -62], [-85, -60], [-82, -28], [-48, -15]], { j: .5 }), L([[55, -62], [85, -60], [82, -28], [48, -15]], { j: .5 }),
      L([[0, 22], [0, 55]]), ret(-38, 55, 76, 26, 6), arco(0, -48, 18, 200, 340, { cor: 'acc' })],
    grafico: () => [L([[-90, -85], [-90, 85], [95, 85]], { reto: true }), ret(-70, 35, 30, 50, 4), ret(-25, 5, 30, 80, 4), ret(20, -30, 30, 115, 4, { cor: 'acc' }),
      ...seta(-75, 10, 80, -80, { cor: 'acc', cab: 24 })],
    balao: () => [L([[-90, -40], [-70, -78], [0, -90], [70, -78], [92, -40], [75, 0], [20, 15], [-25, 15], [-55, 50], [-50, 12], [-82, -5], [-90, -40]], { j: .8 }),
      L([[-45, -45], [45, -45]]), L([[-45, -20], [20, -20]])],
    presente: () => [ret(-70, -30, 140, 110, 6), ret(-80, -55, 160, 28, 6), L([[0, -55], [0, 80]], { cor: 'acc' }),
      L([[0, -55], [-30, -85], [-45, -70], [0, -55]], { cor: 'acc', j: .4 }), L([[0, -55], [30, -85], [45, -70], [0, -55]], { cor: 'acc', j: .4 })],
    carrinho: () => [L([[-95, -70], [-70, -70], [-45, 35], [65, 35], [85, -45], [-62, -45]], { reto: true, j: .6 }), elip(-30, 62, 14, 14, { sobra: 6 }), elip(50, 62, 14, 14, { sobra: 6 })],
    dinheiro: () => [ret(-95, -50, 190, 100, 8), elip(0, 0, 30, 30, { sobra: 8 }), L([[10, -14], [0, -18], [-10, -10], [-4, 0], [8, 4], [10, 14], [0, 18], [-10, 12]], { cor: 'acc', j: .3 }),
      ponto(-68, -28, 4), ponto(68, 28, 4)],
    casa: () => [L([[-90, -5], [0, -90], [90, -5]], { reto: true, j: .6 }), L([[-70, -20], [-70, 85], [70, 85], [70, -20]], { reto: true, j: .6 }), ret(-20, 30, 40, 55, 4, { cor: 'acc' })],
    envelope: () => [ret(-95, -60, 190, 125, 8), L([[-92, -55], [0, 15], [92, -55]], { j: .5 })],
    cadeado: () => [ret(-60, -15, 120, 100, 12), arco(0, -15, 42, 180, 360, { ry: 55 }), ponto(0, 25, 9, 'acc'), L([[0, 30], [0, 55]], { cor: 'acc' })],
    documento: () => [L([[-60, -95], [30, -95], [65, -60], [65, 95], [-60, 95], [-60, -95]], { reto: true, j: .5 }), L([[30, -95], [30, -60], [65, -60]], { j: .4 }),
      L([[-38, -40], [40, -40]]), L([[-38, -10], [40, -10]]), L([[-38, 20], [40, 20]]), L([[-38, 50], [10, 50]], { cor: 'acc' })],
    megafone: () => [L([[-70, -25], [40, -75], [40, 75], [-70, 25], [-70, -25]], { reto: true, j: .5 }), L([[-55, 22], [-45, 75], [-20, 72], [-25, 32]]),
      L([[65, -35], [90, -50]], { cor: 'acc' }), L([[70, 0], [100, 0]], { cor: 'acc' }), L([[65, 35], [90, 50]], { cor: 'acc' })],
    relogio: () => [elip(0, 0, 90, 90, { a0: -80, sobra: 10, espiral: .02 }), L([[0, 0], [0, -58]]), L([[0, 0], [40, 22]], { cor: 'acc' }), ponto(0, 0, 6)],
    engrenagem: () => {
      const pts = [];
      for (let k = 0; k <= 48; k++) { const a = k / 48 * Math.PI * 2, r = (k % 6 < 3) ? 80 : 62; pts.push([Math.cos(a) * r, Math.sin(a) * r]); }
      return [L(pts, { j: .4, reto: true }), elip(0, 0, 24, 24, { sobra: 8 })];
    },
  };
})();
