"""Generate public/index.html (FR) and public/en/index.html (EN) from src/template.html.

Usage:  python3 src/build.py
Every visible text lives in the FR / EN dictionaries below, so both languages stay in sync.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "src" / "template.html").read_text(encoding="utf-8")

PATCHES = "".join("<i></i>" for _ in range(36))

FR = {
    "lang": "fr", "base": "", "cv_file": "CV_Kebaily.pdf",
    "meta_title": "Chems Eddine Adel KEBAILY — Traitement du signal et des images",
    "meta_desc": "Portfolio de Chems Eddine Adel KEBAILY, étudiant en Master 1 Traitement du signal et des images à l'ULCO : machine learning, vision par ordinateur et développement logiciel.",
    "lang_label": "Langue",
    "lang_switch": '<span class="on">FR</span><a href="en/" hreflang="en" lang="en">EN</a>',
    "theme_label": "Changer de thème", "top_label": "Revenir en haut",
    "nav_ai": "Assistant IA", "nav_approach": "Démarche", "nav_projects": "Projets",
    "nav_journey": "Parcours", "nav_skills": "Compétences", "nav_contact": "Me contacter",

    "hero_status": "Ouvert aux opportunités de stage",
    "hero_h1_a": "Bonjour, je suis Chems.",
    "hero_h1_b": "Je donne du sens aux",
    "hero_word_1": "signaux",
    "hero_lead": "Étudiant en Master 1 Traitement du signal et des images à l'Université du Littoral Côte d'Opale. Je combine apprentissage automatique, vision par ordinateur et développement logiciel pour transformer des données brutes en outils utiles.",
    "hero_audience": 'Vous êtes <b class="c1">recruteur</b> ou <b class="c2">enseignant</b> ?',
    "hero_cta_ai": "Demander à CK-AI", "or": "ou", "hero_cta_cv": "Télécharger mon CV",
    "chip_tsi": "Traitement d'images",
    "stat_internships": "stages", "stat_projects": "projets IA", "stat_languages": "langues",

    "ai_pill": "Assistant IA", "ai_title_a": "Une question ? Demandez à",
    "ai_sub": "CK-AI répond à vos questions sur mon parcours, mes projets, mes compétences et ma disponibilité. Vous pouvez aussi coller une offre de stage pour voir si mon profil correspond.",
    "ai_role": "Assistant de Chems", "ai_online": "En ligne",
    "ai_welcome": "Bonjour ! Je suis CK-AI, l'assistant de Chems. Posez-moi une question sur son parcours, ses projets ou ses compétences — ou cliquez sur 📎 pour coller une offre de stage et je vous dirai si son profil correspond.",
    "ai_s1": "Quel est son parcours ?", "ai_s2": "Parle-moi de ses projets IA",
    "ai_s3": "Quelles sont ses compétences ?", "ai_s4": "Comment le contacter ?",
    "ai_offer_label": "Collez le texte de l'offre (stage, alternance…)",
    "ai_offer_ph": "Intitulé, missions, profil recherché…",
    "ai_cancel": "Annuler", "ai_offer_send": "Analyser l'offre", "ai_offer_btn": "Analyser une offre",
    "ai_placeholder": "Posez une question…", "ai_send": "Envoyer",
    "ai_note": "CK-AI peut se tromper : vérifiez les informations importantes avec Chems. Les messages ne sont pas conservés.",

    "ap_pill": "Démarche", "ap_title_a": "Du signal brut à la", "ap_title_b": "décision",
    "ap_sub": "Ma façon d'aborder un problème de traitement du signal ou de l'image.",
    "ap_text": "Chaque projet suit une chaîne complète : comprendre les données, les nettoyer, en extraire l'information utile, construire et évaluer un modèle, puis l'intégrer dans une application réelle.",
    "ap1_t": "Acquisition & compréhension", "ap1_d": "Comprendre le besoin, la source des données (signal, image, texte) et leurs limites.",
    "ap2_t": "Prétraitement & filtrage", "ap2_d": "Nettoyer, normaliser et filtrer les données pour réduire le bruit.",
    "ap3_t": "Extraction de caractéristiques", "ap3_d": "Transformer les données brutes en descripteurs exploitables par un modèle.",
    "ap4_t": "Modélisation", "ap4_d": "Comparer des modèles classiques et profonds (scikit-learn, PyTorch, ViT).",
    "ap5_t": "Évaluation", "ap5_d": "Mesurer les performances avec des métriques adaptées et analyser les erreurs.",
    "ap6_t": "Intégration", "ap6_d": "Intégrer le modèle dans une application web ou mobile (React, Spring Boot, Flutter).",
    "ap_cta": "Voir mes projets",

    "pr_pill": "Projets", "pr_title_a": "Projets", "pr_title_b": "académiques",
    "pr_sub": "Des projets d'apprentissage automatique et de vision par ordinateur, de la donnée au résultat.",
    "mock_legit": "légitime", "mock_phish": "phishing",
    "mock_patches": "Patchs 16×16", "mock_classes": "90 classes", "patches": PATCHES,
    "p1_title": "Détection de phishing par apprentissage automatique",
    "p1_ctx": "Projet de fin d'études de Licence · Recherche · 2025",
    "p1_desc": "Étude et comparaison de plusieurs modèles de classification pour distinguer les sites et URL de phishing des sites légitimes, avec extraction de caractéristiques et rédaction d'un rapport de recherche.",
    "p1_link": "Lire le rapport", "p1_short": "Détection de phishing",
    "tag_classification": "Classification", "tag_features": "Extraction de caractéristiques",
    "p2_title": "Reconnaissance d'animaux (90 espèces)",
    "p2_ctx": "Vision par ordinateur · Deep learning",
    "p2_desc": "Classification d'images multi-classe à l'aide d'un Vision Transformer (ViT) pré-entraîné et du transfer learning sous PyTorch, avec préparation des données et entraînement sur GPU.",
    "p2_link": "Voir le code", "p2_short": "Reconnaissance d'animaux",

    "jo_pill": "Parcours", "jo_title_a": "Formation &", "jo_title_b": "expérience",
    "jo_sub": "Un parcours entre l'Algérie et la France, de l'informatique au traitement du signal et des images.",
    "jo1_title": "Parcours académique", "jo1_desc": "Une base solide en systèmes informatiques, aujourd'hui spécialisée en traitement du signal et des images.",
    "edu1_t": "Master 1 Traitement du signal et des images", "edu1_s": "Université du Littoral Côte d'Opale (ULCO) · en cours",
    "edu2_t": "Licence Systèmes informatiques", "edu2_s": "Université M'Hamed Bougara de Boumerdès",
    "edu3_t": "Baccalauréat Techniques mathématiques, Génie civil", "edu3_s": "Lycée Ali Chekiri, Chéraga · mention Bien",
    "edu4_t": "Bootcamp « AI to Fullstack »", "edu4_s": "DevUp Club · mention Très bien", "edu4_d": "Févr. 2025",
    "jo2_title": "Expérience professionnelle", "jo2_desc": "Deux stages en entreprise dans le développement web et mobile, en équipe Agile.",
    "algeria": "Algérie",
    "ex1_t": "Stagiaire développement mobile", "ex1_d": "Déc. 2024 – Janv. 2025",
    "ex1_1": "Développement d'applications mobiles multiplateformes avec Flutter.",
    "ex1_2": "Participation à toutes les étapes du cycle de développement Agile.",
    "ex1_3": "Découverte du datacenter et du cloud hybride (GCP, on-premise).",
    "ex2_t": "Stagiaire développement web", "ex2_d": "Déc. 2023 – Janv. 2024",
    "ex2_1": "Application de gestion des flux de trésorerie des terminaux de paiement (POS).",
    "ex2_2": "Requêtes SQL, maintenance et optimisation de bases Oracle.",
    "ex2_3": "Tests unitaires, documentation technique, revues de code, Git.",
    "jo3_title": "Engagement associatif", "jo3_desc": "Un engagement actif dans le club d'informatique de mon université.",
    "cl1_t": "Co-manager du département Visual", "cl2_t": "Membre du département Développement",

    "sk_pill": "Compétences", "sk_title_a": "Ma", "sk_title_b": "boîte à outils",
    "sk_sub": "Les langages, frameworks et outils que j'utilise dans mes projets et mes stages.",
    "sk1": "IA & data", "sk2": "Langages", "sk3": "Développement", "sk4": "Systèmes & outils", "sk5": "Méthodes", "sk6": "Langues",
    "rest_api": "API REST", "code_reviews": "Revues de code", "unit_tests": "Tests unitaires", "tech_doc": "Documentation technique",
    "l_ar": "Arabe — natif", "l_fr": "Français — B2", "l_en": "Anglais — B2",
    "org_title": "Universités, entreprise et club qui ont marqué mon parcours",
    "org_uni": "Université", "org_company": "Entreprise", "org_club": "Club",

    "ct_kicker": "Restons en contact", "ct_title": "Discutons de votre projet de stage",
    "ct_sub": "Une offre de stage, un projet, une question ? Écrivez-moi, je vous réponds rapidement.",
    "f_name": "Nom complet", "f_name_ph": "Votre nom", "f_email": "Adresse e-mail",
    "f_company": "Entreprise (facultatif)", "f_company_ph": "Entreprise ou organisation",
    "f_subject": "Objet", "f_subject_ph": "En quelques mots", "f_message": "Message",
    "f_message_ph": "Présentez votre offre, votre projet ou votre question…", "f_send": "Envoyer le message",
    "ct_direct": "Ou contactez-moi directement",
    "footer_note": "Site conçu et développé par Chems avec l'aide de l'IA",
}

EN = {
    "lang": "en", "base": "../", "cv_file": "CV_Kebaily_EN.pdf",
    "meta_title": "Chems Eddine Adel KEBAILY — Signal and Image Processing",
    "meta_desc": "Portfolio of Chems Eddine Adel KEBAILY, Master's student in Signal and Image Processing at ULCO: machine learning, computer vision and software development.",
    "lang_label": "Language",
    "lang_switch": '<a href="../" hreflang="fr" lang="fr">FR</a><span class="on">EN</span>',
    "theme_label": "Toggle theme", "top_label": "Back to top",
    "nav_ai": "AI assistant", "nav_approach": "Approach", "nav_projects": "Projects",
    "nav_journey": "Journey", "nav_skills": "Skills", "nav_contact": "Contact me",

    "hero_status": "Open to internship opportunities",
    "hero_h1_a": "Hi, I'm Chems.",
    "hero_h1_b": "I make sense of",
    "hero_word_1": "signals",
    "hero_lead": "Master's student in Signal and Image Processing at the Université du Littoral Côte d'Opale. I combine machine learning, computer vision and software development to turn raw data into useful tools.",
    "hero_audience": 'Are you a <b class="c1">recruiter</b> or a <b class="c2">teacher</b>?',
    "hero_cta_ai": "Ask CK-AI", "or": "or", "hero_cta_cv": "Download my CV",
    "chip_tsi": "Image processing",
    "stat_internships": "internships", "stat_projects": "AI projects", "stat_languages": "languages",

    "ai_pill": "AI assistant", "ai_title_a": "Have a question? Ask",
    "ai_sub": "CK-AI answers questions about my background, projects, skills and availability. You can also paste an internship offer to see how well my profile matches.",
    "ai_role": "Chems's assistant", "ai_online": "Online",
    "ai_welcome": "Hi! I'm CK-AI, Chems's assistant. Ask me anything about his background, projects or skills — or click 📎 to paste an internship offer and I'll tell you how well his profile matches.",
    "ai_s1": "What is his background?", "ai_s2": "Tell me about his AI projects",
    "ai_s3": "What are his skills?", "ai_s4": "How can I contact him?",
    "ai_offer_label": "Paste the job or internship offer",
    "ai_offer_ph": "Title, responsibilities, required profile…",
    "ai_cancel": "Cancel", "ai_offer_send": "Analyse the offer", "ai_offer_btn": "Analyse an offer",
    "ai_placeholder": "Ask a question…", "ai_send": "Send",
    "ai_note": "CK-AI can make mistakes: check important details with Chems. Messages are not stored.",

    "ap_pill": "Approach", "ap_title_a": "From raw signal to", "ap_title_b": "decision",
    "ap_sub": "How I approach a signal or image processing problem.",
    "ap_text": "Every project follows a complete chain: understand the data, clean it, extract the useful information, build and evaluate a model, then integrate it into a real application.",
    "ap1_t": "Acquisition & understanding", "ap1_d": "Understand the need, the data source (signal, image, text) and its limits.",
    "ap2_t": "Pre-processing & filtering", "ap2_d": "Clean, normalise and filter the data to reduce noise.",
    "ap3_t": "Feature extraction", "ap3_d": "Turn raw data into descriptors a model can use.",
    "ap4_t": "Modelling", "ap4_d": "Compare classical and deep models (scikit-learn, PyTorch, ViT).",
    "ap5_t": "Evaluation", "ap5_d": "Measure performance with suitable metrics and analyse errors.",
    "ap6_t": "Integration", "ap6_d": "Integrate the model into a web or mobile app (React, Spring Boot, Flutter).",
    "ap_cta": "See my projects",

    "pr_pill": "Projects", "pr_title_a": "Academic", "pr_title_b": "projects",
    "pr_sub": "Machine learning and computer vision projects, from data to results.",
    "mock_legit": "legitimate", "mock_phish": "phishing",
    "mock_patches": "16×16 patches", "mock_classes": "90 classes", "patches": PATCHES,
    "p1_title": "Phishing detection with machine learning",
    "p1_ctx": "Bachelor's final project · Research · 2025",
    "p1_desc": "Study and comparison of several classification models to tell phishing websites and URLs apart from legitimate ones, with feature extraction and a research report.",
    "p1_link": "Read the report", "p1_short": "Phishing detection",
    "tag_classification": "Classification", "tag_features": "Feature extraction",
    "p2_title": "Animal recognition (90 species)",
    "p2_ctx": "Computer vision · Deep learning",
    "p2_desc": "Multi-class image classification with a pre-trained Vision Transformer (ViT) and transfer learning in PyTorch, including data preparation and GPU training.",
    "p2_link": "View the code", "p2_short": "Animal recognition",

    "jo_pill": "Journey", "jo_title_a": "Education &", "jo_title_b": "experience",
    "jo_sub": "A path between Algeria and France, from computer science to signal and image processing.",
    "jo1_title": "Education", "jo1_desc": "A solid foundation in computer systems, now specialising in signal and image processing.",
    "edu1_t": "Master's (M1) in Signal and Image Processing", "edu1_s": "Université du Littoral Côte d'Opale (ULCO) · ongoing",
    "edu2_t": "Bachelor's degree in Computer Systems", "edu2_s": "M'Hamed Bougara University of Boumerdès",
    "edu3_t": "Baccalaureate in Technical Mathematics, Civil Engineering", "edu3_s": "Ali Chekiri High School, Chéraga · with honours",
    "edu4_t": "“AI to Fullstack” Bootcamp", "edu4_s": "DevUp Club · grade: Very Good", "edu4_d": "Feb. 2025",
    "jo2_title": "Professional experience", "jo2_desc": "Two internships in web and mobile development, working in Agile teams.",
    "algeria": "Algeria",
    "ex1_t": "Mobile Development Intern", "ex1_d": "Dec. 2024 – Jan. 2025",
    "ex1_1": "Developed cross-platform mobile applications with Flutter.",
    "ex1_2": "Took part in every stage of the Agile development cycle.",
    "ex1_3": "Gained exposure to datacenters and hybrid cloud (GCP, on-premise).",
    "ex2_t": "Web Development Intern", "ex2_d": "Dec. 2023 – Jan. 2024",
    "ex2_1": "Cash-flow management application for point-of-sale (POS) terminals.",
    "ex2_2": "SQL queries, maintenance and optimisation of Oracle databases.",
    "ex2_3": "Unit tests, technical documentation, code reviews, Git.",
    "jo3_title": "Student involvement", "jo3_desc": "Active involvement in my university's computer science club.",
    "cl1_t": "Co-manager, Visual Department", "cl2_t": "Member, Development Department",

    "sk_pill": "Skills", "sk_title_a": "My", "sk_title_b": "toolbox",
    "sk_sub": "The languages, frameworks and tools I use in my projects and internships.",
    "sk1": "AI & data", "sk2": "Programming", "sk3": "Development", "sk4": "Systems & tools", "sk5": "Methods", "sk6": "Languages",
    "rest_api": "REST APIs", "code_reviews": "Code reviews", "unit_tests": "Unit testing", "tech_doc": "Technical documentation",
    "l_ar": "Arabic — native", "l_fr": "French — B2", "l_en": "English — B2",
    "org_title": "Universities, company and club that shaped my journey",
    "org_uni": "University", "org_company": "Company", "org_club": "Club",

    "ct_kicker": "Let's connect", "ct_title": "Let's talk about your internship",
    "ct_sub": "An internship offer, a project or a question? Write to me and I'll get back to you quickly.",
    "f_name": "Full name", "f_name_ph": "Your name", "f_email": "Email address",
    "f_company": "Company (optional)", "f_company_ph": "Company or organisation",
    "f_subject": "Subject", "f_subject_ph": "In a few words", "f_message": "Message",
    "f_message_ph": "Tell me about your offer, project or question…", "f_send": "Send message",
    "ct_direct": "Or reach me directly",
    "footer_note": "Site designed and built by Chems with the help of AI",
}

# Strings used by assets/app.js (chat, rotating words, form, offline answers)
JS = {
    "fr": {
        "words": ["signaux", "images", "données"],
        "online": "En ligne", "demo": "Mode démo",
        "typing": "CK-AI écrit…",
        "error": "Désolé, je n'ai pas pu répondre. Réessayez dans un instant ou écrivez directement à chemseddine.keb@gmail.com.",
        "offer_prefix": "Voici une offre. Analyse la correspondance avec le profil de Chems :\n\n",
        "offer_label": "📎 Offre collée", "chars": "caractères",
        "offer_demo": "L'analyse d'offre utilise l'IA, qui n'est pas encore activée sur ce site. En attendant, voici l'essentiel : Chems est étudiant en **Master 1 Traitement du signal et des images (ULCO)**, avec des projets en **machine learning** (scikit-learn) et **vision par ordinateur** (PyTorch, Vision Transformer), et deux stages en **développement web et mobile** (Spring Boot, React, Flutter). Pour un avis précis, contactez-le : chemseddine.keb@gmail.com.",
        "sent": "Merci ! Votre message a bien été envoyé. Je vous réponds rapidement.",
        "send_error": "L'envoi a échoué. Écrivez-moi directement à chemseddine.keb@gmail.com.",
        "faq": [
            [["parcours", "formation", "master", "étud", "licence", "ulco", "univers", "diplôme", "bac"],
             "Chems est en **Master 1 Traitement du signal et des images** à l'Université du Littoral Côte d'Opale (ULCO, 2026–2027). Avant cela, il a obtenu une **Licence en Systèmes informatiques** à l'Université de Boumerdès (2022–2025) et un Baccalauréat Techniques mathématiques (mention Bien, 2022)."],
            [["projet", "phishing", "animal", "vit", "transformer", "vision"],
             "Deux projets principaux :\n• **Détection de phishing** (PFE de Licence, 2025) : comparaison de modèles de classification avec Python et scikit-learn.\n• **Reconnaissance de 90 espèces animales** : Vision Transformer pré-entraîné et transfer learning sous PyTorch."],
            [["compét", "skill", "outil", "langage", "python", "techno", "framework", "stack"],
             "**IA & data** : PyTorch, TensorFlow, scikit-learn, Vision Transformer, transfer learning.\n**Langages** : Python, C, C++, Java, JavaScript, PHP, SQL.\n**Développement** : Spring Boot, React, Node.js, Flutter.\n**Méthodes** : Agile, revues de code, tests unitaires."],
            [["expérience", "stage", "ooredoo", "travail", "entreprise", "intern"],
             "Deux stages chez **Ooredoo Algérie** :\n• **Développement mobile** (déc. 2024 – janv. 2025) : applications Flutter, cycle Agile, cloud hybride.\n• **Développement web** (déc. 2023 – janv. 2024) : application de gestion de trésorerie POS avec Spring Boot et React, SQL/Oracle."],
            [["contact", "mail", "joindre", "téléphone", "linkedin", "écrire"],
             "Vous pouvez écrire à Chems à **chemseddine.keb@gmail.com**, le contacter sur LinkedIn (chemseddineadel-keb) ou utiliser le formulaire de contact en bas de la page."],
            [["langue", "anglais", "français", "arabe", "parle"],
             "Chems parle **arabe** (langue maternelle), **français** (B2) et **anglais** (B2)."],
            [["disponib", "alternance", "quand", "dispo", "recrut"],
             "Chems est ouvert aux **opportunités de stage** en traitement du signal, de l'image et en IA. Pour les dates précises, le mieux est de lui écrire : chemseddine.keb@gmail.com."],
        ],
        "default": "Je réponds aux questions sur le parcours, les projets, les compétences et les expériences de Chems. Essayez par exemple : « Quels sont ses projets IA ? » ou « Quelle est sa formation ? »",
    },
    "en": {
        "words": ["signals", "images", "data"],
        "online": "Online", "demo": "Demo mode",
        "typing": "CK-AI is typing…",
        "error": "Sorry, I couldn't answer. Please try again in a moment or email chemseddine.keb@gmail.com directly.",
        "offer_prefix": "Here is an offer. Analyse how well it matches Chems's profile:\n\n",
        "offer_label": "📎 Offer pasted", "chars": "characters",
        "offer_demo": "Offer analysis uses AI, which isn't enabled on this site yet. In short: Chems is a **Master's student in Signal and Image Processing (ULCO)**, with projects in **machine learning** (scikit-learn) and **computer vision** (PyTorch, Vision Transformer), and two internships in **web and mobile development** (Spring Boot, React, Flutter). For a precise answer, contact him: chemseddine.keb@gmail.com.",
        "sent": "Thank you! Your message has been sent. I'll get back to you soon.",
        "send_error": "Sending failed. Please email me directly at chemseddine.keb@gmail.com.",
        "faq": [
            [["background", "education", "master", "study", "studies", "degree", "bachelor", "ulco", "university"],
             "Chems is a **Master's (M1) student in Signal and Image Processing** at the Université du Littoral Côte d'Opale (ULCO, 2026–2027). Before that, he earned a **Bachelor's degree in Computer Systems** from the University of Boumerdès (2022–2025) and a Baccalaureate in Technical Mathematics (with honours, 2022)."],
            [["project", "phishing", "animal", "vit", "transformer", "vision"],
             "Two main projects:\n• **Phishing detection** (Bachelor's final project, 2025): comparison of classification models with Python and scikit-learn.\n• **Recognition of 90 animal species**: pre-trained Vision Transformer and transfer learning in PyTorch."],
            [["skill", "tool", "language", "python", "tech", "framework", "stack"],
             "**AI & data**: PyTorch, TensorFlow, scikit-learn, Vision Transformer, transfer learning.\n**Programming**: Python, C, C++, Java, JavaScript, PHP, SQL.\n**Development**: Spring Boot, React, Node.js, Flutter.\n**Methods**: Agile, code reviews, unit testing."],
            [["experience", "internship", "ooredoo", "work", "job", "company"],
             "Two internships at **Ooredoo Algeria**:\n• **Mobile development** (Dec. 2024 – Jan. 2025): Flutter apps, Agile cycle, hybrid cloud.\n• **Web development** (Dec. 2023 – Jan. 2024): POS cash-flow management app with Spring Boot and React, SQL/Oracle."],
            [["contact", "email", "mail", "reach", "phone", "linkedin"],
             "You can email Chems at **chemseddine.keb@gmail.com**, reach him on LinkedIn (chemseddineadel-keb), or use the contact form at the bottom of the page."],
            [["language", "english", "french", "arabic", "speak"],
             "Chems speaks **Arabic** (native), **French** (B2) and **English** (B2)."],
            [["available", "availability", "when", "hire", "recruit"],
             "Chems is open to **internship opportunities** in signal processing, image processing and AI. For exact dates, the best is to email him: chemseddine.keb@gmail.com."],
        ],
        "default": "I answer questions about Chems's background, projects, skills and experience. Try for example: “What are his AI projects?” or “What is his education?”",
    },
}

THANKS = {
    "fr": ("Merci !", "Votre message a bien été envoyé. Je vous réponds rapidement.", "Retour au site"),
    "en": ("Thank you!", "Your message has been sent. I'll get back to you soon.", "Back to the site"),
}


def render(texts: dict) -> str:
    values = dict(texts)
    values["i18n_json"] = json.dumps(JS[texts["lang"]], ensure_ascii=False).replace("</", "<\\/")
    out = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], TEMPLATE)
    leftover = re.findall(r"\{\{\w+\}\}", out)
    assert not leftover, f"missing keys: {leftover}"
    return out


def thanks_page(lang: str, base: str) -> str:
    title, text, back = THANKS[lang]
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Chems Eddine Adel KEBAILY</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="{base}assets/styles.css"></head>
<body class="thanks"><main class="thanks-box"><span class="brand-mark">CK</span><h1>{title}</h1><p>{text}</p>
<a class="btn btn-primary" href="./">{back}</a></main></body></html>
"""


def main() -> None:
    assert FR.keys() == EN.keys(), set(FR) ^ set(EN)
    pub = ROOT / "public"
    (pub / "en").mkdir(parents=True, exist_ok=True)
    (pub / "index.html").write_text(render(FR), encoding="utf-8")
    (pub / "en" / "index.html").write_text(render(EN), encoding="utf-8")
    (pub / "merci.html").write_text(thanks_page("fr", ""), encoding="utf-8")
    (pub / "en" / "merci.html").write_text(thanks_page("en", "../"), encoding="utf-8")
    print("built public/index.html, public/en/index.html and thank-you pages")


if __name__ == "__main__":
    main()
