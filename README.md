# Portfolio — Chems Eddine Adel KEBAILY

Site : https://chemseddine-kebaily.netlify.app (FR) · https://chemseddine-kebaily.netlify.app/en/ (EN)

## Structure

```
public/                 ← ce que Netlify publie
  index.html            ← page FR (générée)
  en/index.html         ← page EN (générée)
  merci.html            ← page après envoi du formulaire (FR + en/merci.html)
  assets/styles.css     ← design
  assets/app.js         ← animations, assistant CK-AI, formulaire
  assets/photo.jpg
  CV_Kebaily.pdf, CV_Kebaily_EN.pdf
src/
  template.html         ← structure commune des deux pages
  build.py              ← tous les textes FR / EN + génération des pages
netlify/functions/
  ask.mjs               ← assistant CK-AI (/api/ask), appelle l'API Claude
  profile.mjs           ← profil utilisé par l'assistant (à tenir à jour avec le CV)
cv/                     ← sources LaTeX des CV (FR et EN) + build.sh
```

## Modifier un texte

1. Modifier le texte dans `src/build.py` (dictionnaires `FR` et `EN`).
2. Lancer `python3 src/build.py` pour regénérer `public/index.html` et `public/en/index.html`.
3. Si l'information concerne le profil, mettre aussi à jour `netlify/functions/profile.mjs` et les CV.
4. Commit + push : Netlify redéploie automatiquement.

## Activer l'assistant IA (CK-AI)

Sans clé, l'assistant fonctionne en **mode démo** (réponses préparées, badge « Mode démo »).
Pour l'IA réelle :

1. Créer une clé API sur https://platform.claude.com (et fixer une limite de dépenses mensuelle).
2. Netlify → projet → **Project configuration → Environment variables** → ajouter
   `ANTHROPIC_API_KEY` = la clé.
3. Redéployer (Deploys → Trigger deploy).

Option : variable `CK_MODEL` pour changer de modèle (par défaut `claude-opus-5-5` ;
`claude-haiku-5-5` est beaucoup moins cher).

Protections incluses : la clé reste côté serveur, origine du site vérifiée,
20 questions max par visiteur / 10 min, taille des messages limitée, aucun message conservé.

## Formulaire de contact

Géré par **Netlify Forms** (gratuit, 100 messages/mois). À activer une fois :
Netlify → projet → **Forms** → *Enable form detection*, puis redéployer.
Pour recevoir les messages par e-mail : Forms → *Form notifications* → *Add notification* → *Email*.

## CV (FR et EN)

Sources : `cv/CV.tex` et `cv/CV_en.tex`. Compilation : `sh cv/build.sh`.

- **Version site** (sans téléphone ni adresse) → copiée dans `public/CV_Kebaily.pdf` et `public/CV_Kebaily_EN.pdf`.
- **Version complète** (avec téléphone et adresse) → `cv/out/`, jamais publiée.
  Elle n'est générée que si `cv/private.tex` existe (fichier ignoré par git) :

```latex
\newcommand{\cvaddress}{N° et rue, code postal Ville}
\newcommand{\cvphone}{\href{tel:+33...}{\faMobile\ +33 ...}}
```

## Carte de visite numérique (QR code)

Page privée servie par `netlify/functions/card.mjs` sur `/c/<CARD_TOKEN>` : seul le lien du QR code l'ouvre, toute autre adresse renvoie 404.
Le jeton et le numéro de téléphone ne sont **pas** dans le dépôt (public) :

1. Netlify → **Project configuration → Environment variables** → ajouter `CARD_TOKEN` (le jeton secret) et `CARD_PHONE` (ex. `+33 6 12 34 56 78`).
2. Redéployer (Deploys → Trigger deploy).
3. Modifier la carte : `card/template.html`, puis `python3 card/build.py`, commit + push.
4. Nouveau QR code : `python3 card/make_qr.py https://chemseddine-kebaily.netlify.app/c/<CARD_TOKEN>` (dossier `card/qr/`, ignoré par git).
   Changer `CARD_TOKEN` désactive l'ancien QR code.
