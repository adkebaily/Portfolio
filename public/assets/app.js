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

  // ---------- Mot animé du titre ----------
  const word = $("#rotating");
  if (!reduceMotion) {
    let w = 0;
    setInterval(() => {
      word.classList.add("out");
      setTimeout(() => {
        w = (w + 1) % T.words.length;
        word.textContent = T.words[w];
        word.classList.remove("out");
      }, 350);
    }, 2600);
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
    const aud = Object.values(T.aud).find(a => a.q === q);
    if (aud) return aud;
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
  // « Recruteur » / « Enseignant » dans le titre : CK-AI répond selon le visiteur
  document.querySelectorAll(".aud").forEach(btn => btn.addEventListener("click", () => {
    $("#assistant").scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    setTimeout(() => ask(T.aud[btn.dataset.aud].q), reduceMotion ? 0 : 500);
  }));
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
