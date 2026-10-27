"""Generate public/index.html (FR) and public/en/index.html (EN) from src/template.html.

Usage:  python3 src/build.py
Every visible text lives in the FR / EN dictionaries below, so both languages stay in sync.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "src" / "template.html").read_text(encoding="utf-8")

SITE = "https://chemseddine-kebaily.netlify.app"


def jsonld(lang: str) -> str:
    """Données structurées schema.org (Person + WebSite) pour les moteurs de recherche."""
    fr = lang == "fr"
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "@id": SITE + "/#person",
                "name": "Chems Eddine Adel Kebaily",
                "givenName": "Chems Eddine Adel",
                "familyName": "Kebaily",
                "jobTitle": "Étudiant en Master 1 Traitement du signal et des images" if fr else "Master's student in Signal and Image Processing",
                "description": "Ingénierie IA : agents IA, IA générative et prompt engineering." if fr else "AI engineering: AI agents, generative AI and prompt engineering.",
                "url": SITE + ("/" if fr else "/en/"),
                "image": SITE + "/assets/photo.jpg",
                "email": "mailto:chemseddine.keb@gmail.com",
                "address": {"@type": "PostalAddress", "addressLocality": "Calais", "addressCountry": "FR"},
                "affiliation": {"@type": "CollegeOrUniversity", "name": "Université du Littoral Côte d'Opale"},
                "alumniOf": {"@type": "CollegeOrUniversity", "name": "Université M'Hamed Bougara de Boumerdès"},
                "knowsAbout": ["AI agents", "Generative AI", "Prompt engineering", "Machine learning",
                               "Computer vision", "Signal processing", "Python", "PyTorch"],
                "knowsLanguage": ["ar", "fr", "en"],
                "sameAs": ["https://www.linkedin.com/in/chemseddineadel-keb", "https://github.com/adkebaily"],
            },
            {
                "@type": "WebSite",
                "@id": SITE + "/#website",
                "url": SITE + "/",
                "name": "Chems Eddine Adel Kebaily",
                "inLanguage": ["fr", "en"],
                "author": {"@id": SITE + "/#person"},
            },
        ],
    }
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

FR = {
    "lang": "fr", "base": "", "cv_file": "CV_Kebaily.pdf",
    "canonical": SITE + "/", "og_locale": "fr_FR", "og_image": "og-fr.jpg",
    "meta_title": "Chems Eddine Adel Kebaily — Ingénierie IA et agents IA",
    "meta_desc": "Portfolio de Chems Eddine Adel Kebaily, étudiant en Master 1 Traitement du signal et des images à l'ULCO : agents IA, IA générative, machine learning et vision par ordinateur. Stage dès le 1er avril 2027.",
    "lang_label": "Langue",
    "lang_switch": '<span class="on" aria-current="true">FR</span><a href="en/" hreflang="en" lang="en">EN</a>',
    "theme_label": "Changer de thème", "skip": "Aller au contenu", "menu_label": "Menu",
    "nav_ai": "Agent CK-AI", "nav_approach": "Démarche", "nav_projects": "Projets",
    "nav_journey": "Parcours", "nav_skills": "Compétences", "nav_contact": "Contact",

    "stage_1": "Scan bruité", "stage_2": "Débruitage", "stage_3": "Binarisation de Sauvola", "stage_4": "Texte reconnu",
    "photo_alt": "Photo de Chems Eddine Adel Kebaily",
    "avail": "Stage dès le 1er avril 2027, 5 mois maximum",
    "hero_lead": "Étudiant en <strong>Master 1 Traitement du signal et des images</strong> à l'Université du Littoral Côte d'Opale. Je construis des <strong>agents IA</strong> qui lisent, vérifient et comprennent des documents.",
    "fact_num": "90", "fact_text": "fois moins d'erreurs OCR grâce au prétraitement d'image, sur mon agent de dossiers administratifs",
    "hero_cta_ai": "Interroger mon agent", "hero_cta_cv": "Télécharger mon CV",
    "fields": "Domaines recherchés : IA, machine learning, deep learning, agents IA, IA générative et prompt engineering, vision par ordinateur, NLP.",

    "ai_title": "Posez vos questions à mon agent",
    "ai_sub": "CK-AI consulte mon profil, compare une offre de stage à mes compétences et agit sur cette page pour vous : il ouvre un projet, propose mon CV ou prépare un message.",
    "ai_role": "Agent IA de Chems Eddine Adel", "ai_online": "En ligne",
    "ai_welcome": "Bonjour ! Je suis CK-AI, l'agent de Chems Eddine Adel. Je peux répondre sur son parcours, vous montrer ses projets, vous donner son CV ou préparer un message pour lui. Cliquez sur le trombone pour coller une offre de stage : je la compare à son profil.",
    "ai_s1": "Quel est son parcours ?", "ai_s2": "Quand est-il disponible ?",
    "ai_s3": "Montre-moi ses projets", "ai_s4": "Je veux lui proposer un stage",
    "ai_offer_label": "Collez le texte de l'offre (stage, alternance…)",
    "ai_offer_ph": "Intitulé, missions, profil recherché…",
    "ai_cancel": "Annuler", "ai_offer_send": "Analyser l'offre", "ai_offer_btn": "Coller une offre de stage",
    "ai_placeholder": "Posez une question…", "ai_send": "Envoyer",
    "ai_note": "CK-AI peut se tromper : vérifiez les informations importantes avec Chems Eddine Adel. Les messages ne sont pas conservés.",

    "ap_title": "De l'idée à l'agent IA",
    "ap_sub": "Les six étapes que je suis pour concevoir une solution d'IA générative. CK-AI, l'agent de ce site, a été construit ainsi.",
    "ap1_t": "Comprendre le besoin", "ap1_d": "Définir le cas d'usage, les utilisateurs et ce qu'une bonne réponse doit contenir.",
    "ap2_t": "Écrire les prompts", "ap2_d": "Des instructions claires, des exemples et des règles pour guider le modèle.",
    "ap3_t": "Donner le contexte", "ap3_d": "Fournir au modèle les bonnes informations : documents, profil, base de connaissances.",
    "ap4_t": "Brancher les outils", "ap4_d": "Connecter le modèle à des outils pour qu'il agisse, pas seulement qu'il réponde.",
    "ap5_t": "Évaluer et protéger", "ap5_d": "Mesurer les réponses sur des données annotées, limiter les erreurs et les abus.",
    "ap6_t": "Intégrer", "ap6_d": "Déployer dans une application web ou mobile, via une API sécurisée.",

    "pr_title": "Projets, avec leurs résultats",
    "pr_sub": "Chaque projet est présenté par ce qu'il mesure.",
    "pd_metric": "97,6 %", "pd_metric_l": "des champs extraits exacts, sur 40 documents annotés",
    "pd_title": "Agent IA de traitement de dossiers administratifs", "pd_ctx": "Projet personnel, 2026",
    "pd_desc": "Un usager dépose ses pièces (avis d'imposition, justificatif de domicile, RIB…). L'agent nettoie l'image (débruitage, binarisation de Sauvola, redressement), la lit par OCR, identifie le document, extrait les champs avec un LLM et vérifie si le dossier est complet. Les cas incertains partent en validation humaine.",
    "pd_tools": "Python, OpenCV, Tesseract, LLM (Claude), FastAPI, PostgreSQL, n8n, Docker",
    "pd_link": "Code et résultats",
    "pc_metric": "6 outils", "pc_metric_l": "dont 4 actions sur cette page",
    "pc_title": "CK-AI, l'agent de ce portfolio", "pc_ctx": "Projet personnel, 2026",
    "pc_desc": "Agent conversationnel bilingue basé sur l'API Claude. Il consulte mon profil, compare une offre de stage à mes compétences et agit sur la page. Garde-fous contre l'injection de prompt, limites de fréquence, déploiement serverless.",
    "pc_tools": "API Claude, tool use, prompt engineering, Node.js, Netlify Functions",
    "pc_link": "L'essayer",
    "pp_metric": "F1", "pp_metric_l": "précision, rappel et F1-score comparés",
    "pp_title": "Détection de phishing par apprentissage automatique", "pp_ctx": "Projet de fin d'études de Licence, recherche, 2025",
    "pp_desc": "Comparaison de plusieurs modèles de classification pour distinguer les sites et URL de phishing des sites légitimes, avec extraction de caractéristiques et rapport de recherche.",
    "pp_tools": "Python, scikit-learn",
    "pp_link": "Lire le rapport",
    "pa_metric": "90", "pa_metric_l": "espèces reconnues",
    "pa_title": "Reconnaissance d'animaux par Vision Transformer", "pa_ctx": "Vision par ordinateur, deep learning",
    "pa_desc": "Classification d'images multi-classe avec un ViT pré-entraîné et du transfer learning, préparation des données et entraînement sur GPU.",
    "pa_tools": "PyTorch, Vision Transformer, Google Colab, Kaggle",
    "pa_link": "Voir le code",

    "jo_title": "Parcours",
    "jo_sub": "De l'informatique en Algérie au traitement du signal et des images en France.",
    "jo_edu": "Formation", "jo_exp": "Expériences", "jo_club": "Engagement associatif",
    "edu1_d": "2026–2027", "edu1_t": "Master 1 Traitement du signal et des images", "edu1_s": "Université du Littoral Côte d'Opale (ULCO), en cours",
    "edu2_d": "2022–2025", "edu2_t": "Licence Systèmes informatiques", "edu2_s": "Université M'Hamed Bougara de Boumerdès",
    "edu3_d": "2022", "edu3_t": "Baccalauréat Techniques mathématiques, Génie civil", "edu3_s": "Lycée Ali Chekiri, Chéraga, mention Bien",
    "edu4_d": "Févr. 2025", "edu4_t": "Bootcamp « AI to Fullstack »", "edu4_s": "DevUp Club, mention Très bien",
    "ex1_d": "Déc. 2024 – janv. 2025", "ex1_t": "Stagiaire développement mobile, Ooredoo Algérie",
    "ex1_s": "Applications multiplateformes avec Flutter, sur tout le cycle Agile ; découverte du datacenter et du cloud hybride (GCP, on-premise).",
    "ex2_d": "Déc. 2023 – janv. 2024", "ex2_t": "Stagiaire développement web, Ooredoo Algérie",
    "ex2_s": "Application de gestion de trésorerie des terminaux de paiement avec Spring Boot et React ; SQL et bases Oracle ; tests unitaires et documentation.",
    "cl1_d": "2025–2026", "cl1_t": "Co-manager du département Visual", "cl1_s": "DevUp Club, Université de Boumerdès",
    "cl2_d": "2024–2025", "cl2_t": "Membre du département Développement", "cl2_s": "DevUp Club, Université de Boumerdès",

    "sk_title": "Compétences",
    "sk_sub": "Les outils que j'ai réellement utilisés dans mes projets et mes stages.",
    "sk0": "IA générative et agents", "sk0_v": "Agents IA, prompt engineering, API de LLM (Claude), sorties structurées, tool use, n8n, validation humaine, évaluation sur données annotées",
    "sk1": "Machine learning et vision", "sk1_v": "PyTorch, TensorFlow, scikit-learn, Vision Transformer, transfer learning, OpenCV, Tesseract OCR",
    "sk2": "Langages", "sk2_v": "Python, C, C++, Java, JavaScript, PHP, SQL, HTML/CSS",
    "sk3": "Développement", "sk3_v": "FastAPI, Spring Boot, React, Node.js, Flutter, API REST, PostgreSQL, Docker",
    "sk4": "Outils et méthodes", "sk4_v": "Git/GitHub, Linux, Google Colab, Kaggle, Agile, revues de code, tests unitaires",
    "sk5": "Langues", "sk5_v": "Arabe (natif), français (B2), anglais (B2)",

    "ct_title": "Travaillons ensemble",
    "ct_sub": "Une offre de stage, un projet d'agent IA ou une question ? Écrivez-moi, je vous réponds rapidement.",
    "f_name": "Nom complet", "f_name_ph": "Votre nom et prénom", "f_email": "Adresse e-mail", "f_email_ph": "nom@exemple.com",
    "f_org": "Entreprise ou école (facultatif)", "f_org_ph": "Entreprise, laboratoire ou université",
    "f_subject": "Objet", "f_subject_ph": "Stage, projet, collaboration…",
    "f_message": "Message", "f_message_ph": "Présentez votre offre, votre projet ou votre question. Ajoutez les détails utiles (missions, durée, outils…).",
    "f_send": "Envoyer le message", "ct_direct": "Ou directement",
    "footer_note": "Site conçu et développé par Chems Eddine Adel avec l'aide de l'IA",
}

EN = {
    "lang": "en", "base": "../", "cv_file": "CV_Kebaily_EN.pdf",
    "canonical": SITE + "/en/", "og_locale": "en_GB", "og_image": "og-en.jpg",
    "meta_title": "Chems Eddine Adel Kebaily — AI engineering and AI agents",
    "meta_desc": "Portfolio of Chems Eddine Adel Kebaily, Master's student in Signal and Image Processing at ULCO: AI agents, generative AI, machine learning and computer vision. Internship from 1 April 2027.",
    "lang_label": "Language",
    "lang_switch": '<a href="../" hreflang="fr" lang="fr">FR</a><span class="on" aria-current="true">EN</span>',
    "theme_label": "Toggle theme", "skip": "Skip to content", "menu_label": "Menu",
    "nav_ai": "CK-AI agent", "nav_approach": "Approach", "nav_projects": "Projects",
    "nav_journey": "Journey", "nav_skills": "Skills", "nav_contact": "Contact",

    "stage_1": "Noisy scan", "stage_2": "Denoising", "stage_3": "Sauvola binarisation", "stage_4": "Recognised text",
    "photo_alt": "Photo of Chems Eddine Adel Kebaily",
    "avail": "Internship from 1 April 2027, up to 5 months",
    "hero_lead": "Master's student in <strong>Signal and Image Processing</strong> at the Université du Littoral Côte d'Opale. I build <strong>AI agents</strong> that read, check and understand documents.",
    "fact_num": "90", "fact_text": "times fewer OCR errors thanks to image preprocessing, in my administrative document agent",
    "hero_cta_ai": "Ask my agent", "hero_cta_cv": "Download my CV",
    "fields": "Fields: AI, machine learning, deep learning, AI agents, generative AI and prompt engineering, computer vision, NLP.",

    "ai_title": "Ask my agent",
    "ai_sub": "CK-AI looks up my profile, compares an internship offer with my skills and acts on this page for you: it opens a project, offers my CV or drafts a message.",
    "ai_role": "Chems Eddine Adel's AI agent", "ai_online": "Online",
    "ai_welcome": "Hi! I'm CK-AI, Chems Eddine Adel's agent. I can answer questions about his background, show you his projects, give you his CV or draft a message to him. Click the paperclip to paste an internship offer: I'll compare it with his profile.",
    "ai_s1": "What is his background?", "ai_s2": "When is he available?",
    "ai_s3": "Show me his projects", "ai_s4": "I want to offer him an internship",
    "ai_offer_label": "Paste the job or internship offer",
    "ai_offer_ph": "Title, responsibilities, required profile…",
    "ai_cancel": "Cancel", "ai_offer_send": "Analyse the offer", "ai_offer_btn": "Paste an internship offer",
    "ai_placeholder": "Ask a question…", "ai_send": "Send",
    "ai_note": "CK-AI can make mistakes: check important details with Chems Eddine Adel. Messages are not stored.",

    "ap_title": "From idea to AI agent",
    "ap_sub": "The six steps I follow to design a generative AI solution. CK-AI, this site's agent, was built this way.",
    "ap1_t": "Understand the need", "ap1_d": "Define the use case, the users and what a good answer must contain.",
    "ap2_t": "Write the prompts", "ap2_d": "Clear instructions, examples and rules to guide the model.",
    "ap3_t": "Provide context", "ap3_d": "Give the model the right information: documents, profile, knowledge base.",
    "ap4_t": "Connect tools", "ap4_d": "Connect the model to tools so it can act, not just answer.",
    "ap5_t": "Evaluate and protect", "ap5_d": "Measure answers on labelled data, reduce errors and misuse.",
    "ap6_t": "Integrate", "ap6_d": "Deploy in a web or mobile app through a secure API.",

    "pr_title": "Projects, with their results",
    "pr_sub": "Each project is presented by what it measures.",
    "pd_metric": "97.6%", "pd_metric_l": "of extracted fields correct, on 40 labelled documents",
    "pd_title": "AI agent for administrative document processing", "pd_ctx": "Personal project, 2026",
    "pd_desc": "A citizen uploads their documents (tax notice, proof of address, bank details…). The agent cleans the image (denoising, Sauvola binarisation, deskewing), reads it with OCR, identifies the document, extracts the fields with an LLM and checks whether the file is complete. Uncertain cases go to human validation.",
    "pd_tools": "Python, OpenCV, Tesseract, LLM (Claude), FastAPI, PostgreSQL, n8n, Docker",
    "pd_link": "Code and results",
    "pc_metric": "6 tools", "pc_metric_l": "including 4 actions on this page",
    "pc_title": "CK-AI, this portfolio's agent", "pc_ctx": "Personal project, 2026",
    "pc_desc": "Bilingual conversational agent on the Claude API. It looks up my profile, compares an internship offer with my skills and acts on the page. Guardrails against prompt injection, rate limits, serverless deployment.",
    "pc_tools": "Claude API, tool use, prompt engineering, Node.js, Netlify Functions",
    "pc_link": "Try it",
    "pp_metric": "F1", "pp_metric_l": "precision, recall and F1-score compared",
    "pp_title": "Phishing detection with machine learning", "pp_ctx": "Bachelor's final project, research, 2025",
    "pp_desc": "Comparison of several classification models to tell phishing websites and URLs apart from legitimate ones, with feature extraction and a research report.",
    "pp_tools": "Python, scikit-learn",
    "pp_link": "Read the report",
    "pa_metric": "90", "pa_metric_l": "species recognised",
    "pa_title": "Animal recognition with a Vision Transformer", "pa_ctx": "Computer vision, deep learning",
    "pa_desc": "Multi-class image classification with a pre-trained ViT and transfer learning, data preparation and GPU training.",
    "pa_tools": "PyTorch, Vision Transformer, Google Colab, Kaggle",
    "pa_link": "View the code",

    "jo_title": "Journey",
    "jo_sub": "From computer science in Algeria to signal and image processing in France.",
    "jo_edu": "Education", "jo_exp": "Experience", "jo_club": "Student involvement",
    "edu1_d": "2026–2027", "edu1_t": "Master's (M1) in Signal and Image Processing", "edu1_s": "Université du Littoral Côte d'Opale (ULCO), ongoing",
    "edu2_d": "2022–2025", "edu2_t": "Bachelor's degree in Computer Systems", "edu2_s": "M'Hamed Bougara University of Boumerdès",
    "edu3_d": "2022", "edu3_t": "Baccalaureate in Technical Mathematics, Civil Engineering", "edu3_s": "Ali Chekiri High School, Chéraga, with honours",
    "edu4_d": "Feb. 2025", "edu4_t": "“AI to Fullstack” Bootcamp", "edu4_s": "DevUp Club, grade: Very Good",
    "ex1_d": "Dec. 2024 – Jan. 2025", "ex1_t": "Mobile Development Intern, Ooredoo Algeria",
    "ex1_s": "Cross-platform apps with Flutter across the full Agile cycle; exposure to datacenters and hybrid cloud (GCP, on-premise).",
    "ex2_d": "Dec. 2023 – Jan. 2024", "ex2_t": "Web Development Intern, Ooredoo Algeria",
    "ex2_s": "Cash-flow management app for payment terminals with Spring Boot and React; SQL and Oracle databases; unit tests and documentation.",
    "cl1_d": "2025–2026", "cl1_t": "Co-manager, Visual Department", "cl1_s": "DevUp Club, University of Boumerdès",
    "cl2_d": "2024–2025", "cl2_t": "Member, Development Department", "cl2_s": "DevUp Club, University of Boumerdès",

    "sk_title": "Skills",
    "sk_sub": "Tools I have actually used in my projects and internships.",
    "sk0": "Generative AI and agents", "sk0_v": "AI agents, prompt engineering, LLM APIs (Claude), structured outputs, tool use, n8n, human-in-the-loop validation, evaluation on labelled data",
    "sk1": "Machine learning and vision", "sk1_v": "PyTorch, TensorFlow, scikit-learn, Vision Transformer, transfer learning, OpenCV, Tesseract OCR",
    "sk2": "Programming", "sk2_v": "Python, C, C++, Java, JavaScript, PHP, SQL, HTML/CSS",
    "sk3": "Development", "sk3_v": "FastAPI, Spring Boot, React, Node.js, Flutter, REST APIs, PostgreSQL, Docker",
    "sk4": "Tools and methods", "sk4_v": "Git/GitHub, Linux, Google Colab, Kaggle, Agile, code reviews, unit testing",
    "sk5": "Languages", "sk5_v": "Arabic (native), French (B2), English (B2)",

    "ct_title": "Let's work together",
    "ct_sub": "An internship offer, an AI agent project or a question? Write to me and I'll get back to you quickly.",
    "f_name": "Full name", "f_name_ph": "Your full name", "f_email": "Email address", "f_email_ph": "name@example.com",
    "f_org": "Company or school (optional)", "f_org_ph": "Company, lab or university",
    "f_subject": "Subject", "f_subject_ph": "Internship, project, collaboration…",
    "f_message": "Message", "f_message_ph": "Tell me about your offer, project or question. Include useful details (tasks, duration, tools…).",
    "f_send": "Send message", "ct_direct": "Or directly",
    "footer_note": "Site designed and built by Chems Eddine Adel with the help of AI",
}

# Strings used by assets/app.js (chat, rotating words, form, offline answers)
JS = {
    "fr": {
        "steps_label": "Étapes de l'agent",
        "steps": {"get_profile_section": "🔎 Profil consulté", "check_offer_requirements": "📋 Offre comparée au profil", "show_section": "📍 Section affichée", "open_project": "🗂️ Projet ouvert", "offer_cv": "📄 CV proposé", "prefill_contact_form": "✉️ Message préparé"},
        "details": {"education": "formation", "experience": "expériences", "projects": "projets", "skills": "compétences", "languages": "langues", "activities": "activités", "contact": "contact", "assistant": "assistant", "demarche": "démarche", "projets": "projets", "parcours": "parcours", "competences": "compétences", "documents": "agent dossiers administratifs", "ckai": "CK-AI", "phishing": "détection de phishing", "animals": "reconnaissance d'animaux", "fr": "français", "en": "anglais"},
        "prefilled": "✍️ CK-AI a préparé un brouillon : vérifiez-le, modifiez-le si besoin, puis envoyez.",
        "cv_fr": "Télécharger le CV (français)", "cv_en": "Télécharger le CV (anglais)",

        "online": "En ligne", "demo": "Mode démo",
        "typing": "CK-AI écrit…",
        "error": "Désolé, je n'ai pas pu répondre. Réessayez dans un instant ou écrivez directement à chemseddine.keb@gmail.com.",
        "offer_prefix": "Voici une offre. Analyse la correspondance avec le profil de Chems Eddine Adel :\n\n",
        "offer_label": "📎 Offre collée", "chars": "caractères",
        "offer_demo": "L'analyse d'offre utilise l'IA, qui n'est pas encore activée sur ce site. En attendant, voici l'essentiel : Chems Eddine Adel est étudiant en **Master 1 Traitement du signal et des images (ULCO)**, avec des projets en **machine learning** (scikit-learn) et **vision par ordinateur** (PyTorch, Vision Transformer), et deux stages en **développement web et mobile** (Spring Boot, React, Flutter). Pour un avis précis, contactez-le : chemseddine.keb@gmail.com.",
        "sent": "Merci ! Votre message a bien été envoyé. Je vous réponds rapidement.",
        "send_error": "L'envoi a échoué. Écrivez-moi directement à chemseddine.keb@gmail.com.",
        "faq": [
            [["offer him", "hire", "recruit", "propose"],
             "Happy to help! I've drafted a message in the contact form: add the details of your offer, then send it.",
             [{"type": "prefill_contact_form", "subject": "Internship offer", "message": "Hello Chems Eddine Adel,\n\nI'm reaching out about an internship in our team.\n\nTasks: \nDuration and dates: \nLocation: \n\nBest regards,", "organisation": ""}]],
            [["proposer", "recruter", "embaucher", "propose", "offre de stage pour"],
             "Avec plaisir ! J'ai préparé un brouillon de message dans le formulaire de contact : complétez-le avec les détails de votre offre, puis envoyez-le.",
             [{"type": "prefill_contact_form", "subject": "Proposition de stage", "message": "Bonjour Chems Eddine Adel,\n\nJe vous contacte au sujet d'un stage dans notre structure.\n\nMissions : \nDurée et dates : \nLieu : \n\nCordialement,", "organisation": ""}]],
            [["parcours", "formation", "master", "étud", "licence", "ulco", "univers", "diplôme", "bac"],
             "Chems Eddine Adel est en **Master 1 Traitement du signal et des images** à l'Université du Littoral Côte d'Opale (ULCO, 2026–2027). Avant cela, il a obtenu une **Licence en Systèmes informatiques** à l'Université de Boumerdès (2022–2025) et un Baccalauréat Techniques mathématiques (mention Bien, 2022).", [{"type": "show_section", "section": "parcours"}]],
            [["projet", "phishing", "animal", "vit", "transformer", "vision", "dossier", "administratif", "ocr", "n8n", "document", "ck-ai"],
             "Quatre projets principaux :\n• **Agent IA de traitement de dossiers administratifs** (2026) : prétraitement d'images (OpenCV), OCR, extraction des champs par LLM, contrôle de complétude et validation humaine ; 97,6 % d'exactitude des champs sur 40 documents annotés.\n• **CK-AI** (2026) : l'agent IA de ce portfolio, avec des outils et des actions sur la page.\n• **Détection de phishing** (PFE de Licence, 2025) : comparaison de modèles de classification avec Python et scikit-learn.\n• **Reconnaissance de 90 espèces animales** : Vision Transformer pré-entraîné et transfer learning sous PyTorch.", [{"type": "show_section", "section": "projets"}]],
            [["compét", "skill", "outil", "langage", "python", "techno", "framework", "stack"],
             "**IA & data** : PyTorch, TensorFlow, scikit-learn, Vision Transformer, transfer learning.\n**Langages** : Python, C, C++, Java, JavaScript, PHP, SQL.\n**Développement** : Spring Boot, React, Node.js, Flutter.\n**Méthodes** : Agile, revues de code, tests unitaires.", [{"type": "show_section", "section": "competences"}]],
            [["expérience", "stage", "ooredoo", "travail", "entreprise", "intern"],
             "Deux stages chez **Ooredoo Algérie** :\n• **Développement mobile** (déc. 2024 – janv. 2025) : applications Flutter, cycle Agile, cloud hybride.\n• **Développement web** (déc. 2023 – janv. 2024) : application de gestion de trésorerie POS avec Spring Boot et React, SQL/Oracle.", [{"type": "show_section", "section": "parcours"}]],
            [["contact", "mail", "joindre", "téléphone", "linkedin", "écrire"],
             "Vous pouvez écrire à Chems Eddine Adel à **chemseddine.keb@gmail.com**, le contacter sur LinkedIn (chemseddineadel-keb) ou utiliser le formulaire de contact en bas de la page.", [{"type": "show_section", "section": "contact"}]],
            [["cv", "curriculum", "télécharger", "pdf"],
             "Voici le CV de Chems Eddine Adel. Vous pouvez aussi le télécharger en anglais en haut de la page.", [{"type": "offer_cv", "language": "fr"}]],
            [["agent", "générative", "generative", "prompt", "llm", "ingénierie ia", "orientation", "spécialis"],
             "Chems Eddine Adel s'oriente vers l'**ingénierie IA** : **agents IA**, **IA générative** et **prompt engineering**. L'assistant CK-AI de ce site en est un exemple concret : un agent basé sur un LLM (Claude), avec des instructions précises, un profil comme contexte et des garde-fous. Il recherche un stage dans ce domaine."],
            [["langue", "anglais", "français", "arabe", "parle"],
             "Chems Eddine Adel parle **arabe** (langue maternelle), **français** (B2) et **anglais** (B2)."],
            [["disponib", "alternance", "quand", "dispo", "recrut", "date", "durée", "avril", "mois"],
             "Chems Eddine Adel recherche un **stage à partir du 1er avril 2027**, d'une durée de **5 mois maximum**, en IA, ingénierie IA, machine learning, deep learning, agents IA, IA générative et prompt engineering, vision par ordinateur ou NLP. Pour en discuter : chemseddine.keb@gmail.com ou le formulaire de contact.", [{"type": "offer_cv", "language": "fr"}]],
        ],
        "default": "Je réponds aux questions sur le parcours, les projets, les compétences et les expériences de Chems Eddine Adel. Essayez par exemple : « Quels sont ses projets IA ? » ou « Quelle est sa formation ? »",
    },
    "en": {
        "steps_label": "Agent steps",
        "steps": {"get_profile_section": "🔎 Profile checked", "check_offer_requirements": "📋 Offer compared to profile", "show_section": "📍 Section shown", "open_project": "🗂️ Project opened", "offer_cv": "📄 CV offered", "prefill_contact_form": "✉️ Message drafted"},
        "details": {"education": "education", "experience": "experience", "projects": "projects", "skills": "skills", "languages": "languages", "activities": "activities", "contact": "contact", "assistant": "assistant", "demarche": "approach", "projets": "projects", "parcours": "journey", "competences": "skills", "documents": "administrative document agent", "ckai": "CK-AI", "phishing": "phishing detection", "animals": "animal recognition", "fr": "French", "en": "English"},
        "prefilled": "✍️ CK-AI drafted a message: review it, edit if needed, then send.",
        "cv_fr": "Download CV (French)", "cv_en": "Download CV (English)",

        "online": "Online", "demo": "Demo mode",
        "typing": "CK-AI is typing…",
        "error": "Sorry, I couldn't answer. Please try again in a moment or email chemseddine.keb@gmail.com directly.",
        "offer_prefix": "Here is an offer. Analyse how well it matches Chems Eddine Adel's profile:\n\n",
        "offer_label": "📎 Offer pasted", "chars": "characters",
        "offer_demo": "Offer analysis uses AI, which isn't enabled on this site yet. In short: Chems Eddine Adel is a **Master's student in Signal and Image Processing (ULCO)**, with projects in **machine learning** (scikit-learn) and **computer vision** (PyTorch, Vision Transformer), and two internships in **web and mobile development** (Spring Boot, React, Flutter). For a precise answer, contact him: chemseddine.keb@gmail.com.",
        "sent": "Thank you! Your message has been sent. I'll get back to you soon.",
        "send_error": "Sending failed. Please email me directly at chemseddine.keb@gmail.com.",
        "faq": [
            [["background", "education", "master", "study", "studies", "degree", "bachelor", "ulco", "university"],
             "Chems Eddine Adel is a **Master's (M1) student in Signal and Image Processing** at the Université du Littoral Côte d'Opale (ULCO, 2026–2027). Before that, he earned a **Bachelor's degree in Computer Systems** from the University of Boumerdès (2022–2025) and a Baccalaureate in Technical Mathematics (with honours, 2022).", [{"type": "show_section", "section": "parcours"}]],
            [["project", "phishing", "animal", "vit", "transformer", "vision", "administrative", "document", "ocr", "n8n", "ck-ai"],
             "Four main projects:\n• **AI agent for administrative document processing** (2026): image preprocessing (OpenCV), OCR, LLM field extraction, completeness checks and human validation; 97.6% field accuracy on 40 labelled documents.\n• **CK-AI** (2026): this portfolio's AI agent, with tools and page actions.\n• **Phishing detection** (Bachelor's final project, 2025): comparison of classification models with Python and scikit-learn.\n• **Recognition of 90 animal species**: pre-trained Vision Transformer and transfer learning in PyTorch.", [{"type": "show_section", "section": "projets"}]],
            [["skill", "tool", "language", "python", "tech", "framework", "stack"],
             "**AI & data**: PyTorch, TensorFlow, scikit-learn, Vision Transformer, transfer learning.\n**Programming**: Python, C, C++, Java, JavaScript, PHP, SQL.\n**Development**: Spring Boot, React, Node.js, Flutter.\n**Methods**: Agile, code reviews, unit testing.", [{"type": "show_section", "section": "competences"}]],
            [["experience", "internship", "ooredoo", "work", "job", "company"],
             "Two internships at **Ooredoo Algeria**:\n• **Mobile development** (Dec. 2024 – Jan. 2025): Flutter apps, Agile cycle, hybrid cloud.\n• **Web development** (Dec. 2023 – Jan. 2024): POS cash-flow management app with Spring Boot and React, SQL/Oracle.", [{"type": "show_section", "section": "parcours"}]],
            [["contact", "email", "mail", "reach", "phone", "linkedin"],
             "You can email Chems Eddine Adel at **chemseddine.keb@gmail.com**, reach him on LinkedIn (chemseddineadel-keb), or use the contact form at the bottom of the page.", [{"type": "show_section", "section": "contact"}]],
            [["cv", "resume", "résumé", "download", "pdf"],
             "Here is Chems Eddine Adel's CV. A French version is also available.", [{"type": "offer_cv", "language": "en"}]],
            [["agent", "generative", "prompt", "llm", "ai engineering", "focus", "speciali"],
             "Chems Eddine Adel is moving into **AI engineering**: **AI agents**, **generative AI** and **prompt engineering**. This site's assistant, CK-AI, is a concrete example: an LLM-based agent (Claude) with precise instructions, his profile as context, and guardrails. He is looking for an internship in this field."],
            [["language", "english", "french", "arabic", "speak"],
             "Chems Eddine Adel speaks **Arabic** (native), **French** (B2) and **English** (B2)."],
            [["available", "availability", "when", "hire", "recruit", "date", "duration", "april", "months", "start"],
             "Chems Eddine Adel is looking for an **internship starting 1 April 2027**, lasting **up to 5 months**, in AI, AI engineering, machine learning, deep learning, AI agents, generative AI and prompt engineering, computer vision or NLP. To discuss it: chemseddine.keb@gmail.com or the contact form.", [{"type": "offer_cv", "language": "en"}]],
        ],
        "default": "I answer questions about Chems Eddine Adel's background, projects, skills and experience. Try for example: “What are his AI projects?” or “What is his education?”",
    },
}

THANKS = {
    "fr": ("Merci !", "Votre message a bien été envoyé. Je vous réponds rapidement.", "Retour au site"),
    "en": ("Thank you!", "Your message has been sent. I'll get back to you soon.", "Back to the site"),
}


def asset_version() -> str:
    h = hashlib.sha1()
    for name in ("styles.css", "app.js"):
        h.update((ROOT / "public" / "assets" / name).read_bytes())
    return h.hexdigest()[:10]


def render(texts: dict) -> str:
    values = dict(texts)
    values["version"] = asset_version()
    values["jsonld"] = jsonld(texts["lang"])
    values["i18n_json"] = json.dumps(JS[texts["lang"]], ensure_ascii=False).replace("</", "<\\/")
    out = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], TEMPLATE)
    leftover = re.findall(r"\{\{\w+\}\}", out)
    assert not leftover, f"missing keys: {leftover}"
    return out


def thanks_page(lang: str, base: str) -> str:
    title, text, back = THANKS[lang]
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Chems Eddine Adel Kebaily</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{base}assets/styles.css?v={asset_version()}"></head>
<body class="thanks"><main class="thanks-box"><span class="mark">CK<span></span></span><h1>{title}</h1><p>{text}</p>
<a class="btn btn-main" href="./">{back}</a></main></body></html>
"""


def seo_files(pub: Path) -> None:
    """robots.txt, sitemap.xml (avec hreflang) et page 404 bilingue."""
    from datetime import date
    today = date.today().isoformat()
    (pub / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nDisallow: /merci.html\nDisallow: /en/merci.html\n\nSitemap: {SITE}/sitemap.xml\n",
        encoding="utf-8")
    alts = (f'    <xhtml:link rel="alternate" hreflang="fr" href="{SITE}/"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/en/"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>\n')
    urls = "".join(f"  <url>\n    <loc>{SITE}{path}</loc>\n    <lastmod>{today}</lastmod>\n{alts}  </url>\n"
                   for path in ("/", "/en/"))
    (pub / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + urls + "</urlset>\n", encoding="utf-8")
    (pub / "404.html").write_text(f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page introuvable — Chems Eddine Adel Kebaily</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/styles.css?v={asset_version()}"></head>
<body class="thanks"><main class="thanks-box"><span class="mark">CK<span></span></span>
<h1>404</h1><p>Cette page n'existe pas.<br><span lang="en">This page doesn't exist.</span></p>
<p><a class="btn btn-main" href="/">Accueil (FR)</a> <a class="btn btn-alt" href="/en/" lang="en">Home (EN)</a></p>
</main></body></html>
""", encoding="utf-8")


def main() -> None:
    assert FR.keys() == EN.keys(), set(FR) ^ set(EN)
    pub = ROOT / "public"
    (pub / "en").mkdir(parents=True, exist_ok=True)
    (pub / "index.html").write_text(render(FR), encoding="utf-8")
    (pub / "en" / "index.html").write_text(render(EN), encoding="utf-8")
    (pub / "merci.html").write_text(thanks_page("fr", ""), encoding="utf-8")
    (pub / "en" / "merci.html").write_text(thanks_page("en", "../"), encoding="utf-8")
    seo_files(pub)
    print("built public/index.html, public/en/index.html, thank-you pages, 404, robots.txt and sitemap.xml")


if __name__ == "__main__":
    main()
