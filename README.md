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
cv/                     ← sources LaTeX des CV (FR et EN)
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
