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

  // ---------- Nav au défilement ----------
  const nav = $("#nav");
  const onScroll = () => nav.classList.toggle("scrolled", scrollY > 10);
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // ---------- Lien actif dans le menu ----------
  const navMap = new Map([...links.querySelectorAll("a")].map(a => [a.hash.slice(1), a]));
  const sectionObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      navMap.forEach(a => { a.classList.remove("active"); a.removeAttribute("aria-current"); });
      const a = navMap.get(e.target.id);
      if (a) { a.classList.add("active"); a.setAttribute("aria-current", "true"); }
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  document.querySelectorAll("main section[id]").forEach(s => sectionObs.observe(s));

  // ---------- Scan du nom : bruit, débruitage, binarisation, redressement ----------
  // Une seule animation au chargement, qui reprend les étapes réelles du pipeline documents.
  (() => {
    const sheet = $("#sheet"), canvas = $("#scan");
    if (!sheet || !canvas) return;
    const stages = [...document.querySelectorAll("#stages li")];
    const finish = () => { stages.forEach(s => s.classList.add("on")); sheet.classList.add("done"); };
    if (reduceMotion) return finish();

    const W = canvas.width, H = canvas.height;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    const off = document.createElement("canvas"); off.width = W; off.height = H;
    const o = off.getContext("2d");
    const draw = () => {
      const size = Math.round(W * 0.106);
      o.fillStyle = "#fff"; o.fillRect(0, 0, W, H);
      o.fillStyle = "#000"; o.textBaseline = "top";
      o.font = `800 ${size}px "Bricolage Grotesque", sans-serif`;
      o.fontVariationSettings = "'opsz' 96";
      o.fillText("Chems Eddine Adel", 0, W * 0.024);
      o.fillText("Kebaily", 0, W * 0.024 + size * 0.98);
      return o.getImageData(0, 0, W, H).data;
    };
    const isDark = () => root.dataset.theme
      ? root.dataset.theme === "dark"
      : matchMedia("(prefers-color-scheme: dark)").matches;

    document.fonts.ready.then(() => {
      const clean = draw();
      const noise = new Float32Array(W * H).map(() => (Math.random() - 0.5) * 2);
      const speck = new Uint8Array(W * H).map(() => (Math.random() < 0.012 ? 1 : 0));
      const img = ctx.createImageData(W, H);
      const dark = isDark();
      const ink = dark ? [232, 238, 236] : [29, 43, 54], bg = dark ? [22, 33, 42] : [251, 252, 251];
      const tmp = document.createElement("canvas"); tmp.width = W; tmp.height = H;
      const tctx = tmp.getContext("2d");
      const DUR = Number(new URLSearchParams(location.search).get("dur")) || 2600;
      const start = performance.now();

      const frame = now => {
        const t = Math.min((now - start) / DUR, 1);
        const amp = 160 * Math.max(0, 1 - t / 0.55);      // le bruit diminue (débruitage)
        const binar = t > 0.55;                            // seuillage à partir de 55 %
        const skew = 0.035 * Math.max(0, 1 - t / 0.75);    // redressement progressif
        stages.forEach((s, i) => s.classList.toggle("on", t >= [0, 0.2, 0.55, 0.9][i]));

        const d = img.data;
        for (let i = 0, p = 0; i < W * H; i++, p += 4) {
          let v = clean[p] + noise[i] * amp + (speck[i] && !binar ? -200 : 0) - (1 - t) * 30;
          if (binar) v = v > 128 ? 255 : 0;
          const k = Math.min(1, Math.max(0, v / 255));      // 0 = encre, 1 = papier
          d[p] = ink[0] + (bg[0] - ink[0]) * k;
          d[p + 1] = ink[1] + (bg[1] - ink[1]) * k;
          d[p + 2] = ink[2] + (bg[2] - ink[2]) * k;
          d[p + 3] = 255;
        }
        tctx.putImageData(img, 0, 0);
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.fillStyle = `rgb(${bg})`; ctx.fillRect(0, 0, W, H);
        ctx.setTransform(1, skew, 0, 1, 0, -skew * W * 0.3);
        ctx.drawImage(tmp, 0, 0);
        if (t < 1) requestAnimationFrame(frame); else setTimeout(finish, 250);
      };
      requestAnimationFrame(frame);
    });
  })();

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
    el.innerHTML = `<div class="bubble">${html}</div>`;
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
    flash(el.querySelector(".sec-head, .col-head") || el);
  };
  const openProject = name => {
    const el = document.getElementById("p-" + name);
    if (!el) return showSection("projets");
    el.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
    flash(el);
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
    const items = steps.map(s => {
      const label = T.steps[s.tool] || s.tool;
      const detail = s.detail !== "" && s.detail !== undefined ? ` · ${T.details[s.detail] || s.detail}` : "";
      return `<li>${escapeHtml(label + detail)}</li>`;
    }).join("");
    return `<ul class="agent-steps" aria-label="${T.steps_label}">${items}</ul>`;
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
    addMsg("bot", stepsHtml(result.steps) + format(result.reply) + extra);
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

  $("#year").textContent = new Date().getFullYear();
})();
