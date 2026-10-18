const root = document.documentElement;
root.classList.add("js");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// ---------- Thème clair / sombre (mémorisé dans le navigateur) ----------
try {
  const saved = localStorage.getItem("theme");
  if (saved) root.dataset.theme = saved;
} catch (e) {}

document.getElementById("themeToggle").addEventListener("click", () => {
  const isDark = root.dataset.theme
    ? root.dataset.theme === "dark"
    : window.matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = isDark ? "light" : "dark";
  try { localStorage.setItem("theme", root.dataset.theme); } catch (e) {}
});

// ---------- Menu mobile ----------
const links = document.getElementById("navLinks");
document.getElementById("menuBtn").addEventListener("click", () => links.classList.toggle("open"));
links.querySelectorAll("a").forEach(a => a.addEventListener("click", () => links.classList.remove("open")));

// ---------- Barre de progression, nav, bouton haut de page ----------
const nav = document.getElementById("nav");
const progress = document.getElementById("progress");
const toTop = document.getElementById("toTop");
function onScroll() {
  const max = document.documentElement.scrollHeight - innerHeight;
  progress.style.width = (max > 0 ? (scrollY / max) * 100 : 0) + "%";
  nav.classList.toggle("scrolled", scrollY > 10);
  toTop.classList.toggle("show", scrollY > 600);
}
addEventListener("scroll", onScroll, { passive: true });
onScroll();

// ---------- Apparition au défilement + compteurs ----------
function countUp(el) {
  const target = +el.dataset.count;
  if (reduceMotion) { el.textContent = target; return; }
  const start = performance.now(), dur = 1400;
  (function step(t) {
    const p = Math.min((t - start) / dur, 1);
    el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
    if (p < 1) requestAnimationFrame(step);
  })(start);
}

const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add("visible");
    e.target.querySelectorAll("[data-count]").forEach(countUp);
    revealObs.unobserve(e.target);
  });
}, { threshold: 0.12 });

document.querySelectorAll(".reveal").forEach((el, i) => {
  // léger décalage entre éléments voisins
  el.style.transitionDelay = (i % 4) * 80 + "ms";
  revealObs.observe(el);
});

// ---------- Lien actif dans le menu ----------
const navMap = new Map([...links.querySelectorAll("a")].map(a => [a.getAttribute("href").slice(1), a]));
const sectionObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    navMap.forEach(a => a.classList.remove("active"));
    const a = navMap.get(e.target.id);
    if (a) a.classList.add("active");
  });
}, { rootMargin: "-45% 0px -50% 0px" });
document.querySelectorAll("main section[id]").forEach(s => sectionObs.observe(s));

// ---------- Texte animé (machine à écrire) ----------
const roles = root.lang === "en" ? [
  "Signal and Image Processing",
  "Machine Learning & Deep Learning",
  "Computer Vision",
  "Software Development",
] : [
  "Traitement du signal et des images",
  "Machine Learning & Deep Learning",
  "Vision par ordinateur",
  "Développement logiciel",
];
const typed = document.getElementById("typed");
if (!reduceMotion) {
  let r = 0, c = roles[0].length, deleting = true;
  setTimeout(function tick() {
    const word = roles[r];
    c += deleting ? -1 : 1;
    typed.textContent = word.slice(0, c);
    let delay = deleting ? 35 : 65;
    if (!deleting && c === word.length) { deleting = true; delay = 2200; }
    else if (deleting && c === 0) { deleting = false; r = (r + 1) % roles.length; delay = 300; }
    setTimeout(tick, delay);
  }, 2600);
}

// ---------- Fond animé : ondes de signal ----------
const canvas = document.getElementById("signal");
const ctx = canvas.getContext("2d");
let w = 0, h = 0, dpr = 1;
function resize() {
  dpr = Math.min(devicePixelRatio || 1, 2);
  w = canvas.clientWidth; h = canvas.clientHeight;
  canvas.width = w * dpr; canvas.height = h * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}
addEventListener("resize", resize);
resize();

const waves = [
  { amp: 26, freq: 0.012, speed: 0.6, y: 0.72, width: 1.6 },
  { amp: 18, freq: 0.02, speed: -0.9, y: 0.78, width: 1.2 },
  { amp: 34, freq: 0.007, speed: 0.35, y: 0.84, width: 1 },
];
function draw(t) {
  ctx.clearRect(0, 0, w, h);
  ctx.strokeStyle = getComputedStyle(root).getPropertyValue("--wave").trim();
  waves.forEach(wv => {
    ctx.lineWidth = wv.width;
    ctx.beginPath();
    for (let x = 0; x <= w; x += 4) {
      const y = h * wv.y
        + Math.sin(x * wv.freq + t * 0.001 * wv.speed) * wv.amp
        + Math.sin(x * wv.freq * 2.3 + t * 0.0013 * wv.speed) * wv.amp * 0.35;
      x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.stroke();
  });
  if (!reduceMotion) requestAnimationFrame(draw);
}
requestAnimationFrame(draw);

document.getElementById("year").textContent = new Date().getFullYear();
