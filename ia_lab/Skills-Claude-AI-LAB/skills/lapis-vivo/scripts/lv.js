// Lápis Vivo — motor. Um lápis escreve e desenha a aula inteira numa página comprida de caderno;
// a página rola pra cima conforme o conteúdo cresce. Tudo é função do tempo: LV.seek(t) deixa a tela
// exatamente no instante t (render quadro a quadro).
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const LV = window.LV = {};
  const QW = 1080, QH = 1920;
  const PAUTA = 92;            // distância entre as linhas do caderno (toda linha de texto senta numa pauta)
  const Y0 = 340;              // linha de base da 1ª linha (abaixo da safe zone do topo)
  const DESC = 14;             // a pauta fica 14 px abaixo da linha de base

  const TEMAS = {
    grafite: {
      papel: ['#2B2F39', '#22252D'], pauta: 'rgba(168,190,235,.15)', margem: 'rgba(240,120,110,.42)', grade: false,
      furo: '#0d0e12', arame: ['#8D94A3', '#E6E9F0'], grao: .55, luz: 'rgba(255,255,255,.075)', vinheta: 'rgba(0,0,0,.55)',
      ink: '#F3F2EC', cinza: '#A7ADB9', amarelo: '#F4C456', verde: '#73D694', vermelho: '#F27A70', azul: '#82B6FF',
      lapisInk: '#C9CCD3', linha: 'rgba(240,240,236,.88)', sombra: 'rgba(0,0,0,.42)', escurece: 'rgba(14,15,19,.80)', brilho: .18 },
    creme: {
      papel: ['#F6F0DF', '#EDE5CE'], pauta: 'rgba(52,104,190,.30)', margem: 'rgba(216,68,58,.55)', grade: false,
      furo: '#b9ae93', arame: ['#70757F', '#D8DBE2'], grao: .5, luz: 'rgba(255,255,255,.35)', vinheta: 'rgba(90,70,40,.22)',
      ink: '#232C3D', cinza: '#7C8493', amarelo: '#D8780A', verde: '#1E9A55', vermelho: '#D6423A', azul: '#2C6BD4',
      lapisInk: '#3D4A63', linha: 'rgba(35,44,61,.85)', sombra: 'rgba(60,45,25,.30)', escurece: 'rgba(246,240,223,.86)', brilho: 0 },
    quadriculado: {
      papel: ['#17264A', '#111C38'], pauta: 'rgba(140,180,255,.16)', margem: 'rgba(255,125,115,.40)', grade: true,
      furo: '#070c1a', arame: ['#8A93A8', '#E6EAF3'], grao: .5, luz: 'rgba(150,190,255,.10)', vinheta: 'rgba(0,3,14,.6)',
      ink: '#F0F4FC', cinza: '#9FB0CF', amarelo: '#FFD166', verde: '#5EE0A0', vermelho: '#FF7F76', azul: '#7CC4FF',
      lapisInk: '#C7CEDD', linha: 'rgba(240,244,252,.88)', sombra: 'rgba(0,0,0,.45)', escurece: 'rgba(8,13,28,.82)', brilho: .2 },
  };

  const cfg = LV.cfg = { tema: 'grafite', assets: 'assets/', cx: 520, x0: 150, foco: 1400, lapisEscala: 1, legY: 1395, espiral: true };
  LV.config = o => { Object.assign(cfg, o); if (o && o.foco) cfg._focoManual = true; };
  LV.cues = [];
  LV.words = window.WORDS || [];
  LV.PAUTA = PAUTA;

  // ---------- util ----------
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, p) => a + (b - a) * p;
  const E = {
    inOut: p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2,
    out: p => 1 - Math.pow(1 - p, 3),
    outBack: p => { const c = 1.9; return 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); },
  };
  LV.E = E;
  const el = (tag, attrs = {}, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  let seed = 7;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  LV.rnd = rnd;
  const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9%]/g, '');
  const hex = h => { h = h.replace('#', ''); if (h.length === 3) h = [...h].map(c => c + c).join(''); return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16)); };
  const rgb = a => `rgb(${a.map(v => Math.round(clamp(v, 0, 255))).join(',')})`;
  const mix = (a, b, p) => a.map((v, i) => lerp(v, b[i], p));

  // ---------- tempos pelas palavras da locução (words.js) ----------
  const achar = (txt, n = 1) => {
    const alvo = txt.split(/\s+/).map(norm);
    let k = 0;
    for (let i = 0; i < LV.words.length; i++) {
      if (alvo.every((a, j) => LV.words[i + j] && norm(LV.words[i + j].w) === a) && ++k === n)
        return [LV.words[i], LV.words[i + alvo.length - 1]];
    }
    throw new Error(`palavra não encontrada na locução: "${txt}" (#${n})`);
  };
  LV.w = (txt, n) => achar(txt, n)[0].s;
  LV.we = (txt, n) => achar(txt, n)[1].e;

  // ---------- estrutura ----------
  const itens = [], segs = [], ancoras = [], ctas = [];
  let T, world, world2, pagina, inkSvg, ctaSvg, fotosSvg, lapisEl, legEl, dimEl;

  const corDe = c => {
    if (!c || c === 'ink') return T.ink;
    if (c === 'acc') return T.amarelo;
    return T[c] && typeof T[c] === 'string' ? T[c] : c;
  };
  const corLapis = c => (!c || c === 'ink' || corDe(c) === T.ink) ? T.lapisInk : corDe(c);

  function ruido(n, escalas) {     // textura de papel emendável: grão fino + manchas largas
    const cv = document.createElement('canvas'); cv.width = cv.height = n;
    const ctx = cv.getContext('2d');
    const camada = (tam, blur) => {
      const c2 = document.createElement('canvas'); c2.width = c2.height = tam;
      const x2 = c2.getContext('2d'), d = x2.createImageData(tam, tam);
      for (let i = 0; i < d.data.length; i += 4) { const v = rnd() * 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; }
      x2.putImageData(d, 0, 0);
      const c3 = document.createElement('canvas'); c3.width = c3.height = n;
      const x3 = c3.getContext('2d'); x3.filter = `blur(${blur}px)`;
      for (const dx of [-n, 0, n]) for (const dy of [-n, 0, n]) x3.drawImage(c2, dx, dy, n, n);
      return x3.getImageData(0, 0, n, n).data;
    };
    const cs = escalas.map(([tam, blur]) => camada(tam, blur));
    const out = ctx.createImageData(n, n);
    for (let i = 0; i < out.data.length; i += 4) {
      let g = 0; escalas.forEach(([, , peso], k) => { g += cs[k][i] * peso; });
      out.data[i] = out.data[i + 1] = out.data[i + 2] = g; out.data[i + 3] = 255;
    }
    ctx.putImageData(out, 0, 0);
    return cv.toDataURL();
  }

  function espiralSvg() {          // um gomo do wire-o (92 px): furo retangular + 2 arames com brilho e sombra
    const [a, b] = T.arame;
    const arame = (y) => `<path d="M-14 ${y + 9} C 14 ${y + 15}, 44 ${y + 12}, 62 ${y + 3}" fill="none" stroke="rgba(0,0,0,.34)" stroke-width="10" stroke-linecap="round"/>
<path d="M-14 ${y} C 14 ${y + 7}, 44 ${y + 5}, 60 ${y - 3}" fill="none" stroke="url(#g)" stroke-width="7.5" stroke-linecap="butt"/>
<path d="M-14 ${y - 2.4} C 14 ${y + 4.6}, 42 ${y + 2.6}, 56 ${y - 4.4}" fill="none" stroke="rgba(255,255,255,.6)" stroke-width="1.8" stroke-linecap="round"/>`;
    const s = `<svg xmlns="http://www.w3.org/2000/svg" width="110" height="${PAUTA}" viewBox="0 0 110 ${PAUTA}">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${b}"/><stop offset=".5" stop-color="${a}"/><stop offset="1" stop-color="#3b3f49"/></linearGradient></defs>
<rect x="50" y="24" width="27" height="44" rx="7" fill="${T.furo}"/>
<rect x="50" y="24" width="27" height="44" rx="7" fill="none" stroke="rgba(0,0,0,.35)" stroke-width="3"/>
<path d="M53 66 Q63.5 70 74 66" fill="none" stroke="rgba(255,255,255,.16)" stroke-width="1.6" stroke-linecap="round"/>
${arame(38)}${arame(56)}
</svg>`;
    return 'url("data:image/svg+xml,' + encodeURIComponent(s) + '")';
  }

  function montar() {
    T = Object.assign({}, TEMAS[cfg.tema] || TEMAS.grafite, cfg.cores || {});
    LV.T = T;
    const R = document.documentElement.style;
    for (const k of ['ink', 'cinza', 'amarelo', 'verde', 'vermelho', 'azul']) R.setProperty('--' + k, T[k]);
    R.setProperty('--acc', T.amarelo);
    document.body.className = 'tema-' + cfg.tema;
    world = document.getElementById('world');
    world2 = document.getElementById('world2');
    pagina = document.getElementById('pagina');
    dimEl = document.getElementById('dim');
    dimEl.style.background = T.escurece;
    legEl = document.getElementById('legenda');
    // --- caderno: papel + manchas + grão + pautas + margem + espiral ---
    const ry = Y0 + DESC - 1;     // posição da 1ª pauta
    const pautas = T.grade
      ? `repeating-linear-gradient(0deg, ${T.pauta} 0 2px, transparent 2px ${PAUTA / 2}px), repeating-linear-gradient(90deg, ${T.pauta} 0 2px, transparent 2px ${PAUTA / 2}px)`
      : `repeating-linear-gradient(0deg, ${T.pauta} 0 2.5px, transparent 2.5px ${PAUTA}px)`;
    pagina.style.background = `linear-gradient(90deg, rgba(0,0,0,.22) 0, rgba(0,0,0,.06) 70px, transparent 130px, transparent 86%, rgba(0,0,0,.10) 100%), linear-gradient(90deg, ${T.papel[0]}, ${T.papel[1]})`;
    const lin = document.getElementById('pautas');
    lin.style.background = pautas;
    lin.style.backgroundPosition = T.grade ? `${cfg.x0 - 30}px ${ry % (PAUTA / 2)}px` : `0 ${ry % PAUTA}px`;
    const mg = document.getElementById('margem');
    mg.style.background = `linear-gradient(90deg, transparent 0, transparent ${cfg.x0 - 36}px, ${T.margem} ${cfg.x0 - 36}px, ${T.margem} ${cfg.x0 - 33}px, transparent ${cfg.x0 - 33}px, transparent ${cfg.x0 - 27}px, ${T.margem} ${cfg.x0 - 27}px, ${T.margem} ${cfg.x0 - 25.5}px, transparent ${cfg.x0 - 25.5}px)`;
    const gr = document.getElementById('grao');
    gr.style.backgroundImage = `url(${(window.LV_IMG || {}).papel || ruido(512, [[512, .35, .55], [128, 1.5, .25], [16, 18, .2]])})`;
    gr.style.opacity = T.grao;
    const mc = document.getElementById('manchas');
    mc.style.backgroundImage = `url(${ruido(256, [[8, 14, 1]])})`;
    const esp = document.getElementById('espiral');
    if (cfg.espiral) { esp.style.backgroundImage = espiralSvg(); esp.style.backgroundPosition = `0 ${(ry + PAUTA / 2 - 46 + PAUTA * 10) % PAUTA}px`; }
    else esp.style.display = 'none';
    document.getElementById('luz').style.background =
      `radial-gradient(ellipse 85% 55% at 28% 16%, ${T.luz} 0, transparent 70%), radial-gradient(ellipse 78% 64% at 50% 46%, transparent 52%, ${T.vinheta} 100%)`;
    fotosSvg = el('svg', { class: 'camada', width: QW, height: 10, viewBox: `0 0 ${QW} 10` }, pagina);
    inkSvg = el('svg', { class: 'camada ink', width: QW, height: 10, viewBox: `0 0 ${QW} 10` }, pagina);
    el('defs', {}, inkSvg);
    ctaSvg = el('svg', { class: 'camada ink', width: QW, height: 10, viewBox: `0 0 ${QW} 10` }, world2);
    el('defs', {}, ctaSvg);
    if (T.brilho) R.setProperty('--glow', `drop-shadow(0 0 2.2px rgba(255,255,255,${T.brilho}))`);
    criarLapis();
  }

  // ---------- LÁPIS (foto recortada; o corpo laqueado é tingido pela máscara com a cor da tinta) ----------
  let lapisCorAtual = '';
  const LP = { tinta: null, sombra: null, g: null };
  const LW = 84, LH = 760, PONTA = [42, 2];          // tamanho do PNG e onde fica a ponta do grafite
  function criarLapis() {
    const I = window.LV_IMG || {};
    const svg = el('svg', { id: 'lapis', class: 'camada', width: QW, height: 10, viewBox: `0 0 ${QW} 10` }, world2);
    const defs = el('defs', {}, svg);
    const f = el('filter', { id: 'lapis-sombra', x: '-80%', y: '-10%', width: '260%', height: '120%' }, defs);
    el('feFlood', { 'flood-color': T.sombra }, f);
    el('feComposite', { in2: 'SourceAlpha', operator: 'in' }, f);
    el('feGaussianBlur', { stdDeviation: 7 }, f);
    const mk = el('mask', { id: 'lapis-mask', maskUnits: 'userSpaceOnUse', x: 0, y: 0, width: LW, height: LH }, defs);
    el('image', { href: I.mask, x: 0, y: 0, width: LW, height: LH }, mk);
    LP.sombra = el('g', {}, svg);
    el('image', { href: I.lapis, x: -PONTA[0], y: -PONTA[1], width: LW, height: LH, filter: 'url(#lapis-sombra)' }, LP.sombra);
    const g = LP.g = el('g', { style: 'isolation:isolate' }, svg);
    const inner = el('g', { transform: `translate(${-PONTA[0]} ${-PONTA[1]})` }, g);
    el('image', { href: I.lapis, x: 0, y: 0, width: LW, height: LH }, inner);
    LP.tinta = el('rect', { x: 0, y: 0, width: LW, height: LH, mask: 'url(#lapis-mask)', style: 'mix-blend-mode:multiply' }, inner);
    lapisEl = svg;
  }
  function pintarLapis(c) {
    const k = rgb(c);
    if (k === lapisCorAtual) return;
    lapisCorAtual = k;
    LP.tinta.setAttribute('fill', rgb(mix(c, [255, 255, 255], .12)));
  }

  // segmento de lápis: entre t0 e t1 a ponta percorre f(p) (coordenadas da página)
  const seg = (t0, t1, f, cor) => { const s = { t0, t1, f, cor: hex(toHex(corLapis(cor))) }; segs.push(s); return s; };
  const toHex = c => {
    if (c[0] === '#') return c;
    const d = document.createElement('span'); d.style.color = c; document.body.appendChild(d);
    const m = getComputedStyle(d).color.match(/[\d.]+/g).slice(0, 3).map(Number); d.remove();
    return '#' + m.map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  };
  const ancora = (t, y) => ancoras.push({ t, y });

  // ---------- página (API do roteiro) ----------
  const P = LV.p = { y: Y0, t: .15, layer: null };
  const snap = y => Y0 + Math.ceil((y - Y0 - 1) / PAUTA) * PAUTA;
  P.pular = (n = 1) => { P.y += n * PAUTA; return P; };
  P.snap = () => { P.y = snap(P.y); return P; };
  const camada = () => P.layer || inkSvg;

  // TEXTO manuscrito. *trecho* = cor de destaque (op.destaque, padrão amarelo).
  // op: x, y (linha de base), size, cor, at | ate (termina em), dur | vel (s/letra), ancora ('start'|'middle'|'end'), negrito, avanca
  function escrever(str, op = {}) {
    const size = op.size || 52;
    const x = op.x ?? cfg.x0, y = op.y ?? P.y;
    const cor = corDe(op.cor), corD = corDe(op.destaque || 'amarelo');
    const svg = op.layer || camada();
    const partes = str.split('*');
    const plano = partes.join('');
    const nChars = plano.replace(/\s/g, '').length, nEsp = Math.max(0, plano.trim().split(/\s+/).length - 1);
    const unidades = Math.max(1, nChars + nEsp * .9);
    const vel = op.dur ? op.dur / unidades : (op.vel || .05);
    let t = op.at ?? (op.ate != null ? op.ate - vel * unidades : P.t);
    const t0 = t;
    const id = 'clip' + itens.length + '_' + Math.round(rnd() * 1e6);
    const cp = el('clipPath', { id }, svg.querySelector('defs'));
    const rect = el('rect', { x: -9999, y: y - size * 1.25, width: 0, height: size * 1.9 }, cp);
    const tx = el('text', { x, y, 'text-anchor': op.ancora || 'start', 'font-size': size, fill: cor, 'clip-path': `url(#${id})`,
      class: 'hand' + (op.negrito ? ' negrito' : '') }, svg);
    if (op.negrito) { tx.setAttribute('stroke-width', size * .034); }
    const coresChar = [];
    partes.forEach((s, i) => {
      if (!s) return;
      const c = i % 2 ? corD : cor;
      const ts = el('tspan', { fill: c }, tx);
      if (op.negrito) ts.setAttribute('stroke', c);
      ts.textContent = s;
      for (let k = 0; k < s.length; k++) coresChar.push(i % 2 ? (op.destaque || 'amarelo') : op.cor);
    });
    const glifos = [];
    for (let k = 0; k < plano.length; k++) {
      if (plano[k] === ' ') continue;
      const b = tx.getExtentOfChar(k);
      glifos.push({ x0: b.x, x1: b.x + b.width, top: y - size * .62, bot: y + size * .02, esp: k > 0 && plano[k - 1] === ' ', cor: coresChar[k] });
    }
    if (!glifos.length) return { x0: x, x1: x, base: y, w: 0, h: size, cx: x, cy: y, t0, fim: t };
    const xa = Math.min(...glifos.map(g => g.x0)), xb = Math.max(...glifos.map(g => g.x1));
    rect.setAttribute('x', xa - size * .35);
    glifos.forEach((g, gi) => {
      if (gi && g.esp) t += vel * .9;
      g.t0 = t; g.t1 = t + vel * (0.85 + rnd() * .3); t = g.t1;
      const zz = 3 + Math.round(rnd());
      seg(g.t0, g.t1, p => {
        const q = p * zz, k = Math.floor(Math.min(q, zz - 1e-6)), f = q - k;
        const xA = lerp(g.x0, g.x1, k / zz), xB = lerp(g.x0, g.x1, (k + 1) / zz);
        const yA = k % 2 ? g.top : g.bot, yB = k % 2 ? g.bot : g.top;
        return [lerp(xA, xB, f), lerp(yA, yB, f)];
      }, g.cor);
    });
    // reescala pra terminar exatamente em dur (as letras têm durações irregulares)
    const alvo = op.dur ?? vel * unidades, real = t - t0, k = alvo / real;
    for (const g of glifos) { g.t0 = t0 + (g.t0 - t0) * k; g.t1 = t0 + (g.t1 - t0) * k; }
    segs.slice(-glifos.length).forEach((s, i) => { s.t0 = glifos[i].t0; s.t1 = glifos[i].t1; });
    const fim = t0 + alvo;
    itens.push({ seek(tt) {
      let rx = xa - size * .35;
      for (const g of glifos) {
        if (tt >= g.t1) rx = g.x1 + size * .2;
        else if (tt > g.t0) { rx = lerp(g.x0, g.x1, (tt - g.t0) / (g.t1 - g.t0)) + size * .06; break; }
        else break;
      }
      rect.setAttribute('width', Math.max(0, rx - (xa - size * .35)));
    } });
    if (!op.layer && op.camera !== false) ancora(t0, y);
    if (op.y == null && op.avanca !== false) P.y = y + (op.pula ?? 1) * PAUTA;
    P.t = fim + (op.pausa ?? .22);
    return { x0: xa, x1: xb, base: y, w: xb - xa, h: size, cx: (xa + xb) / 2, cy: y - size * .3, x: (xa + xb) / 2, y: y - size * .3, t0, fim, el: tx };
  }
  P.linha = (s, op = {}) => escrever(s, op.centro ? Object.assign({ x: cfg.cx, ancora: 'middle' }, op) : op);
  P.titulo = (s, op = {}) => escrever(s, Object.assign({ x: cfg.cx, ancora: 'middle', size: 80, negrito: true, vel: .055 }, op));
  P.sub = (s, op = {}) => escrever(s, Object.assign({ x: cfg.cx, ancora: 'middle', size: 46, cor: 'cinza', vel: .045 }, op));
  P.secao = (s, op = {}) => { if (op.y == null && op.espaco !== false) P.y += PAUTA; return escrever(s, Object.assign({ size: 66, negrito: true, cor: 'verde' }, op)); };
  P.nota = (s, op = {}) => escrever(s, Object.assign({ size: 42, cor: 'cinza', vel: .042 }, op));
  // lista: um item por linha. op.ats = [t de cada item] (ou sequencial); devolve as caixas
  P.lista = (arr, op = {}) => arr.map((s, i) => escrever(s, Object.assign({}, op, { at: op.ats ? op.ats[i] : (i ? undefined : op.at), ats: undefined })));

  // TRAÇO: path desenhado pelo lápis. op: cor, w, at, dur | vel (px/s), layer, fill
  function tracar(d, op = {}) {
    const svg = op.layer || camada();
    const cor = corDe(op.cor);
    const p = el('path', { d, fill: 'none', stroke: op.linha ? T.linha : cor, 'stroke-width': op.w || 5, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, op.grupo || svg);
    const len = p.getTotalLength();
    p.setAttribute('stroke-dasharray', `${len + 2} ${len + 2}`); p.setAttribute('stroke-dashoffset', len + 2);
    const t0 = op.at ?? P.t, dur = op.dur ?? clamp(len / (op.vel || 1100), .18, 2.5);
    const M = op.matriz;
    seg(t0, t0 + dur, q => { const pt = p.getPointAtLength(q * len); return M ? M(pt.x, pt.y) : [pt.x, pt.y]; }, op.corLapis || op.cor);
    itens.push({ seek(tt) { p.setAttribute('stroke-dashoffset', (len + 2) * (1 - clamp((tt - t0) / dur))); } });
    if (op.seguir !== false) P.t = t0 + dur + .08;
    return { fim: t0 + dur, el: p, len };
  }
  P.tracar = tracar;

  // SETA de (x1,y1) até (x2,y2). op.curva = barriga em px (+ pra um lado, − pro outro)
  P.seta = (x1, y1, x2, y2, op = {}) => {
    const mx = (x1 + x2) / 2, my = (y1 + y2) / 2, dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy) || 1;
    const c = op.curva || 0, qx = mx - dy / L * c, qy = my + dx / L * c;
    const a = tracar(`M${x1} ${y1} Q${qx} ${qy} ${x2} ${y2}`, op);
    const ang = Math.atan2(y2 - qy, x2 - qx), h = op.ponta || 24;
    const pt = k => `${x2 - Math.cos(ang + k) * h} ${y2 - Math.sin(ang + k) * h}`;
    const b = tracar(`M${pt(.5)} L${x2} ${y2} L${pt(-.5)}`, Object.assign({}, op, { at: a.fim + .04, dur: .14 }));
    if (!op.layer) ancora(op.at ?? a.fim, Math.max(y1, y2));
    return { fim: b.fim };
  };

  // CHAVE: seta curva lateral ligando duas linhas (ex.: "× 6" entre duas linhas de uma tabela)
  P.chave = (x, yA, yB, op = {}) => {
    const s = op.lado === 'dir' ? 1 : -1, d = (op.barriga || 34) * s;
    const a = tracar(`M${x} ${yA} C${x + d} ${yA + (yB - yA) * .2} ${x + d} ${yB - (yB - yA) * .2} ${x} ${yB}`, Object.assign({ cor: 'verde', w: 5 }, op));
    const h = 20, ang = Math.atan2((yB - yA) * .2, -d);
    const pt = k => `${x - Math.cos(ang + k) * h} ${yB - Math.sin(ang + k) * h}`;
    const b = tracar(`M${pt(.55)} L${x} ${yB} L${pt(-.55)}`, Object.assign({ cor: 'verde', w: 5 }, op, { at: a.fim + .03, dur: .12 }));
    let fim = b.fim;
    if (op.rotulo) {
      const r = escrever(op.rotulo, { x: x + d * .8 + s * 16, y: (yA + yB) / 2 + 16, size: op.size || 46, cor: op.cor || 'verde',
        ancora: s < 0 ? 'end' : 'start', at: b.fim + .08, camera: false });
      fim = r.fim;
    }
    return { fim };
  };

  // GRADE de quadradinhos que vão sendo pintados: "38 de 45"
  // op: total, cheios, cols, lado (46), x, at, dur (pintura), cor, rotulo ("*38* de 45"), durGrade
  P.grade = (op = {}) => {
    const lado = op.lado || PAUTA / 2, cols = op.cols || 9, total = op.total || 45, cheios = op.cheios ?? total;
    const rows = Math.ceil(total / cols), x = op.x ?? cfg.x0, top = (op.y ?? P.y) - PAUTA + DESC + 28;
    const cor = corDe(op.cor || 'verde');
    const svg = camada();
    const gFill = el('g', {}, svg), gLin = el('g', {}, svg);
    const t0 = op.at ?? P.t, dG = op.durGrade ?? .9;
    ancora(t0, top + rows * lado + 10);
    const ult = total - (rows - 1) * cols;      // quadradinhos na última linha
    let t = t0; const n = rows + 1 + cols + 1, cada = dG / n;
    for (let r = 0; r <= rows; r++) {
      const wCols = r === rows ? ult : cols;
      tracar(`M${x} ${top + r * lado} L${x + wCols * lado} ${top + r * lado}`, { linha: true, w: 3, at: t, dur: cada * .9, grupo: gLin, seguir: false }); t += cada;
    }
    for (let c = 0; c <= cols; c++) {
      const hRows = c > ult ? rows - 1 : rows;
      tracar(`M${x + c * lado} ${top} L${x + c * lado} ${top + hRows * lado}`, { linha: true, w: 3, at: t, dur: cada * .9, grupo: gLin, seguir: false }); t += cada;
    }
    const tP = op.atPinta ?? (t + .1), dP = op.dur ?? Math.min(2.4, cheios * .06), cadaP = dP / Math.max(1, cheios);
    const cels = [];
    for (let i = 0; i < cheios; i++) {
      const r = Math.floor(i / cols), c = i % cols, cx = x + c * lado, cy = top + r * lado;
      const q = el('rect', { x: cx + 1.5, y: cy + 1.5, width: lado - 3, height: lado - 3, fill: cor, opacity: 0 }, gFill);
      const a = tP + i * cadaP;
      cels.push([q, a]);
      seg(a, a + cadaP, p => [cx + lado * (.15 + .7 * p), cy + lado * (p < .5 ? .8 - 1.2 * p : .2 + 1.2 * (p - .5))], op.cor || 'verde');
    }
    itens.push({ seek(tt) { for (const [q, a] of cels) q.setAttribute('opacity', clamp((tt - a) / (cadaP * .9)) * .92); } });
    let fim = tP + dP;
    const box = { x0: x, x1: x + cols * lado, top, bot: top + rows * lado, fim };
    if (op.rotulo) {
      const r = escrever(op.rotulo, { x: x + cols * lado + 26, y: top + rows * lado / 2 + 18, size: 50, destaque: op.cor || 'verde', at: op.atRotulo ?? fim + .12, camera: false });
      fim = r.fim; box.rotulo = r;
    }
    if (op.y == null) P.y = snap(top + rows * lado + PAUTA - DESC + 30);
    P.t = fim + .25; box.fim = fim;
    return box;
  };

  // TABELA desenhada linha a linha. rows = [['gotas','quilos'],['5','2'],['30', null]] (null = célula vazia, preencher com t.cel)
  // op: x, colW ([..] ou número), alt (92), at, durLinhas, cab (1ª linha colorida), corCab, tempos ([[t,..],..]), size, centro
  P.tabela = (rows, op = {}) => {
    const nR = rows.length, nC = Math.max(...rows.map(r => r.length));
    const alt = op.alt || PAUTA, size = op.size || 46, svg = camada();
    const medir = s => { const t = el('text', { class: 'hand', 'font-size': size, x: -9999, y: -9999 }, svg); t.textContent = (s || '').replace(/\*/g, ''); const w = t.getComputedTextLength(); t.remove(); return w; };
    let colW = op.colW;
    if (!Array.isArray(colW)) colW = Array.from({ length: nC }, (_, c) => colW || Math.max(130, Math.max(...rows.map(r => medir(r[c]))) + 56));
    const W = colW.reduce((a, b) => a + b, 0);
    const x = op.x ?? (op.centro ? cfg.cx - W / 2 : cfg.x0), top = (op.y ?? P.y) - PAUTA + DESC + 28;
    const t0 = op.at ?? P.t, dL = op.durLinhas ?? 1.0;
    ancora(t0, top + nR * alt + 10);
    const g = el('g', {}, svg);
    const tra = [[`M${x} ${top} L${x + W} ${top} L${x + W} ${top + nR * alt} L${x} ${top + nR * alt} Z`, 2.2]];
    for (let r = 1; r < nR; r++) tra.push([`M${x} ${top + r * alt} L${x + W} ${top + r * alt}`, 1]);
    let xx = x; for (let c = 0; c < nC - 1; c++) { xx += colW[c]; tra.push([`M${xx} ${top} L${xx} ${top + nR * alt}`, 1]); }
    const soma = tra.reduce((a, b) => a + b[1], 0); let t = t0;
    for (const [d, peso] of tra) { const dd = dL * peso / soma; tracar(d, { linha: true, w: 3, at: t, dur: dd * .92, grupo: g, seguir: false }); t += dd; }
    const cx = c => x + colW.slice(0, c).reduce((a, b) => a + b, 0) + colW[c] / 2;
    const base = r => top + r * alt + alt / 2 + size * .32;
    let tt = (op.atTexto ?? t0 + dL + .1), fim = t0 + dL;
    const tab = { x0: x, x1: x + W, top, bot: top + nR * alt, alt,
      meio: r => top + r * alt + alt / 2,
      cel: (r, c, s, o = {}) => { const b = escrever(s, Object.assign({ x: cx(c), y: base(r), ancora: 'middle', size, camera: false }, o)); tab.fim = Math.max(tab.fim || 0, b.fim); return b; } };
    rows.forEach((row, r) => row.forEach((s, c) => {
      if (s == null || s === '') return;
      const at = op.tempos && op.tempos[r] && op.tempos[r][c] != null ? op.tempos[r][c] : tt;
      const b = tab.cel(r, c, s, { at, cor: op.cab !== false && r === 0 ? (op.corCab || 'amarelo') : op.cor, vel: .045 });
      tt = b.fim + (op.gap ?? .12); fim = Math.max(fim, b.fim);
    }));
    tab.fim = fim;
    if (op.y == null) P.y = snap(top + nR * alt + PAUTA - DESC + 30);
    P.t = fim + .25;
    return tab;
  };

  // DESENHO vetorial da biblioteca doodles.js (ou traços próprios [{d, cor, fill, w}] centrados em 0,0)
  P.desenho = (nome, op = {}) => {
    const tracos = typeof nome === 'string' ? LV.doodles[nome](...(op.params || [])) : nome;
    if (!tracos) throw new Error('doodle inexistente: ' + nome);
    const svg = op.layer || camada();
    const x = op.x ?? cfg.cx, y = op.y ?? P.y, s = op.s ?? 1, rot = (op.rot || 0) * Math.PI / 180;
    const g = el('g', { transform: `translate(${x} ${y}) rotate(${op.rot || 0}) scale(${s})` }, svg);
    const toW = (px, py) => [x + s * (px * Math.cos(rot) - py * Math.sin(rot)), y + s * (px * Math.sin(rot) + py * Math.cos(rot))];
    const pts = [];
    const objs = tracos.map(tr => {
      const c = tr.cor || op.cor;
      if (tr.fill && !tr.stroke) { const p = el('path', { d: tr.d, fill: corDe(c), opacity: 0 }, g); return { p, fill: true }; }
      const p = el('path', { d: tr.d, fill: 'none', stroke: corDe(c), 'stroke-width': (tr.w || 1) * (op.w || 5) / s, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
      const len = p.getTotalLength();
      p.setAttribute('stroke-dasharray', `${len + 2} ${len + 2}`); p.setAttribute('stroke-dashoffset', len + 2);
      return { p, len, c };
    });
    const total = objs.reduce((a, o) => a + (o.len || 0), 0) * s, gap = .06;
    const nS = objs.filter(o => !o.fill).length;
    const dur = op.dur ?? clamp(total / (op.vel || 1000), .3, 3);
    const tD = Math.max(.12, dur - gap * (nS - 1));
    let t = op.at ?? P.t; const t0 = t;
    for (const o of objs) {
      if (o.fill) { o.t0 = t - gap * .5; o.t1 = o.t0 + .14; continue; }
      o.t0 = t; o.t1 = t + tD * (o.len * s / Math.max(1, total)); t = o.t1 + gap;
      const p = o.p, len = o.len;
      seg(o.t0, o.t1, q => { const pt = p.getPointAtLength(q * len); return toW(pt.x, pt.y); }, o.c);
    }
    itens.push({ seek(tt) {
      for (const o of objs) {
        if (o.fill) { o.p.setAttribute('opacity', clamp((tt - o.t0) / (o.t1 - o.t0))); continue; }
        o.p.setAttribute('stroke-dashoffset', (o.len + 2) * (1 - clamp((tt - o.t0) / (o.t1 - o.t0))));
      }
    } });
    if (!op.layer && op.camera !== false) ancora(t0, y + 100 * s);
    P.t = t - gap + .15;
    return { fim: t - gap, x, y };
  };
  P.circular = (b, op = {}) => P.desenho(LV.doodles.circulo(b.w, b.h), Object.assign({ x: b.cx, y: b.cy, cor: 'amarelo', camera: false }, op));
  P.sublinhar = (b, op = {}) => P.desenho(LV.doodles.sublinhado(b.w), Object.assign({ x: b.cx, y: b.base + 16, cor: 'amarelo', camera: false }, op));
  P.riscar = (b, op = {}) => P.desenho(LV.doodles.risco(b.w), Object.assign({ x: b.cx, y: b.cy, cor: 'vermelho', camera: false }, op));

  // ÍCONE: emoji (ou imagem com op.src) que o lápis "pinta" e estoura no lugar
  P.icone = (emoji, op = {}) => {
    const size = op.size || 120, x = op.x ?? 800, y = op.y ?? P.y, at = op.at ?? P.t;
    const g = el('g', { opacity: 0 }, camada());
    if (op.src) el('image', { href: op.src, x: -size / 2, y: -size / 2, width: size, height: size }, g);
    else { const t = el('text', { class: 'emoji', 'font-size': size, 'text-anchor': 'middle', x: 0, y: size * .34 }, g); t.textContent = emoji; }
    const d = .34;
    seg(at - d, at, p => [x - size * .4 + size * .8 * p, y + Math.sin(p * Math.PI * 5) * size * .32], op.cor || 'amarelo');
    LV.cues.push({ t: at, type: 'pop' });
    itens.push({ seek(tt) {
      const p = clamp((tt - at) / .32);
      g.setAttribute('opacity', clamp(p * 3));
      g.setAttribute('transform', `translate(${x} ${y}) rotate(${(1 - E.out(p)) * -10 + (op.rot || 0)}) scale(${lerp(.4, 1, E.outBack(p))})`);
    } });
    if (op.camera !== false) ancora(at - d, y + size / 2);
    P.t = at + .4;
    return { x, y, fim: at + .32 };
  };

  // FOTO/print colado com fita. op: x, y (centro), w, prop (h/w), rot, at
  P.foto = (src, op = {}) => {
    const w = op.w || 420, h = op.h || w * (op.prop || .62), x = op.x ?? cfg.cx, y = op.y ?? (P.y - PAUTA + DESC + h / 2 + 20);
    const rot = op.rot ?? (rnd() * 5 - 2.5), at = op.at ?? P.t, b = op.borda ?? 12;
    const g = el('g', { opacity: 0 }, fotosSvg), inner = el('g', { class: 'foto' }, g);
    el('rect', { x: -b, y: -b, width: w + 2 * b, height: h + 2 * b, rx: 5, fill: '#FBFAF6' }, inner);
    el('image', { href: src, x: 0, y: 0, width: w, height: h, preserveAspectRatio: 'xMidYMid slice' }, inner);
    el('rect', { x: w / 2 - 75, y: -b - 22, width: 150, height: 42, rx: 3, fill: 'rgba(240,226,180,.82)', transform: `rotate(${-3 + rnd() * 6} ${w / 2} ${-b})` }, inner);
    LV.cues.push({ t: at, type: 'pop' });
    itens.push({ seek(tt) {
      const p = clamp((tt - at) / .38);
      g.setAttribute('opacity', clamp(p * 2.5));
      g.setAttribute('transform', `translate(${x} ${y}) rotate(${rot + (1 - E.out(p)) * 6}) scale(${lerp(1.18, 1, E.outBack(p))}) translate(${-w / 2} ${-h / 2})`);
    } });
    ancora(at - .2, y + h / 2 + 20);
    if (op.y == null) P.y = snap(y + h / 2 + PAUTA);
    P.t = at + .5;
    return { x, y, w, h, x0: x - w / 2, x1: x + w / 2, cx: x, cy: y, base: y + h / 2, fim: at + .38 };
  };

  // CTA final: a página escurece e o lápis escreve a chamada por cima (coordenadas de TELA)
  // op: at, seta ('baixo' | 'comentario' | false), cor, y
  P.cta = (l1, l2, op = {}) => { ctas.push({ l1, l2, op: Object.assign({ at: P.t }, op) }); P.t = (op.at ?? P.t) + 2; };
  function montarCtas() {
    for (const { l1, l2, op } of ctas) {
      const cam = scrollAlvo(1e9), at = op.at, y = (op.y || 905) + cam;
      itens.push({ seek(tt) { dimEl.style.opacity = clamp((tt - (at - .35)) / .4); } });
      LV.cues.push({ t: at - .3, type: 'whoosh' });
      const a = escrever(l1, { layer: ctaSvg, x: 540, y, ancora: 'middle', size: op.size || 124, negrito: true, cor: op.cor || 'amarelo', destaque: 'ink', at, vel: .06 });
      let fim = a.fim, yb = y;
      if (l2) { const b = escrever(l2, { layer: ctaSvg, x: 540, y: y + 112, ancora: 'middle', size: op.size2 || 68, cor: 'ink', destaque: op.cor || 'amarelo', at: a.fim + .12, vel: .045 }); fim = b.fim; yb = y + 112; }
      if (op.seta !== false) {
        const com = op.seta === 'comentario';
        const P0 = [com ? 600 : 640, yb + 70], P1 = com ? [830, cam + 1215] : [500, yb + 330];
        P.layer = ctaSvg;
        const s = P.seta(P0[0], P0[1], P1[0], P1[1], { cor: op.cor || 'amarelo', w: 9, curva: com ? -70 : 40, ponta: 44, at: fim + .15, dur: .45 });
        P.layer = null; fim = s.fim;
      }
    }
  }

  // ---------- LEGENDA em pílula (opcional) ----------
  const legs = [];
  LV.legendas = (o = {}) => {
    if (!cfg._focoManual) cfg.foco = Math.min(cfg.foco, 1180);     // a pílula fica em y 1395: o texto para antes
    const dest = new Set((o.destaques || []).map(norm));
    const max = o.max || 3, maxC = o.maxChars || 17;
    let bloco = [];
    const fecha = () => { if (bloco.length) legs.push({ t0: bloco[0].s - .04, ws: bloco }); bloco = []; };
    for (const w of LV.words) {
      const len = bloco.map(b => b.w).join(' ').length + w.w.length + 1;
      if (bloco.length >= max || (bloco.length && len > maxC) || (bloco.length && w.s - bloco[bloco.length - 1].e > .45)) fecha();
      bloco.push(w);
      if (/[.?!,:;…]$/.test(w.w)) fecha();
    }
    fecha();
    legs.forEach((l, i) => {
      const prox = legs[i + 1];
      l.t1 = prox ? Math.min(prox.t0, l.ws[l.ws.length - 1].e + .9) : l.ws[l.ws.length - 1].e + .6;
      l.html = l.ws.map(w => dest.has(norm(w.w)) ? `<b>${w.w.toUpperCase()}</b>` : w.w.toUpperCase()).join(' ');
    });
  };
  LV.legenda = (texto, t0, t1) => legs.push({ t0, t1, html: texto.toUpperCase().replace(/\*(.+?)\*/g, '<b>$1</b>') });
  let legAtual = -1;
  function seekLegenda(t) {
    const i = legs.findIndex(l => t >= l.t0 && t < l.t1);
    if (i !== legAtual) { legEl.innerHTML = i >= 0 ? `<span>${legs[i].html}</span>` : ''; legAtual = i; }
    if (i >= 0) {
      const p = clamp((t - legs[i].t0) / .14), q = clamp((legs[i].t1 - t) / .1), s = legEl.firstChild;
      s.style.opacity = Math.min(p, q); s.style.transform = `scale(${lerp(.9, 1, E.outBack(p))})`;
    }
  }

  // ---------- PONTA DO LÁPIS no tempo ----------
  let segsOrd = [];
  function penAt(t) {      // → [x, y, encostado(0..1), cor]
    let lo = 0, hi = segsOrd.length - 1, k = -1;
    while (lo <= hi) { const m = (lo + hi) >> 1; if (segsOrd[m].t0 <= t) { k = m; lo = m + 1; } else hi = m - 1; }
    const S = segsOrd[k], N = segsOrd[k + 1];
    if (S && t <= S.t1) { const [x, y] = S.f((t - S.t0) / (S.t1 - S.t0)); return [x, y, 1, S.cor]; }
    const fora = P_ => [P_[0] + 620, P_[1] + 760];
    if (!S) {
      if (!N) return [0, 0, 0, hex(toHex(T.lapisInk))];
      const B = N.f(0), A = fora(B), p = E.inOut(clamp((t - (N.t0 - .55)) / .55));
      return [lerp(A[0], B[0], p), lerp(A[1], B[1], p), 0, N.cor];
    }
    const A = S.f(1);
    if (!N) { const B = fora(A), p = E.inOut(clamp((t - S.t1 - .45) / .7)); return [lerp(A[0], B[0], p), lerp(A[1], B[1], p), 0, S.cor]; }
    const B = N.f(0), gapT = N.t0 - S.t1, dist = Math.hypot(B[0] - A[0], B[1] - A[1]);
    const tr = Math.min(gapT, gapT > 1.2 ? .45 : .26 + .26 * clamp(dist / 900));
    const pc = clamp((t - (N.t0 - tr)) / tr), cor = mix(S.cor, N.cor, clamp(pc * 2 - .5));
    if (gapT > 1.2) {       // pausa longa: descansa ao lado e volta
      const R = [A[0] + 130, A[1] + 150];
      if (t < S.t1 + .4) { const p = E.inOut((t - S.t1) / .4); return [lerp(A[0], R[0], p), lerp(A[1], R[1], p), 0, S.cor]; }
      if (t < N.t0 - tr) { const b = Math.sin((t - S.t1) * 2.1) * 6; return [R[0] + b * .6, R[1] + b, 0, S.cor]; }
      const p = E.inOut(pc); return [lerp(R[0], B[0], p), lerp(R[1], B[1], p), 0, cor];
    }
    if (t < N.t0 - tr) return [A[0], A[1] - 4 * clamp((t - S.t1) / .1), 0, S.cor];
    const p = E.inOut(pc), arco = Math.sin(p * Math.PI) * Math.min(46, dist * .09);
    return [lerp(A[0], B[0], p), lerp(A[1], B[1], p) - arco - 4 * (1 - p), 0, cor];
  }

  function seekLapis(t) {
    const [x, y, down, cor] = penAt(t);
    pintarLapis(cor);
    const lift = 1 - down, s = .86 * cfg.lapisEscala * (1 + .035 * lift);
    const rot = -30 + 12 * clamp(x / QW) + Math.sin(t * 24) * 1.1 * down + Math.sin(t * 1.3) * 1.4;
    LP.g.setAttribute('transform', `translate(${x} ${y}) rotate(${rot}) scale(${s})`);
    const off = 12 + 22 * lift;
    LP.sombra.setAttribute('transform', `translate(${x - off * .9} ${y + off}) rotate(${rot + 5 + 4 * lift}) scale(${s})`);
    LP.sombra.setAttribute('opacity', .9 - .35 * lift);
  }

  // ---------- CÂMERA: a página sobe pra manter a linha que está sendo escrita no foco ----------
  let ancOrd = [];
  function scrollAlvo(t) {
    let m = 0;
    for (const a of ancOrd) { if (a.t - .5 > t) break; m = Math.max(m, a.y - cfg.foco); }
    return m;
  }
  function scrollAt(t) {      // média exponencial do alvo no passado = rolagem macia e determinística
    let s = 0, ws = 0;
    for (let k = 0; k < 24; k++) { const dt = k * .04, w = Math.exp(-dt / .26); s += scrollAlvo(t - dt) * w; ws += w; }
    return s / ws;
  }
  LV.scrollAt = scrollAt;

  // ---------- ciclo ----------
  LV.seek = t => {
    for (const it of itens) it.seek(t);
    const sc = scrollAt(t), tr = `translate(0px, ${-sc}px)`;
    world.style.transform = tr; world2.style.transform = tr;
    seekLapis(t);
    seekLegenda(t);
  };
  LV.roteiro = fn => { LV._fn = fn; };

  async function iniciar() {
    await document.fonts.load('80px Lapis');
    await document.fonts.load('800 40px Inter');
    await document.fonts.ready;
    montar();
    LV._fn(Object.assign({ p: P }, LV));
    ancOrd = ancoras.slice().sort((a, b) => a.t - b.t);
    montarCtas();
    segsOrd = segs.slice().sort((a, b) => a.t0 - b.t0);
    let cur = null;
    for (const s of segsOrd) {
      if (cur && s.t0 - cur.t1 < .09) cur.t1 = Math.max(cur.t1, s.t1);
      else { if (cur) LV.cues.push({ t: cur.t0, type: 'risco', dur: cur.t1 - cur.t0 }); cur = { t0: s.t0, t1: s.t1 }; }
    }
    if (cur) LV.cues.push({ t: cur.t0, type: 'risco', dur: cur.t1 - cur.t0 });
    LV.cues.push({ ferramenta: 'lapis' });
    LV.duration = cfg.duracao || (segsOrd.length ? segsOrd[segsOrd.length - 1].t1 + 1.2 : 5);
    const altura = Math.max(QH, scrollAlvo(1e9) + QH) + 400;
    pagina.style.height = altura + 'px';
    for (const s of [inkSvg, ctaSvg, fotosSvg, lapisEl]) { s.setAttribute('height', altura); s.setAttribute('viewBox', `0 0 ${QW} ${altura}`); }
    const q = new URLSearchParams(location.search);
    if (q.has('render')) LV.seek(0);
    else if (q.has('t')) LV.seek(+q.get('t'));
    else {
      const t0 = performance.now();
      const loop = () => { LV.seek(((performance.now() - t0) / 1000) % LV.duration); requestAnimationFrame(loop); };
      loop();
    }
  }
  // tema pela URL (?tema=creme) — útil pra renderizar o mesmo roteiro em vários temas
  const qs = new URLSearchParams(location.search);
  LV._temaUrl = qs.get('tema');
  const _config = LV.config;
  LV.config = o => { _config(o); if (LV._temaUrl) cfg.tema = LV._temaUrl; };
  if (LV._temaUrl) cfg.tema = LV._temaUrl;
  // erro no roteiro (palavra não encontrada, doodle inexistente…) não pode travar o render: vira LV.erro
  window.LV_READY = new Promise(r => window.addEventListener('load', () => iniciar().then(r, e => { LV.erro = String(e && e.stack || e); console.error(LV.erro); r(); })));
})();
