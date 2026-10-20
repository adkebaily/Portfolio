// Carte de visite numérique, accessible uniquement par le lien du QR code : /c/<CARD_TOKEN>.
// Le jeton et le numéro de téléphone sont lus dans les variables d'environnement Netlify
// (CARD_TOKEN, CARD_PHONE) et ne sont jamais dans le dépôt. Toute autre adresse renvoie 404.
import { timingSafeEqual } from "node:crypto";
import { PAGE } from "./card-page.mjs";

export const config = { path: "/c/:token" };

const PRIVATE_HEADERS = {
  "X-Robots-Tag": "noindex, nofollow, noarchive",
  "Cache-Control": "private, no-store",
  "Referrer-Policy": "no-referrer",
};

const notFound = () =>
  new Response("Not found", { status: 404, headers: { ...PRIVATE_HEADERS, "Content-Type": "text/plain; charset=utf-8" } });

const sameToken = (a, b) => {
  const x = Buffer.from(a), y = Buffer.from(b);
  return x.length === y.length && timingSafeEqual(x, y);
};

export default async (req, context) => {
  const token = process.env.CARD_TOKEN;
  const phone = process.env.CARD_PHONE;
  if (!token || !phone || !sameToken(context.params.token || "", token)) return notFound();

  // Les valeurs sont insérées dans des chaînes JS du modèle : JSON.stringify les échappe.
  const js = v => JSON.stringify(v).slice(1, -1);
  const html = PAGE
    .replace("__PHONE__", js(phone))
    .replace("__WHATSAPP__", js(phone.replace(/\D/g, "")));

  return new Response(html, { headers: { ...PRIVATE_HEADERS, "Content-Type": "text/html; charset=utf-8" } });
};
