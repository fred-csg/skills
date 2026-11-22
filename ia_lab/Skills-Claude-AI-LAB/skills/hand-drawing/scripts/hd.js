// Hand Drawing — motor. Uma mão (marcador ou giz) escreve e desenha a copy num quadro comprido;
// cada cena é um "quadro" ao lado do anterior e a câmera chicoteia pro próximo.
// Tudo é função do tempo: HD.seek(t) deixa a tela exatamente no instante t (render quadro a quadro).
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const HD = window.HD = {};
  const QW = 1080, QH = 1920, BOARD = 1400;        // largura útil, altura, distância entre quadros

  const TEMAS = {
    'papel':       { fundo: 'fundo_papel.jpg',       ink: '#1C1C1C', acc: '#E8452C', mao: 'marcador', giz: false,
                     vinheta: 'rgba(70,58,44,.13)', sombra: [40, 30, 20, .26] },
    'lousa-verde': { fundo: 'fundo_lousa_verde.jpg', ink: '#F2F0E6', acc: '#FFD54A', mao: 'giz', giz: true,
                     vinheta: 'rgba(0,10,4,.55)', sombra: [0, 0, 0, .42] },
    'lousa-preta': { fundo: 'fundo_lousa_preta.jpg', ink: '#F0F0EB', acc: '#D7FF3A', mao: 'giz', giz: true,
                     vinheta: 'rgba(0,0,0,.6)', sombra: [0, 0, 0, .5] },
  };
  const MAOS = {   // = assets/maos.json (prep_assets.py + estender_braco.py)
    marcador: { arquivo: 'mao_marcador.webp', w: 1907, h: 1723, ponta: [10, 1710] },
    giz:      { arquivo: 'mao_giz.webp',      w: 1858, h: 1785, ponta: [11, 1767] },
  };

  const cfg = HD.cfg = { tema: 'papel', maoEscala: .56, fonte: 'PM', cx: 520, assets: 'assets/', legY: 1395 };
  HD.config = o => { Object.assign(cfg, o); };
  HD.CX = 520;
  HD.cues = [];
  HD.words = window.WORDS || [];

  // ---------- util ----------
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, p) => a + (b - a) * p;
  const E = {
    inOut: p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2,
    out: p => 1 - Math.pow(1 - p, 3),
    outBack: p => { const c = 1.9; return 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); },
    whip: p => p < .5 ? 16 * p ** 5 : 1 - Math.pow(-2 * p + 2, 5) / 2,
  };
  HD.E = E;
  const el = (tag, attrs = {}, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  let seed = 1;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  HD.rnd = rnd;
  const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9%]/g, '');

  // ---------- tempos pelas palavras da locução (words.js) ----------
  // HD.w('dez') = início da 1ª ocorrência; HD.w('dez', 2) = da 2ª; HD.we(...) = fim da palavra
  const achar = (txt, n = 1) => {
    const alvo = txt.split(/\s+/).map(norm);
    let k = 0;
    for (let i = 0; i < HD.words.length; i++) {
      if (alvo.every((a, j) => HD.words[i + j] && norm(HD.words[i + j].w) === a) && ++k === n)
        return [HD.words[i], HD.words[i + alvo.length - 1]];
    }
    throw new Error(`palavra não encontrada na locução: "${txt}" (#${n})`);
  };
  HD.w = (txt, n) => achar(txt, n)[0].s;
  HD.we = (txt, n) => achar(txt, n)[1].e;

  // ---------- estrutura ----------
  const cenas = [], itens = [], segs = [];
  let stage, world, bgEl, maoEl, legEl, blurNode, T;

  function montar() {
    T = Object.assign({}, TEMAS[cfg.tema], cfg.cores || {});
    if (cfg.mao) T.mao = cfg.mao;
    document.documentElement.style.setProperty('--ink', T.ink);
    document.documentElement.style.setProperty('--acc', T.acc);
    document.body.className = 'tema-' + cfg.tema + (T.giz ? ' giz' : '');
    if (T.giz) document.documentElement.style.setProperty('--grao', `url(${graoGiz()})`);
    stage = document.getElementById('stage');
    world = document.getElementById('world');
    bgEl = document.getElementById('bg');
    bgEl.style.backgroundImage = `url(${cfg.assets}${T.fundo})`;
    document.getElementById('vinheta').style.background =
      `radial-gradient(ellipse 75% 62% at 50% 46%, transparent 55%, ${T.vinheta} 100%)`;
    const m = MAOS[T.mao];
    maoEl = document.createElement('img');
    maoEl.id = 'mao'; maoEl.src = cfg.assets + m.arquivo;
    maoEl.style.width = m.w * cfg.maoEscala + 'px';
    maoEl.style.transformOrigin = `${m.ponta[0] * cfg.maoEscala}px ${m.ponta[1] * cfg.maoEscala}px`;
    world.appendChild(maoEl);
    legEl = document.getElementById('legenda');
    blurNode = document.getElementById('mblur-node');
    document.getElementById('tint-ink-cor').setAttribute('flood-color', T.ink);
    document.getElementById('tint-acc-cor').setAttribute('flood-color', T.acc);
  }

  // grão do giz gerado em canvas (mask-image de arquivo local é bloqueada por CORS no file://)
  function graoGiz() {
    const n = 512, cv = document.createElement('canvas'); cv.width = cv.height = n;
    const ctx = cv.getContext('2d');
    const camada = (tam, blur) => {          // ruído em baixa resolução ampliado = manchas
      const c2 = document.createElement('canvas'); c2.width = c2.height = tam;
      const x2 = c2.getContext('2d'), d = x2.createImageData(tam, tam);
      for (let i = 0; i < d.data.length; i += 4) { const v = rnd() * 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; }
      x2.putImageData(d, 0, 0);
      const c3 = document.createElement('canvas'); c3.width = c3.height = n;
      const x3 = c3.getContext('2d'); x3.filter = `blur(${blur}px)`; x3.imageSmoothingEnabled = true;
      for (const dx of [-n, 0, n]) for (const dy of [-n, 0, n]) x3.drawImage(c2, dx, dy, n, n);   // emendável
      return x3.getImageData(0, 0, n, n).data;
    };
    const fino = camada(512, .4), medio = camada(128, 1.2), largo = camada(32, 4);
    const out = ctx.createImageData(n, n);
    for (let i = 0; i < out.data.length; i += 4) {
      const g = (.5 * fino[i] + .3 * medio[i] + .2 * largo[i]) / 255;          // ~0..1, média .5
      let a = clamp((g - .24) / .34);
      if (fino[i] > 246) a *= .15;                                             // falhas do giz
      out.data[i] = out.data[i + 1] = out.data[i + 2] = 255; out.data[i + 3] = a ** 1.3 * 255;
    }
    ctx.putImageData(out, 0, 0);
    return cv.toDataURL();
  }

  // Cena = um quadro novo. Coordenadas dos itens: as da tela (0..1080 × 0..1920).
  HD.cena = (t0, t1, o = {}) => {
    const i = cenas.length;
    const ox = i * BOARD;
    const wrap = document.createElement('div');
    wrap.className = 'quadro'; wrap.style.left = ox + 'px';
    const fotos = el('svg', { class: 'camada fotos', width: QW, height: QH, viewBox: `0 0 ${QW} ${QH}` });
    const ink = el('svg', { class: 'camada ink', width: QW, height: QH, viewBox: `0 0 ${QW} ${QH}` });
    el('defs', {}, ink);
    wrap.append(fotos, ink);
    world.insertBefore(wrap, maoEl);
    const c = { i, t0, t1, ox, wrap, fotos, ink, zoom: o.zoom ?? 1.035, foco: o.foco || null };
    cenas.push(c);
    const api = {
      cena: c,
      texto: (s, op) => texto(c, s, op),
      desenho: (nome, op) => desenho(c, nome, op),
      arte: (nome, op) => arte(c, nome, op),
      foto: (src, op) => foto(c, src, op),
      circular: (box, op = {}) => desenho(c, HD.doodles.circulo(box.w, box.h), Object.assign({ x: box.x, y: box.y, cor: 'acc' }, op)),
      sublinhar: (box, op = {}) => desenho(c, HD.doodles.sublinhado(box.w), Object.assign({ x: box.x, y: box.y, cor: 'acc' }, op)),
      riscar: (box, op = {}) => desenho(c, HD.doodles.risco(box.w), Object.assign({ x: box.x, y: box.y, cor: 'acc' }, op)),
    };
    return api;
  };

  // segmento de caneta: entre t0 e t1 a ponta percorre f(p) (coordenadas do quadro)
  const seg = (c, t0, t1, f) => { segs.push({ c, t0, t1, f }); return segs[segs.length - 1]; };

  // ---------- TEXTO manuscrito ----------
  // op: x (centro), y (linha de base da 1ª linha), size, cor ('ink'|'acc'|'#hex'), at, dur (total) ou vel (s/letra), linha, ancora
  function texto(c, s, op = {}) {
    const size = op.size || 74, lh = (op.linha || 1.14) * size;
    const x = op.x ?? cfg.cx, y0 = op.y ?? 380;
    const cor = corDe(op.cor);
    const linhas = s.split('\n');
    const nChars = s.replace(/\s|\n/g, '').length;
    // dur = tempo total real (letras + pausas entre palavras + trocas de linha)
    const nEsp = linhas.reduce((a, l) => a + Math.max(0, l.trim().split(/\s+/).length - 1), 0);
    const vel = op.dur ? op.dur / Math.max(1, nChars + nEsp * .9 + (linhas.length - 1) * 2.5) : (op.vel || .062);
    let fim = 0;
    let t = op.at ?? c.t0 + .1;
    const boxes = [];
    linhas.forEach((ln, li) => {
      const y = y0 + li * lh;
      const id = `clip${itens.length}_${li}`;
      const cp = el('clipPath', { id }, c.ink.querySelector('defs'));
      const rect = el('rect', { x: -9999, y: y - size * 1.25, width: 0, height: size * 1.9 }, cp);
      const tx = el('text', { x, y, 'text-anchor': op.ancora || 'middle', 'font-size': size, fill: cor,
        'clip-path': `url(#${id})`, class: 'hand' + (op.classe ? ' ' + op.classe : '') }, c.ink);
      tx.textContent = ln;
      const glifos = [];
      for (let k = 0; k < ln.length; k++) {
        if (ln[k] === ' ') continue;
        const b = tx.getExtentOfChar(k);
        glifos.push({ x0: b.x, x1: b.x + b.width, top: y - size * .72, bot: y + size * .02, t0: 0, t1: 0, esp: k > 0 && ln[k - 1] === ' ' });
      }
      if (!glifos.length) return;
      const xa = Math.min(...glifos.map(g => g.x0)), xb = Math.max(...glifos.map(g => g.x1));
      boxes.push({ x: (xa + xb) / 2, y: y - size * .35, w: xb - xa, h: size, x0: xa, x1: xb, base: y });
      rect.setAttribute('x', xa - size * .35);
      const L = { rect, glifos, xa, size };
      glifos.forEach((g, gi) => {
        // pequena pausa entre palavras (o espaço anterior) e letras ligeiramente irregulares
        const prev = glifos[gi - 1];
        if (prev && g.esp) t += vel * .9;
        g.t0 = t; g.t1 = t + vel * (0.85 + rnd() * .3);
        t = g.t1; fim = t;
        const zz = 3 + Math.round(rnd());           // zigue-zague dentro da letra
        seg(c, g.t0, g.t1, p => {
          const q = p * zz, k = Math.floor(Math.min(q, zz - 1e-6)), f = q - k;
          const xA = lerp(g.x0, g.x1, k / zz), xB = lerp(g.x0, g.x1, (k + 1) / zz);
          const yA = k % 2 ? g.top : g.bot, yB = k % 2 ? g.bot : g.top;
          return [lerp(xA, xB, f), lerp(yA, yB, f)];
        });
      });
      itens.push({ tipo: 'texto', c, L, seek(tt) {
        let rx = L.xa - L.size * .35;
        for (const g of L.glifos) {
          if (tt >= g.t1) rx = g.x1 + L.size * .2;
          else if (tt > g.t0) { rx = lerp(g.x0, g.x1, (tt - g.t0) / (g.t1 - g.t0)) + L.size * .06; break; }
          else break;
        }
        L.rect.setAttribute('width', Math.max(0, rx - (L.xa - L.size * .35)));
      } });
      t += vel * 2.5;                                // troca de linha (só conta se houver outra)
    });
    const all = boxes.length ? {
      x: (Math.min(...boxes.map(b => b.x0)) + Math.max(...boxes.map(b => b.x1))) / 2,
      y: (boxes[0].y + boxes[boxes.length - 1].y) / 2,
      w: Math.max(...boxes.map(b => b.w)), h: boxes[boxes.length - 1].base - boxes[0].base + size,
      fim, linhas: boxes } : { fim: t, linhas: [] };
    return all;   // caixa do texto (pra circular/sublinhar) + all.fim = quando termina
  }

  function corDe(c) {
    if (!c || c === 'ink') return 'var(--ink)';
    if (c === 'acc') return 'var(--acc)';
    return c;
  }

  // ---------- DESENHO vetorial (biblioteca doodles.js ou paths próprios) ----------
  // nome: string da biblioteca, ou array de traços [{d, cor, fill, w}] em coordenadas centradas em 0,0
  // op: x, y, s (escala), rot (graus), cor (cor padrão), at, dur, w (espessura), vel (px/s)
  function desenho(c, nome, op = {}) {
    const tracos = typeof nome === 'string' ? HD.doodles[nome](...(op.params || [])) : nome;
    if (!tracos) throw new Error('doodle inexistente: ' + nome);
    const x = op.x ?? cfg.cx, y = op.y ?? 900, s = op.s ?? 1, rot = (op.rot || 0) * Math.PI / 180;
    const g = el('g', { transform: `translate(${x} ${y}) rotate(${op.rot || 0}) scale(${s})` }, c.ink);
    const w = (op.w || 7) / s;
    const objs = tracos.map(tr => {
      const cor = corDe(tr.cor || op.cor);
      if (tr.fill && !tr.stroke) {
        const p = el('path', { d: tr.d, fill: cor, opacity: 0 }, g);
        return { p, fill: true };
      }
      const p = el('path', { d: tr.d, fill: 'none', stroke: cor, 'stroke-width': (tr.w || 1) * w,
        'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
      const len = p.getTotalLength();
      p.setAttribute('stroke-dasharray', `${len + 2} ${len + 2}`);
      p.setAttribute('stroke-dashoffset', len + 2);
      return { p, len, fillCor: tr.fill ? cor : null };
    });
    const total = objs.reduce((a, o) => a + (o.len || 0), 0) * s;
    const gap = .07;
    const nStroke = objs.filter(o => !o.fill).length;
    let dur = op.dur ?? clamp(total / (op.vel || 950), .35, 3.2);
    const tDraw = Math.max(.15, dur - gap * (nStroke - 1));
    let t = op.at ?? c.t0 + .2;
    const toW = (px, py) => [x + s * (px * Math.cos(rot) - py * Math.sin(rot)), y + s * (px * Math.sin(rot) + py * Math.cos(rot))];
    for (const o of objs) {
      if (o.fill) { o.t0 = t - gap * .5; o.t1 = o.t0 + .14; continue; }
      o.t0 = t; o.t1 = t + tDraw * (o.len * s / Math.max(1, total)); t = o.t1 + gap;
      const p = o.p, len = o.len;
      seg(c, o.t0, o.t1, q => { const pt = p.getPointAtLength(q * len); return toW(pt.x, pt.y); });
      if (o.fillCor) { o.p.setAttribute('fill', o.fillCor); o.p.setAttribute('fill-opacity', 0); }
    }
    itens.push({ tipo: 'desenho', c, seek(tt) {
      for (const o of objs) {
        if (o.fill) { o.p.setAttribute('opacity', clamp((tt - o.t0) / (o.t1 - o.t0))); continue; }
        const q = clamp((tt - o.t0) / (o.t1 - o.t0));
        o.p.setAttribute('stroke-dashoffset', (o.len + 2) * (1 - q));
        if (o.fillCor) o.p.setAttribute('fill-opacity', clamp((tt - o.t1) / .15));
      }
    } });
    return { fim: t - gap, x, y };
  }

  // ---------- ARTE (doodle gerado por IA e vetorizado com vetorizar.py) ----------
  // nome = chave em window.HD_ARTES (arquivo artes/artes.js). op: x, y (centro), w (largura na tela), at, dur
  function arte(c, nome, op = {}) {
    const A = (window.HD_ARTES || {})[nome];
    if (!A) throw new Error('arte não vetorizada: ' + nome + ' (rode vetorizar.py)');
    const w = op.w || 420, s = w / A.w, h = A.h * s;
    const x = (op.x ?? cfg.cx) - w / 2, y = (op.y ?? 900) - h / 2;
    const defs = c.ink.querySelector('defs');
    const id = 'arte' + itens.length;
    const mask = el('mask', { id, maskUnits: 'userSpaceOnUse', x: -50, y: -50, width: A.w + 100, height: A.h + 100 }, defs);
    const g = el('g', { transform: `translate(${x} ${y}) scale(${s})` }, c.ink);
    const larg = A.largura * 2.6 + 4;
    const ps = A.tracos.map(tr => {
      const d = 'M' + tr.pts.map(p => p.join(' ')).join(' L');
      const p = el('path', { d, fill: 'none', stroke: '#fff', 'stroke-width': larg, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, mask);
      const len = Math.max(1, p.getTotalLength());
      p.setAttribute('stroke-dasharray', `${len + 1} ${len + 1}`); p.setAttribute('stroke-dashoffset', len + 1);
      return { p, len };
    });
    const mg = el('g', { mask: `url(#${id})` }, g);
    for (const camada of ['ink', 'acc']) if (A[camada]) {
      el('image', { href: (cfg.artes || 'artes/') + A[camada], x: 0, y: 0, width: A.w, height: A.h, filter: `url(#tint-${camada})` }, mg);
    }
    const total = ps.reduce((a, o) => a + o.len, 0) * s;
    const gap = .045;
    const dur = op.dur ?? clamp(total / (op.vel || 1500), .6, 4);
    const tDraw = Math.max(.2, dur - gap * (ps.length - 1) * .5);
    let t = op.at ?? c.t0 + .2;
    for (const o of ps) {
      o.t0 = t; o.t1 = t + tDraw * (o.len * s / total); t = o.t1 + (o.len * s < 25 ? gap * .3 : gap);
      const p = o.p, len = o.len;
      seg(c, o.t0, o.t1, q => { const pt = p.getPointAtLength(q * len); return [x + pt.x * s, y + pt.y * s]; });
    }
    itens.push({ tipo: 'arte', c, seek(tt) {
      for (const o of ps) o.p.setAttribute('stroke-dashoffset', (o.len + 1) * (1 - clamp((tt - o.t0) / (o.t1 - o.t0))));
    } });
    return { fim: t, x: x + w / 2, y: y + h / 2, w, h };
  }

  // ---------- FOTO colada com fita (print, produto, prova) ----------
  // op: x, y (centro), w, rot, at, borda (px de papel branco), fita (true)
  function foto(c, src, op = {}) {
    const w = op.w || 360, x = op.x ?? cfg.cx, y = op.y ?? 900, rot = op.rot ?? (rnd() * 6 - 3);
    const at = op.at ?? c.t0 + .2;
    const g = el('g', {}, c.fotos);
    const inner = el('g', {}, g);
    const img = el('image', { href: src, x: 0, y: 0, width: w, preserveAspectRatio: 'xMidYMid meet' }, inner);
    const h = op.h || w * (op.prop || 1.25);
    img.setAttribute('height', h);
    const b = op.borda ?? 12;
    inner.insertBefore(el('rect', { x: -b, y: -b, width: w + 2 * b, height: h + 2 * b, rx: 4, fill: '#FBFAF6', class: 'foto-papel' }), img);
    if (op.fita !== false) for (const [fx, fr] of [[w * .5, -4 + rnd() * 8]]) {
      el('rect', { x: fx - 70, y: -b - 22, width: 140, height: 40, rx: 3, fill: 'rgba(236,226,196,.82)',
        transform: `rotate(${fr} ${fx} ${-b})`, class: 'fita' }, inner);
    }
    HD.cues.push({ t: at, type: 'pop' });
    itens.push({ tipo: 'foto', c, seek(tt) {
      const p = clamp((tt - at) / .38);
      const sc = lerp(1.18, 1, E.outBack(p)), op_ = clamp(p * 2.5);
      g.setAttribute('opacity', op_);
      g.setAttribute('transform', `translate(${x} ${y}) rotate(${rot + (1 - E.out(p)) * 6}) scale(${sc}) translate(${-w / 2} ${-h / 2})`);
    } });
    return { x, y, w, h, fim: at + .38 };
  }

  // ---------- LEGENDA em pílula (2–3 palavras, palavra-chave colorida) ----------
  const legs = [];
  // auto: a partir de HD.words. destaques = lista de palavras (sem acento tanto faz) que ficam na cor de destaque
  HD.legendas = (o = {}) => {
    const dest = new Set((o.destaques || []).map(norm));
    const max = o.max || 3, maxC = o.maxChars || 17;
    let bloco = [];
    const fecha = () => { if (bloco.length) legs.push({ t0: bloco[0].s - .04, ws: bloco }); bloco = []; };
    for (const w of HD.words) {
      const len = bloco.map(b => b.w).join(' ').length + w.w.length + 1;
      if (bloco.length >= max || (bloco.length && len > maxC) ||
          (bloco.length && w.s - bloco[bloco.length - 1].e > .45)) fecha();
      bloco.push(w);
      if (/[.?!,:;…]$/.test(w.w)) fecha();
    }
    fecha();
    legs.forEach((l, i) => {
      const prox = legs[i + 1];
      l.t1 = prox ? Math.min(prox.t0, l.ws[l.ws.length - 1].e + .9) : l.ws[l.ws.length - 1].e + .6;
      l.html = l.ws.map(w => {
        const txt = w.w.toUpperCase();
        return dest.has(norm(w.w)) ? `<b>${txt}</b>` : txt;
      }).join(' ');
    });
  };
  HD.legenda = (texto, t0, t1) => legs.push({ t0, t1, html: texto.toUpperCase().replace(/\*(.+?)\*/g, '<b>$1</b>') });
  let legAtual = -1;
  function seekLegenda(t) {
    const i = legs.findIndex(l => t >= l.t0 && t < l.t1);
    if (i !== legAtual) { legEl.innerHTML = i >= 0 ? `<span>${legs[i].html}</span>` : ''; legAtual = i; }
    if (i >= 0) {
      const p = clamp((t - legs[i].t0) / .14), q = clamp((legs[i].t1 - t) / .1);
      const s = legEl.firstChild;
      s.style.opacity = Math.min(p, q);
      s.style.transform = `scale(${lerp(.9, 1, E.outBack(p))})`;
    }
  }

  // ---------- CANETA / MÃO ----------
  let segsOrd = [];
  function penAt(t) {
    // devolve [x, y, desce(0..1), cenaIdx] em coordenadas do mundo
    let lo = 0, hi = segsOrd.length - 1, k = -1;
    while (lo <= hi) { const m = (lo + hi) >> 1; if (segsOrd[m].t0 <= t) { k = m; lo = m + 1; } else hi = m - 1; }
    const S = segsOrd[k], N = segsOrd[k + 1];
    const W = (s, p) => { const [x, y] = s.f(p); return [x + s.c.ox, y]; };
    if (S && t <= S.t1) { const [x, y] = W(S, (t - S.t0) / (S.t1 - S.t0)); return [x, y, 1, S.c.i]; }
    const fora = (P, c) => [P[0] + 760, P[1] + 1050];
    if (!S) {                                         // antes do 1º traço: entra pela direita/baixo
      if (!N) return [0, 0, 0, 0];
      const B = W(N, 0), A = fora(B), p = E.inOut(clamp((t - (N.t0 - .5)) / .5));
      return [lerp(A[0], B[0], p), lerp(A[1], B[1], p), 0, N.c.i];
    }
    const A = W(S, 1);
    if (!N) {                                         // depois do último: sai
      const B = fora(A), p = E.inOut(clamp((t - S.t1 - .5) / .6));
      return [lerp(A[0], B[0], p), lerp(A[1], B[1], p), 0, S.c.i];
    }
    const B = W(N, 0), gapT = N.t0 - S.t1;
    const tr = Math.min(gapT, gapT > 1.2 ? .42 : .3 + .25 * clamp(Math.hypot(B[0] - A[0], B[1] - A[1]) / 900));
    if (gapT > 1.2) {                                 // pausa longa: recolhe um pouco e volta
      const R = [A[0] + 150, A[1] + 230];
      if (t < S.t1 + .35) { const p = E.inOut((t - S.t1) / .35); return [lerp(A[0], R[0], p), lerp(A[1], R[1], p), 0, S.c.i]; }
      if (t < N.t0 - tr) { const b = Math.sin((t - S.t1) * 2.1) * 6; return [R[0] + b * .6, R[1] + b, 0, S.c.i]; }
      const p = E.inOut((t - (N.t0 - tr)) / tr); return [lerp(R[0], B[0], p), lerp(R[1], B[1], p), 0, N.c.i];
    }
    if (t < N.t0 - tr) return [A[0], A[1] - 4 * clamp((t - S.t1) / .1), 0, S.c.i];
    const p = E.inOut((t - (N.t0 - tr)) / tr);
    const arco = Math.sin(p * Math.PI) * Math.min(40, Math.hypot(B[0] - A[0], B[1] - A[1]) * .08);
    return [lerp(A[0], B[0], p), lerp(A[1], B[1], p) - arco - 4 * (1 - p), 0, (p < .5 ? S : N).c.i];
  }

  function seekMao(t) {
    const [x, y, down] = penAt(t);
    const m = MAOS[T.mao], s = cfg.maoEscala;
    const cena = cenaEm(t);
    const lx = x - (cena ? cena.ox : 0);
    const lift = 1 - down;
    // giro leve: mais deitada à esquerda do quadro, tremidinha enquanto escreve
    const rot = -6 + 9 * clamp(lx / QW) + Math.sin(t * 23) * .5 * down + Math.sin(t * 1.3) * 1.2;
    const sc = 1 + .03 * lift;
    maoEl.style.left = (x - m.ponta[0] * s) + 'px';
    maoEl.style.top = (y - m.ponta[1] * s) + 'px';
    maoEl.style.transform = `rotate(${rot}deg) scale(${sc})`;
    const [r, g, b, a] = T.sombra;
    const off = 14 + 16 * lift;
    maoEl.style.filter = `drop-shadow(${-off * .55}px ${off}px ${12 + 10 * lift}px rgba(${r},${g},${b},${a}))`;
  }

  // ---------- CÂMERA ----------
  const WHIP = .42;
  const cenaEm = t => { let c = cenas[0]; for (const k of cenas) if (t >= k.t0 - WHIP * .45) c = k; return c; };
  function boardX(t) {
    let x = 0;
    for (let i = 1; i < cenas.length; i++) x += BOARD * E.whip(clamp((t - (cenas[i].t0 - WHIP * .45)) / WHIP));
    return x;
  }
  function follow(t) {
    const [x, y] = penAt(t);
    const c = cenaEm(t);
    const lx = x - (c ? c.ox : 0);
    return [clamp(lx - QW / 2, -400, 400) * .07, clamp(y - 900, -700, 700) * .05];
  }
  function camAt(t) {
    // média exponencial do "alvo" no passado = câmera com mola, mas determinística
    let fx = 0, fy = 0, ws = 0;
    for (let k = 0; k < 14; k++) {
      const dt = k * .045, wgt = Math.exp(-dt / .22);
      const [a, b] = follow(Math.max(0, t - dt));
      fx += a * wgt; fy += b * wgt; ws += wgt;
    }
    const c = cenaEm(t);
    const pz = c ? clamp((t - c.t0) / Math.max(.5, c.t1 - c.t0)) : 0;
    const z = 1 + ((c ? c.zoom : 1.03) - 1) * E.out(pz) + .025 * (1 - E.out(clamp((t - (c ? c.t0 : 0)) / .6)));
    return { x: QW / 2 + boardX(t) + fx / ws, y: QH / 2 + fy / ws, z };
  }

  function seekCamera(t) {
    const cam = camAt(t);
    world.style.transform = `translate(${QW / 2}px, ${QH / 2}px) scale(${cam.z}) translate(${-cam.x}px, ${-cam.y}px)`;
    const v = Math.abs(boardX(t + 1 / 60) - boardX(t - 1 / 60)) * 30;   // px/s
    const b = Math.min(60, v / 260);
    if (b > .6) { blurNode.setAttribute('stdDeviation', `${b} 0`); world.style.filter = 'url(#mblur)'; }
    else world.style.filter = 'none';
    // só os quadros perto da câmera ficam ligados (desempenho)
    const ci = (cam.x - QW / 2) / BOARD;
    for (const c of cenas) c.wrap.style.display = Math.abs(c.i - ci) < 1.3 ? 'block' : 'none';
  }

  // ---------- ciclo ----------
  HD.seek = t => {
    for (const it of itens) it.seek(t);
    seekCamera(t);
    seekMao(t);
    seekLegenda(t);
  };

  HD.roteiro = fn => { HD._fn = fn; };

  async function iniciar() {
    await document.fonts.load('80px PM');
    await document.fonts.load('800 40px Inter');
    await document.fonts.ready;
    montar();
    HD._fn(HD);
    segsOrd = segs.slice().sort((a, b) => a.t0 - b.t0);
    // som de risco: junta segmentos colados
    let cur = null;
    for (const s of segsOrd) {
      if (cur && s.t0 - cur.t1 < .09) cur.t1 = Math.max(cur.t1, s.t1);
      else { if (cur) HD.cues.push({ t: cur.t0, type: 'risco', dur: cur.t1 - cur.t0 }); cur = { t0: s.t0, t1: s.t1 }; }
    }
    if (cur) HD.cues.push({ t: cur.t0, type: 'risco', dur: cur.t1 - cur.t0 });
    for (let i = 1; i < cenas.length; i++) HD.cues.push({ t: cenas[i].t0 - WHIP * .45 + WHIP * .5, type: 'whoosh' });
    HD.cues.push({ ferramenta: T.mao });
    HD.duration = cfg.duracao || Math.max(...cenas.map(c => c.t1));
    const bgW = (cenas.length + 1) * BOARD + 2000;
    bgEl.style.width = bgW + 'px';
    const q = new URLSearchParams(location.search);
    if (q.has('render')) { HD.seek(0); }
    else if (q.has('t')) HD.seek(+q.get('t'));
    else {
      const t0 = performance.now();
      const loop = () => { HD.seek(((performance.now() - t0) / 1000) % HD.duration); requestAnimationFrame(loop); };
      loop();
    }
  }
  window.HD_READY = new Promise(r => window.addEventListener('load', () => iniciar().then(r)));
})();
