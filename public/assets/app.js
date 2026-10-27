(() => {
  const root = document.documentElement;
  root.classList.add("js");
  const T = window.CK_I18N;
  const lang = document.body.dataset.lang;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (sel, el = document) => el.querySelector(sel);

  // ---------- Thème (mémorisé dans le navigateur) ----------
  try {
    const saved = localStorage.getItem("theme");
    if (saved) root.dataset.theme = saved;
  } catch (e) {}
  $("#themeToggle").addEventListener("click", () => {
    const isDark = root.dataset.theme
      ? root.dataset.theme === "dark"
      : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = isDark ? "light" : "dark";
    try { localStorage.setItem("theme", root.dataset.theme); } catch (e) {}
  });

  // ---------- Menu mobile ----------
  const links = $("#navLinks");
  const menuBtn = $("#menuBtn");
  menuBtn.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    menuBtn.setAttribute("aria-expanded", open);
  });
  links.querySelectorAll("a").forEach(a => a.addEventListener("click", () => links.classList.remove("open")));

  // ---------- Défilement : barre de progression, nav, bouton haut ----------
  const nav = $("#nav"), progress = $("#progress"), toTop = $("#toTop");
  const onScroll = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = (max > 0 ? (scrollY / max) * 100 : 0) + "%";
    nav.classList.toggle("scrolled", scrollY > 10);
    toTop.classList.toggle("show", scrollY > 700);
  };
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // ---------- Apparition au défilement + compteurs ----------
  const countUp = el => {
    const target = +el.dataset.count;
    if (reduceMotion) return;
    const start = performance.now();
    (function step(t) {
      const p = Math.min((t - start) / 1200, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    })(start);
  };
  const revealObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add("visible");
      e.target.querySelectorAll("[data-count]").forEach(countUp);
      revealObs.unobserve(e.target);
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach((el, i) => {
    el.style.transitionDelay = (i % 3) * 90 + "ms";
    revealObs.observe(el);
  });

  // ---------- Lien actif dans le menu ----------
  const navMap = new Map([...links.querySelectorAll("a")].map(a => [a.hash.slice(1), a]));
  const sectionObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      navMap.forEach(a => a.classList.remove("active"));
      navMap.get(e.target.id)?.classList.add("active");
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  document.querySelectorAll("main section[id]").forEach(s => sectionObs.observe(s));

  // ---------- Mot du titre : effacé puis réécrit jeton par jeton, comme un LLM ----------
  const word = $("#rotating");
  if (!reduceMotion) {
    let w = 0;
    word.classList.add("typing-on");
    const wait = ms => new Promise(r => setTimeout(r, ms));
    (async function loop() {
      for (;;) {
        await wait(2400);
        for (let t = word.textContent; t.length; t = t.slice(0, -1)) { word.textContent = t.slice(0, -1); await wait(38); }
        w = (w + 1) % T.words.length;
        const next = T.words[w];
        // découpe en petits « jetons » de 1 à 3 caractères
        for (let i = 0; i < next.length;) {
          i += 1 + Math.floor(Math.random() * 3);
          word.textContent = next.slice(0, i);
          await wait(70 + Math.random() * 60);
        }
      }
    })();
  }

  // ---------- Hero : réseau d'agents qui échangent des messages ----------
  (() => {
    const canvas = $("#net");
    if (!canvas || reduceMotion) return;
    const ctx = canvas.getContext("2d");
    const hero = canvas.parentElement;
    const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
    let W = 0, H = 0, nodes = [], packets = [], running = false, raf = 0;
    const mouse = { x: -1e4, y: -1e4 };
    let c1 = "79,70,229", c2 = "6,182,212";
    const readColors = () => {
      const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
      c1 = dark ? "129,140,248" : "79,70,229";
      c2 = dark ? "34,211,238" : "6,182,212";
    };
    const resize = () => {
      const dpr = Math.min(devicePixelRatio || 1, 2);
      W = hero.clientWidth; H = hero.clientHeight;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.min(70, Math.round(W * H / (fine ? 16000 : 26000)));
      nodes = Array.from({ length: n }, () => ({
        x: Math.random() * W, y: Math.random() * H,
        vx: (Math.random() - .5) * .25, vy: (Math.random() - .5) * .25, r: 1.2 + Math.random() * 1.8
      }));
      packets = [];
    };
    const LINK = 140;
    const frame = () => {
      ctx.clearRect(0, 0, W, H);
      for (const p of nodes) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > W) p.vx *= -1;
        if (p.y < 0 || p.y > H) p.vy *= -1;
      }
      // liens entre agents proches
      for (let i = 0; i < nodes.length; i++) {
        const a = nodes[i];
        for (let j = i + 1; j < nodes.length; j++) {
          const b = nodes[j], dx = a.x - b.x, dy = a.y - b.y, d = Math.hypot(dx, dy);
          if (d < LINK) {
            ctx.strokeStyle = `rgba(${c1},${(1 - d / LINK) * .22})`;
            ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
            if (packets.length < 14 && Math.random() < .0009) packets.push({ a, b, t: 0 });
          }
        }
        // le pointeur agit comme un agent « orchestrateur »
        const dm = Math.hypot(a.x - mouse.x, a.y - mouse.y);
        if (dm < 190) {
          ctx.strokeStyle = `rgba(${c2},${(1 - dm / 190) * .55})`;
          ctx.beginPath(); ctx.moveTo(mouse.x, mouse.y); ctx.lineTo(a.x, a.y); ctx.stroke();
        }
        ctx.fillStyle = dm < 190 ? `rgba(${c2},.9)` : `rgba(${c1},.55)`;
        ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2); ctx.fill();
      }
      // messages qui circulent le long des liens
      packets = packets.filter(k => (k.t += .018) < 1);
      for (const k of packets) {
        const x = k.a.x + (k.b.x - k.a.x) * k.t, y = k.a.y + (k.b.y - k.a.y) * k.t;
        ctx.fillStyle = `rgba(${c2},.95)`;
        ctx.shadowColor = `rgba(${c2},.9)`; ctx.shadowBlur = 8;
        ctx.beginPath(); ctx.arc(x, y, 2.2, 0, Math.PI * 2); ctx.fill();
        ctx.shadowBlur = 0;
      }
      raf = requestAnimationFrame(frame);
    };
    const start = () => { if (!running && !document.hidden) { running = true; raf = requestAnimationFrame(frame); } };
    const stop = () => { running = false; cancelAnimationFrame(raf); };
    readColors(); resize();
    new IntersectionObserver(([e]) => (e.isIntersecting ? start() : stop())).observe(hero);
    document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
    new MutationObserver(readColors).observe(root, { attributes: true, attributeFilter: ["data-theme"] });
    let rt; addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(resize, 150); });
    if (fine) {
      hero.addEventListener("pointermove", e => { const r = hero.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
      hero.addEventListener("pointerleave", () => { mouse.x = mouse.y = -1e4; });
    }
  })();

  // ---------- Inclinaison 3D de la photo et liseré lumineux des cartes ----------
  if (!reduceMotion && matchMedia("(hover: hover) and (pointer: fine)").matches) {
    const visual = $(".hero-visual");
    let tx = 0, ty = 0, cx = 0, cy = 0, tilting = false;
    const tilt = () => {
      cx += (tx - cx) * .1; cy += (ty - cy) * .1;
      visual.style.transform = `perspective(900px) rotateX(${cy}deg) rotateY(${cx}deg)`;
      if (Math.abs(tx - cx) > .01 || Math.abs(ty - cy) > .01) requestAnimationFrame(tilt); else tilting = false;
    };
    const hero = $(".hero");
    hero.addEventListener("pointermove", e => {
      if (visual.classList.contains("visible")) visual.style.transition = "opacity .8s";   // l'inclinaison suit sans retard
      const r = visual.getBoundingClientRect();
      tx = ((e.clientX - r.left) / r.width - .5) * 14;
      ty = -((e.clientY - r.top) / r.height - .5) * 14;
      if (!tilting) { tilting = true; requestAnimationFrame(tilt); }
    });
    hero.addEventListener("pointerleave", () => { tx = ty = 0; if (!tilting) { tilting = true; requestAnimationFrame(tilt); } });

    const spots = document.querySelectorAll(".step, .skill, .org, .j-block, .chat, .contact-form");
    spots.forEach(el => {
      el.classList.add("spot");
      el.addEventListener("pointermove", e => {
        const r = el.getBoundingClientRect();
        el.style.setProperty("--mx", `${e.clientX - r.left}px`);
        el.style.setProperty("--my", `${e.clientY - r.top}px`);
      });
    });
  }

  // ---------- Onglets des projets ----------
  const tabs = document.querySelectorAll(".tabs button");
  tabs.forEach(tab => tab.addEventListener("click", () => {
    const id = tab.dataset.tab;
    tabs.forEach(t => { t.classList.toggle("on", t === tab); t.setAttribute("aria-selected", t === tab); });
    document.querySelectorAll("[data-project]").forEach(el => { el.hidden = el.dataset.project !== id; });
  }));

  // ---------- Assistant CK-AI ----------
  const contact = $("#contactForm"), formStatus = $("#formStatus");
  const body = $("#chatBody"), form = $("#chatForm"), input = $("#chatInput");
  const sendBtn = form.querySelector(".send"), status = $("#chatStatus");
  const offerPanel = $("#offerPanel"), offerText = $("#offerText");
  const history = [];          // {role, content} envoyés à l'API
  let demo = false, busy = false;

  const escapeHtml = s => s.replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  // Mise en forme minimale : **gras**, retours à la ligne, adresses e-mail cliquables
  const format = s => escapeHtml(s)
    .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
    .replace(/([\w.+-]+@[\w-]+\.[\w.]+)/g, '<a href="mailto:$1">$1</a>')
    .split(/\n{2,}/).map(p => `<p>${p.replace(/\n/g, "<br>")}</p>`).join("");

  const addMsg = (who, html) => {
    const el = document.createElement("div");
    el.className = "msg " + who;
    el.innerHTML = (who === "bot" ? '<span class="avatar sm">CK</span>' : "") + `<div class="bubble">${html}</div>`;
    body.appendChild(el);
    body.scrollTop = body.scrollHeight;
    return el;
  };

  const setDemo = () => {
    if (demo) return;
    demo = true;
    status.classList.add("demo");
    status.querySelector("span").textContent = T.demo;
  };

  // ---------- Actions de l'agent sur la page ----------
  const flash = el => {
    el.classList.remove("flash");
    void el.offsetWidth;          // relance l'animation
    el.classList.add("flash");
  };
  const showSection = id => {
    const el = document.getElementById(id);
    if (!el) return;
    el.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    flash(el.querySelector(".section-head") || el);
  };
  const openProject = name => {
    const tab = document.querySelector(`.tabs button[data-tab="${({ documents: 2, ckai: 3, phishing: 0, animals: 1 })[name] ?? 0}"]`);
    if (tab) tab.click();
    showSection("projets");
  };
  const prefillContact = a => {
    contact.elements.objet.value = a.subject || "";
    contact.elements.message.value = a.message || "";
    if (a.organisation) contact.elements.organisation.value = a.organisation;
    formStatus.className = "form-status ok";
    formStatus.textContent = T.prefilled;
    showSection("contact");
    flash(contact);
  };
  // Exécute les actions renvoyées par l'agent ; renvoie le HTML à ajouter sous la réponse.
  const runActions = actions => {
    let extra = "";
    for (const a of actions || []) {
      if (a.type === "show_section") showSection(a.section);
      else if (a.type === "open_project") openProject(a.project);
      else if (a.type === "prefill_contact_form") prefillContact(a);
      else if (a.type === "offer_cv") {
        const file = a.language === "en" ? "CV_Kebaily_EN.pdf" : "CV_Kebaily.pdf";
        const base = lang === "en" ? "../" : "";
        extra += `<a class="chat-cta" href="${base}${file}" download>⬇ ${a.language === "en" ? T.cv_en : T.cv_fr}</a>`;
      }
    }
    return extra;
  };
  // Étapes de l'agent (outils utilisés), affichées au-dessus de la réponse
  const stepsHtml = steps => {
    if (!steps || !steps.length) return "";
    const items = steps.map((s, k) => {
      const label = T.steps[s.tool] || s.tool;
      const detail = s.detail !== "" && s.detail !== undefined ? ` · ${T.details[s.detail] || s.detail}` : "";
      return `<li style="--k:${k}">${escapeHtml(label + detail)}</li>`;
    }).join("");
    return `<ul class="agent-steps" aria-label="${T.steps_label}">${items}</ul>`;
  };

  // Fait apparaître la réponse mot par mot, après les étapes de l'agent
  const streamIn = (bubble, nSteps) => {
    const walker = document.createTreeWalker(bubble, NodeFilter.SHOW_TEXT);
    const texts = [];
    for (let n; (n = walker.nextNode());) if (!n.parentElement.closest(".agent-steps, .chat-cta") && n.data.trim()) texts.push(n);
    let k = 0;
    const words = texts.reduce((acc, n) => acc + n.data.split(/\s+/).length, 0);
    const step = Math.max(8, Math.min(28, 1400 / words));        // au plus ~1,4 s pour toute la réponse
    const offset = nSteps * 120 + 150;
    for (const n of texts) {
      const frag = document.createDocumentFragment();
      n.data.split(/(\s+)/).forEach(part => {
        if (!part) return;
        if (/^\s+$/.test(part)) return frag.append(part);
        const sp = document.createElement("span");
        sp.className = "tok"; sp.textContent = part;
        sp.style.animationDelay = `${offset + k++ * step}ms`;
        frag.append(sp);
      });
      n.replaceWith(frag);
    }
    const cta = bubble.querySelector(".chat-cta");
    if (cta) { cta.classList.add("tok"); cta.style.animationDelay = `${offset + k * step}ms`; }
    const scroll = () => { body.scrollTop = body.scrollHeight; };
    setTimeout(scroll, offset + k * step + 300);
  };

  // Réponses hors ligne, utilisées tant que l'IA n'est pas configurée sur Netlify
  const localAnswer = (q, isOffer) => {
    if (isOffer) return { reply: T.offer_demo, actions: [{ type: "show_section", section: "contact" }] };
    const text = q.toLowerCase();
    let best = null, bestScore = 0;
    for (const entry of T.faq) {
      const score = entry[0].filter(k => text.includes(k)).length;
      if (score > bestScore) { best = entry; bestScore = score; }
    }
    return best ? { reply: best[1], actions: best[2] || [] } : { reply: T.default, actions: [] };
  };

  const ask = async (question, shown, isOffer = false) => {
    if (busy || !question.trim()) return;
    busy = true; sendBtn.disabled = true;
    addMsg("user", shown ? escapeHtml(shown) : format(question));
    history.push({ role: "user", content: question });
    const typing = addMsg("bot typing", "<i></i><i></i><i></i>");

    let result = null;
    if (!demo) {
      try {
        const res = await fetch("/api/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ lang, messages: history.slice(-10) }),
        });
        if (res.ok) {
          result = await res.json();
        } else if (res.status === 429 || res.status === 413) {
          result = { reply: T.error };   // trop de questions ou message trop long
        } else {
          setDemo();          // fonction absente, clé API non configurée ou erreur serveur
        }
      } catch (e) {
        setDemo();            // hors ligne ou aperçu local
      }
    }
    if (result === null) {
      await new Promise(r => setTimeout(r, 500));
      result = localAnswer(question, isOffer);
    }

    typing.remove();
    const extra = runActions(result.actions);
    const msg = addMsg("bot", stepsHtml(result.steps) + format(result.reply) + extra);
    if (!reduceMotion) streamIn(msg.querySelector(".bubble"), (result.steps || []).length);
    history.push({ role: "assistant", content: result.reply });
    busy = false; sendBtn.disabled = false;
  };

  form.addEventListener("submit", e => {
    e.preventDefault();
    const q = input.value;
    input.value = "";
    ask(q);
  });
  $("#suggestions").addEventListener("click", e => {
    if (e.target.tagName === "BUTTON") ask(e.target.textContent);
  });
  $("#offerBtn").addEventListener("click", () => { offerPanel.hidden = !offerPanel.hidden; if (!offerPanel.hidden) offerText.focus(); });
  $("#offerCancel").addEventListener("click", () => { offerPanel.hidden = true; });
  $("#offerSend").addEventListener("click", () => {
    const offer = offerText.value.trim();
    if (!offer) return offerText.focus();
    offerPanel.hidden = true;
    offerText.value = "";
    ask(T.offer_prefix + offer, `${T.offer_label} (${offer.length} ${T.chars})`, true);
  });

  // ---------- Formulaire de contact (Netlify Forms) ----------
  contact.addEventListener("submit", async e => {
    e.preventDefault();
    const btn = contact.querySelector("button[type=submit]");
    btn.disabled = true;
    formStatus.className = "form-status";
    formStatus.textContent = "…";
    try {
      const res = await fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(new FormData(contact)).toString(),
      });
      if (!res.ok) throw new Error(res.status);
      contact.reset();
      formStatus.classList.add("ok");
      formStatus.textContent = T.sent;
    } catch (err) {
      formStatus.classList.add("err");
      formStatus.textContent = T.send_error;
    }
    btn.disabled = false;
  });

  // ---------- Bandeau défilant : contenu doublé pour une boucle continue ----------
  const track = $(".marquee-track");
  track.innerHTML += track.innerHTML;

  $("#year").textContent = new Date().getFullYear();
})();
