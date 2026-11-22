/* Kinetic Creme — motor de animação determinístico.
   Tudo é função do tempo t (segundos): KC.seek(t) posiciona cada elemento.
   Isso permite renderizar quadro a quadro (render.mjs) com resultado idêntico. */
(function () {
  const W = 1080, H = 1920, CX = 495; // CX = centro da área segura dos Reels (x 90..900)
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const mix = (a, b, k) => a + (b - a) * k;
  const Ease = {
    lin: x => x,
    inCubic: x => x * x * x,
    outCubic: x => 1 - Math.pow(1 - x, 3),
    inOutCubic: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
    outQuint: x => 1 - Math.pow(1 - x, 5),
    outExpo: x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x),
    inExpo: x => x <= 0 ? 0 : Math.pow(2, 10 * x - 10),
    inOutExpo: x => x <= 0 ? 0 : x >= 1 ? 1 : x < .5 ? Math.pow(2, 20 * x - 10) / 2 : (2 - Math.pow(2, -20 * x + 10)) / 2,
    outBack: (x, s = 1.70158) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2),
  };
  const prog = (t, a, d, e = Ease.lin) => e(clamp((t - a) / d));
  function rng(seed) { // mulberry32
    return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let r = Math.imul(seed ^ seed >>> 15, 1 | seed);
      r = r + Math.imul(r ^ r >>> 7, 61 | r) ^ r; return ((r ^ r >>> 14) >>> 0) / 4294967296; };
  }

  const updaters = [], cues = [], shakes = [];
  let DURATION = 15, HANDLE = '';
  const on = fn => (updaters.push(fn), fn);
  const cue = (t, type, gain = 0) => cues.push({ t: +t.toFixed(3), type, gain });
  const shake = (t, amp = 12, dur = .45) => shakes.push({ t, amp, dur });

  function el(tag, cls, parent, html) {
    const e = document.createElement(tag); if (cls) e.className = cls;
    if (html != null) e.innerHTML = html; parent.appendChild(e); return e;
  }
  function svg(tag, attrs, parent) {
    const e = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e;
  }
  // Coloca um elemento centrado em (x,y) e devolve uma função de transformação.
  function put(e, x, y) { e.classList.add('abs'); e._x = x; e._y = y; tf(e, {}); return e; }
  function tf(e, { x = 0, y = 0, s = 1, r = 0, o = 1, b = 0, rx = 0, sx = 1 } = {}) {
    e.style.transform = `translate(${e._x + x}px,${e._y + y}px) translate(-50%,-50%)` +
      (rx ? ` perspective(1400px) rotateX(${rx}deg)` : '') + ` rotate(${r}deg) scale(${s * sx},${s})`;
    e.style.opacity = clamp(o);
    e.style.filter = b > .25 ? `blur(${b.toFixed(2)}px)` : 'none';
    e.style.visibility = o <= .001 ? 'hidden' : 'visible';
  }
  // Entrada padrão "pop": cresce com leve overshoot + sai do desfoque.
  function popIn(e, t0, { d = .55, from = .55, blur = 14, dy = 18, sound = 'pop' } = {}) {
    if (sound) cue(t0, sound);
    return t => { const k = prog(t, t0, d), kb = Ease.outBack(k, 2.1), ke = Ease.outExpo(k);
      return { s: mix(from, 1, kb), o: clamp(k * 3), b: (1 - ke) * blur, y: (1 - ke) * dy }; };
  }

  /* ---------------- fundo ---------------- */
  function background(frame, { handle = '' } = {}) {
    const bg = el('div', '', frame); bg.id = 'bg';
    el('div', '', bg).id = 'glow';
    const grain = el('div', '', bg); grain.id = 'grain';
    grain.style.backgroundImage = `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`;
    // passarinhos em traço
    const R = rng(7), birds = svg('svg', { width: W, height: 700, style: 'position:absolute;left:0;top:0' }, bg);
    const bl = [];
    for (let i = 0; i < 16; i++) {
      const x = R() * W, y = 40 + R() * 600, sc = .6 + R() * .7;
      const g = svg('g', {}, birds);
      svg('path', { d: 'M-14 0 Q-7 -7 0 0 Q7 -7 14 0', fill: 'none', stroke: '#B8A68F', 'stroke-width': 2.4, 'stroke-linecap': 'round', opacity: .55 + R() * .3 }, g);
      bl.push({ g, x, y, sc, v: 6 + R() * 10, ph: R() * 6 });
    }
    on(t => bl.forEach(b => { const fl = .55 + .45 * Math.abs(Math.sin(t * 3 + b.ph));
      b.g.setAttribute('transform', `translate(${(b.x + t * b.v) % (W + 40) - 20},${b.y + Math.sin(t * .7 + b.ph) * 4}) scale(${b.sc},${b.sc * fl})`); }));
    // cidade em linha fina
    const SW = W + 240, base = 330, sk = svg('svg', { width: SW, height: base + 10 }, bg); sk.id = 'skyline';
    const g = svg('g', { fill: 'none', stroke: '#D5C2A8', 'stroke-width': 2.2, 'stroke-linejoin': 'round' }, sk);
    const S = rng(11); let x = 0;
    svg('line', { x1: 0, y1: base, x2: SW, y2: base }, g);
    while (x < SW) {
      const kind = S(), w = 60 + S() * 110;
      if (kind < .55) { // prédio
        const h = 90 + S() * 220; svg('rect', { x, y: base - h, width: w, height: h }, g);
        for (let yy = base - h + 22; yy < base - 18; yy += 26) svg('line', { x1: x + 12, y1: yy, x2: x + w - 12, y2: yy, opacity: .55 }, g);
        if (S() < .3) svg('line', { x1: x + w / 2, y1: base - h, x2: x + w / 2, y2: base - h - 30 }, g);
      } else if (kind < .78) { // casinha
        const hw = 70 + S() * 40, hh = 46; svg('path', { d: `M${x} ${base}V${base - hh}L${x + hw / 2} ${base - hh - 34}L${x + hw} ${base - hh}V${base}` }, g);
        svg('rect', { x: x + hw / 2 - 10, y: base - 30, width: 20, height: 30 }, g);
      } else { // árvore ou poste
        if (S() < .6) { svg('circle', { cx: x + 22, cy: base - 62, r: 20 }, g); svg('line', { x1: x + 22, y1: base - 42, x2: x + 22, y2: base }, g); }
        else svg('path', { d: `M${x + 10} ${base}V${base - 90}Q${x + 10} ${base - 104} ${x + 30} ${base - 104}` }, g);
      }
      x += w + 6 + S() * 30;
    }
    on(t => { sk.style.transform = `translateX(${-t * 5}px)`; });
    if (handle) el('div', '', bg, handle).id = 'handle';
    return bg;
  }

  /* ---------------- cenas e transições ---------------- */
  const TR = .44; // duração da transição (centrada no corte)
  function scene(cam, start, end, { out = 'whip', last = false, breathe = .025 } = {}) {
    const s = el('div', 'scene', cam), h = TR / 2;
    if (start > 0) cue(start - .2, 'whoosh');
    on(t => {
      const vis = (start <= 0 || t >= start - h) && (last || t < end + h);
      s.style.display = vis ? 'block' : 'none'; if (!vis) return;
      let x = 0, y = 0, r = 0, b = 0, o = 1, sc = 1 + breathe * prog(t, start, end - start, Ease.inOutCubic);
      if (start > 0 && t < start + h) { const k = prog(t, start - h, TR);
        x = (1 - Ease.outCubic(k)) * 620; b = (1 - Ease.outCubic(k)) * 30; o = clamp(k * 2.4); }
      if (!last && t > end - h) { const k = prog(t, end - h, TR);
        if (out === 'tilt') { const e = Ease.inCubic(k); x -= 520 * e; y += 70 * e; r = -8 * e; sc *= 1 - .1 * e; b += 26 * k; o *= 1 - Ease.inCubic(k); }
        else { const e = Ease.inCubic(k); x -= 640 * e; b += 32 * k; o *= 1 - e; }
      }
      s.style.transform = `translate(${x}px,${y}px) rotate(${r}deg) scale(${sc})`; s.style.transformOrigin = `${CX}px 760px`;
      s.style.opacity = o; s.style.filter = b > .25 ? `blur(${b}px)` : 'none';
    });
    return s;
  }

  /* ---------------- texto cinético ---------------- */
  // spec: "Essa *ferramenta* faz\nvídeos *ilimitados*"  (*…* = destaque laranja, \n = quebra)
  function words(parent, spec, { x = CX, y = 800, size = 96, cls = 'hl', t0 = 0, step = .13, d = .5, align = 'center', width = null, letters = false, color = null, sound = false } = {}) {
    const box = el('div', 'words ' + cls, parent); box.style.fontSize = size + 'px'; box.style.textAlign = align;
    if (color) box.style.color = color;
    if (width) { box.style.width = width + 'px'; box.style.whiteSpace = 'normal'; }
    const spans = [], lines = [];
    spec.split('\n').forEach(line => {
      const ln = el('div', 'ln', box), inn = el('span', 'lnIn', ln); lines.push(inn);
      line.split(' ').filter(Boolean).forEach((tok, i, arr) => {
        const acc = /^\*.*\*[.,!?:]*$/.test(tok) || /^\*/.test(tok) && tok.endsWith('*');
        const txt = tok.replace(/\*/g, '');
        const units = letters ? [...txt] : [txt];
        units.forEach(u => { const sp = el('span', 'w' + (acc ? ' acc' : ''), inn, u === ' ' ? '&nbsp;' : u); spans.push(sp); });
        if (i < arr.length - 1) { const gap = el('span', 'w', inn, '&nbsp;'); gap._gap = 1; spans.push(gap); }
      });
    });
    put(box, x, y);
    let i = 0; const times = [];
    spans.forEach(sp => { if (sp._gap) { sp._t = null; return; } sp._t = t0 + i++ * step; times.push(sp._t); if (sound) cue(sp._t, 'type', -6); });
    on(t => spans.forEach(sp => { if (sp._t == null) return;
      const k = prog(t, sp._t, d), e = Ease.outExpo(k);
      sp.style.opacity = clamp(k * 2.2); sp.style.transform = `translateY(${(1 - e) * 30}px) scale(${mix(.94, 1, e)})`;
      sp.style.filter = e < .98 ? `blur(${((1 - e) * 13).toFixed(2)}px)` : 'none'; }));
    return { box, spans, lines, end: times.length ? times[times.length - 1] + d : t0 };
  }

  /* ---------------- ícones, pílulas, conectores ---------------- */
  const ICONS = {
    doc: c => `<svg width="46%" viewBox="0 0 60 72"><path d="M6 4h32l16 16v46a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" fill="none" stroke="#1C1915" stroke-width="4.5" stroke-linejoin="round"/><path d="M38 4v16h16" fill="none" stroke="#1C1915" stroke-width="4.5" stroke-linejoin="round"/><text x="29" y="52" font-family="JetBrains Mono,monospace" font-size="10" font-weight="700" text-anchor="middle" fill="${c}">.vid</text></svg>`,
    spark: c => { let p = ''; for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2, l = i % 2 ? 26 : 34;
        p += `<line x1="${50 + Math.cos(a) * 7}" y1="${50 + Math.sin(a) * 7}" x2="${50 + Math.cos(a) * l}" y2="${50 + Math.sin(a) * l}"/>`; }
      return `<svg class="spk" width="62%" viewBox="0 0 100 100"><g stroke="${c}" stroke-width="7.5" stroke-linecap="round">${p}</g></svg>`; },
    play: c => `<svg width="44%" viewBox="0 0 60 60"><rect x="3" y="3" width="54" height="54" rx="14" fill="none" stroke="#1C1915" stroke-width="4.5"/><path d="M24 18l18 12-18 12z" fill="${c}"/></svg>`,
    mail: c => `<svg width="70%" viewBox="0 0 40 30"><rect x="2" y="2" width="36" height="26" rx="5" fill="#fff"/><path d="M4 5l16 12L36 5" fill="none" stroke="${c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    q: c => `<svg width="60%" viewBox="0 0 60 60"><text x="30" y="44" text-anchor="middle" font-family="Inter,Arial" font-weight="900" font-size="44" fill="${c}">?</text></svg>`,
  };
  function tile(parent, { x, y, size = 150, icon = 'doc', color = '#E8742E', t0 = 0, spin = 0, pulses = [], bare = false } = {}) {
    const e = el('div', 'tile', parent, ICONS[icon](color)); e.style.width = e.style.height = size + 'px'; put(e, x, y);
    if (bare) { e.style.background = 'none'; e.style.boxShadow = 'none'; }
    const a = popIn(e, t0, { from: .4 }), spk = e.querySelector('.spk');
    on(t => { const st = a(t); let pz = 0; pulses.forEach(p => { const k = (t - p) / .35; if (k > 0 && k < 1) pz += Math.sin(k * Math.PI) * .07; });
      st.s *= 1 + pz; tf(e, st); if (spk) spk.style.transform = `rotate(${t * spin}deg)`; });
    return e;
  }
  function pill(parent, { x, y, text, t0, icon = 'check' }) {
    const e = el('div', 'pill', parent, (icon ? `<span class="chk"><svg width="22" viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>` : '') + `<span>${text}</span>`);
    put(e, x, y); const a = popIn(e, t0); on(t => tf(e, a(t))); return e;
  }
  function monoChip(parent, { x, y, t0, text }) { // text: string ou fn(t)
    const e = el('div', 'mchip', parent); put(e, x, y); const a = popIn(e, t0, { sound: null });
    let last = ''; on(t => { const s = typeof text === 'function' ? text(t) : text; if (s !== last) e.innerHTML = last = s; tf(e, a(t)); }); return e;
  }
  function connector(parent, { x1, y1, x2, y2, t0, d = .5, dots = 3, period = 1.3 }) {
    const s = svg('svg', { width: W, height: H, style: 'position:absolute;left:0;top:0;overflow:visible' }, parent);
    const len = Math.hypot(x2 - x1, y2 - y1);
    const ln = svg('line', { x1, y1, x2, y2, stroke: '#F0802A', 'stroke-width': 4.5, 'stroke-linecap': 'round', 'stroke-dasharray': len, 'stroke-dashoffset': len }, s);
    const ends = [svg('circle', { cx: x1, cy: y1, r: 8, fill: '#F0802A' }, s), svg('circle', { cx: x2, cy: y2, r: 8, fill: '#F0802A' }, s)];
    const ds = []; for (let i = 0; i < dots; i++) ds.push(svg('circle', { r: 7.5, fill: '#F0802A' }, s));
    on(t => { const k = prog(t, t0, d, Ease.inOutCubic); ln.setAttribute('stroke-dashoffset', len * (1 - k));
      ends[0].setAttribute('opacity', k > 0 ? 1 : 0); ends[1].setAttribute('opacity', k >= 1 ? 1 : 0);
      ds.forEach((c, i) => { const u = ((t - t0 - d) / period + i / dots) % 1; const vis = t > t0 + d;
        const ue = Ease.inOutCubic(Math.max(0, u)); c.setAttribute('cx', mix(x1, x2, ue)); c.setAttribute('cy', mix(y1, y2, ue)); c.setAttribute('opacity', vis ? Math.sin(Math.max(0, u) * Math.PI) : 0); }); });
    return s;
  }

  /* ---------------- miniaturas (cards/celulares) ---------------- */
  const PAL = [['#F4A259', '#BC4B51'], ['#2E2A27', '#F47B20'], ['#7FB7BE', '#2D4654'], ['#F2E3C9', '#E07A3F'], ['#3A3633', '#8C6A4F'], ['#E8C07D', '#8D5A3B'], ['#A7C4A0', '#3E5C4A']];
  function thumbHTML(R, kind) {
    const [a, b] = PAL[Math.floor(R() * PAL.length)];
    if (kind === 'ui') return `<div style="width:100%;height:100%;background:#fff;padding:9px">
      <div style="height:9px;width:55%;border-radius:4px;background:#2B2622"></div>
      <div style="height:38%;margin-top:8px;border-radius:8px;background:linear-gradient(135deg,${a},${b})"></div>
      ${[70, 90, 50, 80].map(w => `<div style="height:6px;width:${w}%;margin-top:7px;border-radius:3px;background:#DDD4C8"></div>`).join('')}
      <div style="height:12px;width:45%;margin-top:9px;border-radius:6px;background:#F47B20"></div></div>`;
    if (kind === 'dark') return `<div style="width:100%;height:100%;background:#22201E;padding:9px">
      <div style="height:8px;width:40%;border-radius:4px;background:#6E665D"></div>
      <svg viewBox="0 0 100 60" style="width:100%;margin-top:10px"><path d="M0 55 L15 50 L30 52 L45 38 L60 40 L75 22 L100 8 V60 H0Z" fill="${b}" opacity=".35"/><path d="M0 55 L15 50 L30 52 L45 38 L60 40 L75 22 L100 8" fill="none" stroke="#F47B20" stroke-width="3"/></svg>
      <div style="height:16px;width:60%;margin-top:6px;border-radius:5px;background:#F47B20"></div></div>`;
    // "foto" abstrata: céu + sol + silhueta
    return `<div style="width:100%;height:100%;position:relative;background:linear-gradient(170deg,${a},${b})">
      <div style="position:absolute;left:${20 + R() * 40}%;top:${15 + R() * 20}%;width:34%;aspect-ratio:1;border-radius:50%;background:rgba(255,240,215,.75)"></div>
      <div style="position:absolute;left:-10%;right:-10%;bottom:-8%;height:48%;border-radius:50% 50% 0 0;background:rgba(30,20,15,.45)"></div>
      <div style="position:absolute;left:12%;bottom:10%;width:30%;height:6px;border-radius:3px;background:rgba(255,255,255,.85)"></div></div>`;
  }
  // Cards que "jorram" de um ponto e se espalham numa região (ex.: do ícone pra cima).
  function cardBurst(parent, { fx, fy, t0, t1, n = 14, region = [120, 30, 1040, 400], seed = 3, hubPulses = null }) {
    const R = rng(seed), kinds = ['photo', 'ui', 'photo', 'dark'];
    for (let i = 0; i < n; i++) {
      const w = 96 + R() * 46, h = w * 1.55, kind = kinds[Math.floor(R() * kinds.length)];
      const e = el('div', 'thumb', parent, thumbHTML(R, kind)); e.style.width = w + 'px'; e.style.height = h + 'px';
      put(e, fx, fy); e.style.zIndex = 5 + i;
      const ts = t0 + (t1 - t0) * (i / n) + R() * .05, tx = region[0] + R() * (region[2] - region[0]), ty = region[1] + R() * (region[3] - region[1]);
      const rot = -40 + R() * 80, arc = -120 - R() * 160, drift = (R() - .5) * 18, dr = (R() - .5) * 8;
      if (hubPulses) hubPulses.push(ts);
      if (i % 3 === 0) cue(ts, 'flick', -8);
      on(t => { const k = prog(t, ts, .85), e2 = Ease.outExpo(k), tt = Math.max(0, t - ts);
        const x = mix(0, tx - fx, e2) + drift * tt, y = mix(0, ty - fy, e2) + Math.sin(k * Math.PI) * arc * (1 - e2) + Math.sin(tt * 1.3 + i) * 5;
        tf(e, { x, y, s: mix(.15, 1, Ease.outBack(k, 1.4)), r: mix(0, rot, e2) + dr * tt, o: clamp(k * 6), b: (1 - e2) * 6 }); });
    }
  }

  /* ---------------- janela escura (app/IDE/dashboard) ---------------- */
  function windowCard(parent, { x, y, w = 820, h = 640, title = '<i>●</i> studio · painel', t0 }) {
    const e = el('div', 'win', parent, `<div class="bar"><span class="dot" style="background:#FF5F57"></span><span class="dot" style="background:#FEBC2E"></span><span class="dot" style="background:#28C840"></span><div class="ttl">${title}</div></div><div class="body"></div>`);
    e.style.width = w + 'px'; e.style.height = h + 'px'; put(e, x, y); cue(t0, 'whoosh_soft', -4);
    on(t => { const k = prog(t, t0, .7), ex = Ease.outExpo(k);
      tf(e, { y: (1 - ex) * 160, rx: (1 - ex) * 28, s: mix(.9, 1, ex), o: clamp(k * 3), b: (1 - ex) * 16 }); });
    return { e, body: e.querySelector('.body'), w, h };
  }
  // lines: [[ [texto, classe], ... ], ...]  — digitação caractere a caractere
  function codeTyper(body, { lines, t0, cps = 120, until = 1e9, foot = null }) {
    const c = el('div', 'code', body); let total = 0; lines.forEach(l => l.forEach(([s]) => total += s.length)); total += lines.length;
    for (let tt = t0; tt < t0 + total / cps; tt += .085) cue(tt, 'type', -10);
    let last = -1;
    on(t => { const n = Math.floor(clamp((t - t0) * cps, 0, total)), blink = Math.floor(t * 2.4) % 2 === 0 || n < total;
      const key = n * 2 + (blink ? 1 : 0); if (key === last) return; last = key;
      let left = n, html = '';
      for (const l of lines) { for (const [s, k] of l) { if (left <= 0) break; const part = s.slice(0, left); left -= part.length; html += `<span class="${k || ''}">${part.replace(/</g, '&lt;')}</span>`; }
        if (left <= 0) break; left--; html += '\n'; }
      c.innerHTML = html + (blink ? '<span class="caret"></span>' : '') ; });
    c.style.position = 'absolute'; c.style.inset = '0';
    on(t => { const k = prog(t, until, .35, Ease.inCubic); c.style.opacity = 1 - k; c.style.transform = `translateY(${-30 * k}px)`; c.style.filter = k > .02 ? `blur(${k * 10}px)` : 'none'; });
    return c;
  }
  const fmt = v => Math.round(v).toLocaleString('pt-BR');
  function statTile(body, { x, y, w, h = 150, label, from = 0, to, t0, d = 1.1, suffix = '' }) {
    const e = el('div', 'stat', body, `<div class="lb">${label}</div><div class="vl">0</div>`); e.style.left = x + 'px'; e.style.top = y + 'px'; e.style.width = w + 'px'; e.style.height = h + 'px';
    const vl = e.querySelector('.vl');
    for (let i = 0; i < 9; i++) cue(t0 + .05 + i * d / 11, 'tick', -14 - i);
    on(t => { const k = prog(t, t0 - .25, .4, Ease.outCubic); e.style.opacity = k; e.style.transform = `translateY(${(1 - k) * 20}px)`;
      vl.textContent = fmt(mix(from, to, prog(t, t0, d, Ease.outExpo))) + suffix; });
    return e;
  }
  function areaChart(body, { x, y, w, h, t0, d = 1.2, seed = 5, label = 'alcance', up = '▲ subindo' }) {
    const p = el('div', 'panel', body, `<div class="lb">${label}</div><div class="up">${up}</div>`); Object.assign(p.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' });
    const R = rng(seed), N = 16, pts = []; let v = .08;
    for (let i = 0; i < N; i++) { const u = i / (N - 1); v = Math.max(v, .06 + Math.pow(u, 2.2) * .85 + (R() - .5) * .07); pts.push([28 + u * (w - 56), h - 26 - v * (h - 90)]); }
    const s = svg('svg', { width: w, height: h, style: 'position:absolute;left:0;top:0' }, p), id = 'g' + seed;
    s.innerHTML = `<defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F47B20" stop-opacity=".6"/><stop offset="1" stop-color="#F47B20" stop-opacity="0"/></linearGradient><clipPath id="c${id}"><rect x="0" y="0" width="0" height="${h}"/></clipPath></defs>`;
    const line = 'M' + pts.map(q => q.join(' ')).join(' L');
    const g = svg('g', { 'clip-path': `url(#c${id})` }, s);
    svg('path', { d: line + ` L${pts[N - 1][0]} ${h} L${pts[0][0]} ${h}Z`, fill: `url(#${id})` }, g);
    svg('path', { d: line, fill: 'none', stroke: '#F47B20', 'stroke-width': 5, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }, g);
    const dot = svg('circle', { r: 11, fill: '#fff', stroke: 'rgba(244,123,32,.35)', 'stroke-width': 10 }, s);
    const clip = s.querySelector('rect');
    on(t => { const k = prog(t, t0, d, Ease.inOutCubic), xx = mix(pts[0][0], pts[N - 1][0], k); clip.setAttribute('width', xx + 3);
      let j = 0; while (j < N - 2 && pts[j + 1][0] < xx) j++; const u = clamp((xx - pts[j][0]) / (pts[j + 1][0] - pts[j][0]));
      dot.setAttribute('cx', xx); dot.setAttribute('cy', mix(pts[j][1], pts[j + 1][1], u)); dot.setAttribute('opacity', k > .02 ? 1 : 0);
      const ka = prog(t, t0 - .3, .4); p.style.opacity = ka; });
    return p;
  }
  function tag(parent, { x, y, text, rot = -3, t0, white = false, icon = '' }) {
    const e = el('div', 'tag' + (white ? ' white' : ''), parent, icon + text); put(e, x, y);
    const a = popIn(e, t0, { from: .4 }); on(t => { const st = a(t); st.r = rot * Ease.outBack(prog(t, t0, .6), 3); tf(e, st); }); return e;
  }
  function captionCard(parent, { x, y, w, spec, t0, step = .16, size = 40 }) {
    const c = el('div', 'capcard', parent); c.style.width = w + 'px'; put(c, x, y);
    const wd = words(c, spec, { size, cls: 'hl', t0: t0 + .15, step, align: 'left', width: w - 68 });
    wd.box.classList.remove('abs'); wd.box.style.transform = 'none'; wd.box.style.position = 'relative'; wd.box.style.lineHeight = '1.28'; wd.box.style.letterSpacing = '-.02em';
    on(t => { const k = prog(t, t0, .6), e = Ease.outExpo(k); tf(c, { y: (1 - e) * 60, o: clamp(k * 3), b: (1 - e) * 12 }); });
    return c;
  }

  /* ---------------- risco + carimbo ---------------- */
  function strikeLines(wd, { t0, gap = .14, dim = .4 }) {
    wd.lines.forEach((ln, i) => { const b = el('div', 'strike', ln); const ts = t0 + i * gap; cue(ts, 'swipe', -6);
      on(t => { const k = prog(t, ts, .32, Ease.outCubic); b.style.width = `${108 * k}%`; }); });
    on(t => { const k = prog(t, t0, .4); wd.box.style.opacity = mix(1, dim, k); });
  }
  function stamp(parent, { x, y, text, rot = -3, t0 }) {
    const e = el('div', 'stamp', parent, text); put(e, x, y); cue(t0 + .06, 'impact'); shake(t0 + .1, 14, .5);
    on(t => { const k = prog(t, t0, .45), e2 = Ease.outExpo(k);
      tf(e, { s: mix(1.9, 1, Ease.outBack(k, 1.2)), r: mix(-12, rot, e2), o: clamp(k * 4), b: (1 - e2) * 18 }); });
    return e;
  }

  /* ---------------- rede: hub + celulares ---------------- */
  function hubNetwork(parent, { cx, cy, r = 320, n = 6, t0, icon = 'spark', seed = 9, labels = ['+12 mil', '+8 mil', '+21 mil', '+5 mil', '+15 mil', '+9 mil'] }) {
    const R = rng(seed), s = svg('svg', { width: W, height: H, style: 'position:absolute;left:0;top:0' }, parent);
    const halo = el('div', '', parent); Object.assign(halo.style, { width: '330px', height: '330px', borderRadius: '30%', border: '3px solid rgba(240,128,42,.25)', background: 'rgba(240,128,42,.05)' }); put(halo, cx, cy);
    const pulses = [];
    for (let i = 0; i < n; i++) {
      const a = -Math.PI / 2 + i / n * Math.PI * 2 + (R() - .5) * .35, rr = r * (.9 + R() * .2);
      const px = cx + Math.cos(a) * rr * 1.08, py = cy + Math.sin(a) * rr * .95, ts = t0 + .2 + i * .09;
      const len = Math.hypot(px - cx, py - cy);
      const ln = svg('line', { x1: cx, y1: cy, x2: px, y2: py, stroke: '#F0802A', 'stroke-width': 3.5, 'stroke-dasharray': len, 'stroke-dashoffset': len, opacity: .85 }, s);
      const dot = svg('circle', { r: 7, fill: '#F0802A' }, s);
      const ph = el('div', 'phone', parent, `<div class="scr">${thumbHTML(R, ['photo', 'ui', 'dark'][i % 3])}</div>`); ph.style.width = '128px'; ph.style.height = '230px'; put(ph, px, py);
      const a2 = popIn(ph, ts + .2, { from: .3, sound: i % 2 ? null : 'pop' }), rot = (R() - .5) * 18;
      const fl = el('div', 'float', parent, labels[i % labels.length]); put(fl, px + (px > cx ? 70 : -70), py - 140);
      pulses.push(ts);
      on(t => { const k = prog(t, ts, .4, Ease.outCubic); ln.setAttribute('stroke-dashoffset', len * (1 - k));
        const u = ((t - ts - .4) / 1.1) % 1, vis = t > ts + .4; dot.setAttribute('cx', mix(cx, px, Math.max(0, u))); dot.setAttribute('cy', mix(cy, py, Math.max(0, u))); dot.setAttribute('opacity', vis ? Math.sin(Math.max(0, u) * Math.PI) : 0);
        const st = a2(t); st.r = rot + Math.sin(t * 1.4 + i) * 2; st.y += Math.sin(t * 1.8 + i * 1.7) * 6; tf(ph, st);
        const kf = prog(t, ts + .7, .9); tf(fl, { y: -40 * Ease.outCubic(kf), o: Math.sin(kf * Math.PI), b: 0 }); });
    }
    on(t => { const k = prog(t, t0 + .15, .6, Ease.outBack); tf(halo, { s: mix(.5, 1, k) * (1 + .03 * Math.sin(t * 3)), o: clamp(prog(t, t0 + .15, .3)) }); });
    tile(parent, { x: cx, y: cy, size: 170, icon, t0, spin: 14, pulses });
  }

  /* ---------------- CTA: comentário + DM ---------------- */
  function commentBox(parent, { x, y, w = 780, text = 'QUERO', t0, cps = 12, pubAt }) {
    const e = el('div', 'cbox', parent, `<div class="av"></div><div class="tx"></div><div class="bt">Publicar</div>`); e.style.width = w + 'px'; put(e, x, y);
    const tx = e.querySelector('.tx'), bt = e.querySelector('.bt'), a = popIn(e, t0, { from: .7 });
    const ts = t0 + .35; for (let i = 0; i < text.length; i++) cue(ts + i / cps, 'type', -4); cue(pubAt, 'click');
    on(t => { tf(e, a(t)); const n = Math.floor(clamp((t - ts) * cps, 0, text.length)), car = t < pubAt && Math.floor(t * 2.4) % 2 === 0;
      tx.innerHTML = text.slice(0, n) + (car || (n < text.length && t > ts) ? '<span class="caret" style="height:44px;vertical-align:-8px"></span>' : '');
      const pub = t >= pubAt; bt.className = 'bt' + (pub ? ' ok' : ''); bt.textContent = pub ? 'Publicado ✓' : 'Publicar';
      if (pub) { const k = prog(t, pubAt, .35); bt.style.transform = `scale(${mix(1.25, 1, Ease.outBack(k))})`; } });
    return e;
  }
  function dmToast(parent, { x, y, w = 780, label = 'RESPOSTA AUTOMÁTICA', html, t0 }) {
    const lb = el('div', 'dmlab', parent, label); put(lb, x - w / 2 + lb.offsetWidth / 2, y - 76);
    const e = el('div', 'dm', parent, html); e.style.width = w + 'px'; put(e, x, y); cue(t0 + .05, 'ding');
    on(t => { const k = prog(t, t0, .6), ex = Ease.outExpo(k); tf(e, { y: (1 - ex) * -50, o: clamp(k * 3), b: (1 - ex) * 14, s: mix(.92, 1, ex) });
      const kl = prog(t, t0 - .1, .4, Ease.outCubic); tf(lb, { o: kl, y: (1 - kl) * 10 }); });
    return e;
  }
  function glyph(parent, { x, y, text, t0, size = 64 }) {
    const e = el('div', 'mono', parent, text); e.style.cssText += `font-size:${size}px;color:rgba(240,128,42,.45);font-weight:500`; put(e, x, y);
    on(t => { const k = prog(t, t0, .6, Ease.outCubic); tf(e, { o: k, y: Math.sin(t * 1.6 + x) * 10 + (1 - k) * 20, b: (1 - k) * 8 }); });
    return e;
  }
  function underline(parent, { x, y, w = 170, t0 }) {
    const e = el('div', '', parent); Object.assign(e.style, { width: w + 'px', height: '8px', borderRadius: '4px', background: 'linear-gradient(90deg,#FF8E2E,#EA6511)' }); put(e, x, y);
    on(t => { const k = prog(t, t0, .5, Ease.outExpo); tf(e, { sx: Math.max(.001, k), o: k > 0 ? 1 : 0 }); }); return e;
  }

  /* ---------------- montagem / API ---------------- */
  function setup({ duration = 15, handle = '' } = {}) {
    DURATION = duration; HANDLE = handle;
    const frame = document.getElementById('frame'); background(frame, { handle });
    const cam = el('div', '', frame); cam.id = 'cam';
    on(t => { let dx = 0, dy = 0; shakes.forEach(s => { const u = t - s.t; if (u > 0 && u < s.dur) { const a = s.amp * Math.pow(1 - u / s.dur, 2);
      dx += Math.sin(u * 70) * a; dy += Math.cos(u * 55) * a * .7; } }); cam.style.transform = `translate(${dx}px,${dy}px)`; });
    return cam;
  }
  function seek(t) { for (const f of updaters) f(t); }
  function play() { const t0 = performance.now(); const loop = () => { seek(((performance.now() - t0) / 1000) % DURATION); requestAnimationFrame(loop); }; loop(); }

  window.KC = { W, H, CX, Ease, prog, mix, clamp, rng, on, cue, shake, cues, el, svg, put, tf, popIn,
    setup, scene, words, tile, pill, monoChip, connector, cardBurst, windowCard, codeTyper, statTile, areaChart,
    tag, captionCard, strikeLines, stamp, hubNetwork, commentBox, dmToast, glyph, underline, thumbHTML,
    seek, play, get duration() { return DURATION; } };
})();
