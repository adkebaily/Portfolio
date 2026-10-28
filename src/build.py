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

PATCHES = "".join("<i></i>" for _ in range(36))
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
    "meta_title": "Chems Eddine Adel Kebaily — Traitement du signal et des images",
    "meta_desc": "Portfolio de Chems Eddine Adel Kebaily, étudiant en Master 1 Traitement du signal et des images à l'ULCO : machine learning, vision par ordinateur et développement logiciel.",
    "lang_label": "Langue",
    "lang_switch": '<span class="on">FR</span><a href="en/" hreflang="en" lang="en">EN</a>',
    "theme_label": "Changer de thème", "skip": "Aller au contenu", "top_label": "Revenir en haut",
    "nav_ai": "Assistant IA", "nav_approach": "Démarche", "nav_projects": "Projets",
    "nav_journey": "Parcours", "nav_skills": "Compétences", "nav_contact": "Me contacter",

    "hero_status": "Disponible en stage dès le 1er avril 2027 · jusqu'à 5 mois",
    "hero_h1_a": "Bonjour, je suis Chems Eddine Adel.",
    "hero_h1_b": "Je conçois des",
    "hero_word_1": "agents IA",
    "hero_lead": "Étudiant en Master 1 Traitement du signal et des images à l'Université du Littoral Côte d'Opale, je m'oriente vers l'ingénierie IA : agents IA, IA générative et prompt engineering. J'associe ces outils au machine learning et au développement logiciel pour créer des solutions utiles.",
    "hero_audience": 'Vous êtes <button type="button" class="aud c1" data-aud="recruiter">recruteur</button> ou <button type="button" class="aud c2" data-aud="teacher">enseignant</button> ?',
    "hero_cta_ai": "Demander à CK-AI", "or": "ou", "hero_cta_cv": "Télécharger mon CV",
    "chip_tsi": "Agents IA",
    "stat_fields": "précision d'extraction", "stat_ocr": "moins d'erreurs OCR", "stat_tools": "stages en entreprise", "stat_link": "Voir le projet d'agent de dossiers administratifs",

    "ai_pill": "Assistant IA", "ai_title_a": "Une question ? Demandez à",
    "ai_sub": "CK-AI est un agent IA : il consulte mon profil, compare une offre de stage à mes compétences et agit sur la page pour vous (afficher un projet, proposer mon CV, préparer un message).",
    "ai_role": "Agent IA de Chems Eddine Adel", "ai_online": "En ligne",
    "ai_welcome": "Bonjour ! Je suis CK-AI, l'agent de Chems Eddine Adel. Je peux répondre sur son parcours, vous montrer ses projets, vous donner son CV ou préparer un message pour lui. Cliquez sur 📎 pour coller une offre de stage : je la compare à son profil.",
    "ai_s1": "Quel est son parcours ?", "ai_s2": "Parle-moi de ses projets IA",
    "ai_s3": "Montre-moi ses projets", "ai_s4": "Je veux lui proposer un stage",
    "ai_offer_label": "Collez le texte de l'offre (stage, alternance…)",
    "ai_offer_ph": "Intitulé, missions, profil recherché…",
    "ai_cancel": "Annuler", "ai_offer_send": "Analyser l'offre", "ai_offer_btn": "Analyser une offre",
    "ai_placeholder": "Posez une question…", "ai_send": "Envoyer",
    "ai_note": "CK-AI peut se tromper : vérifiez les informations importantes avec Chems Eddine Adel. Les messages ne sont pas conservés.",

    "ap_pill": "Démarche", "ap_title_a": "De l'idée à", "ap_title_b": "l'agent IA",
    "ap_sub": "Ma façon de concevoir une solution d'IA générative.",
    "ap_text": "Un agent IA utile ne se résume pas à un bon modèle : il faut un besoin clair, des prompts précis, le bon contexte, des outils bien choisis et une évaluation honnête. Exemple concret : CK-AI, l'assistant de ce site.",
    "ap1_t": "Comprendre le besoin", "ap1_d": "Définir le cas d'usage, les utilisateurs et ce qu'une bonne réponse doit contenir.",
    "ap2_t": "Prompt engineering", "ap2_d": "Rédiger des instructions claires, des exemples et des règles pour guider le modèle.",
    "ap3_t": "Données & contexte", "ap3_d": "Fournir au modèle les bonnes informations : documents, profil, base de connaissances.",
    "ap4_t": "Agents & outils", "ap4_d": "Connecter le modèle à des outils et des étapes pour qu'il agisse, pas seulement qu'il réponde.",
    "ap5_t": "Évaluation & garde-fous", "ap5_d": "Tester les réponses, limiter les erreurs et protéger contre les abus.",
    "ap6_t": "Intégration", "ap6_d": "Déployer la solution dans une application web ou mobile, via une API sécurisée.",
    "ap_cta": "Voir mes projets",

    "pr_pill": "Projets", "pr_title_a": "Mes", "pr_title_b": "projets",
    "pr_sub": "Deux agents IA, un projet de recherche en machine learning et un projet de vision par ordinateur, de la donnée au résultat mesuré.",
    "mock3_ok": "validé", "mock3_review": "revue humaine", "mock3_missing": "manquant",
    "p3_title": "Agent IA de traitement de dossiers administratifs",
    "p3_ctx": "Projet personnel · IA dans le service public · 2026",
    "p3_desc": "Un usager dépose ses pièces (avis d'imposition, justificatif de domicile, RIB…). L'agent nettoie l'image (débruitage, binarisation de Sauvola, redressement), la lit par OCR, identifie le document, extrait les champs avec un LLM et vérifie si le dossier est complet ; les cas incertains partent en validation humaine. Résultats sur 40 documents annotés : 100 % de classification, 97,6 % d'exactitude des champs, erreur OCR divisée par 90 grâce au prétraitement.",
    "p3_link": "Voir le code et les résultats", "p3_short": "Agent dossiers administratifs",
    "mock_legit": "légitime", "mock_phish": "phishing",
    "mock_patches": "Patchs 16×16", "mock_classes": "90 classes", "patches": PATCHES,
    "p4_title": "CK-AI — l'agent IA de ce portfolio",
    "p4_ctx": "Projet personnel · Agents IA · 2026",
    "p4_desc": "Agent conversationnel bilingue basé sur l'API Claude : il consulte mon profil avec des outils, compare une offre de stage à mes compétences et agit sur la page (afficher un projet, proposer mon CV, préparer un message). Garde-fous contre l'injection de prompt, limites de fréquence, déploiement serverless sur Netlify.",
    "p4_link": "L'essayer", "p4_short": "CK-AI (agent IA)",
    "mock_ag_q": "Voici notre offre de stage en IA générative…", "mock_ag_a": "Bonne correspondance : Python, LLM, agents. À préciser : Kubernetes. J'ai préparé un message pour lui.",
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
    "sk0": "IA générative & agents", "t_agents": "Agents IA", "t_genai": "IA générative", "t_llm_api": "API de LLM (Claude)", "sk1": "Machine learning & vision", "sk2": "Langages", "sk3": "Développement", "sk4": "Systèmes & outils", "sk5": "Méthodes", "sk6": "Langues",
    "rest_api": "API REST", "code_reviews": "Revues de code", "unit_tests": "Tests unitaires", "tech_doc": "Documentation technique",
    "l_ar": "Arabe — natif", "l_fr": "Français — B2", "l_en": "Anglais — B2",
    "org_title": "Universités, entreprise et club qui ont marqué mon parcours",
    "org_uni": "Université", "org_company": "Entreprise", "org_club": "Club",

    "ct_kicker": "Restons en contact", "ct_title": "Travaillons ensemble sur votre prochain projet IA",
    "ct_sub": "Un projet d'agent IA, une collaboration ou simplement une question ? Écrivez-moi, je serai ravi d'en discuter.",
    "f_name": "Nom complet", "f_name_ph": "Votre nom et prénom", "f_email": "Adresse e-mail", "f_email_ph": "nom@exemple.com",
    "f_org": "Entreprise ou école (facultatif)", "f_org_ph": "Entreprise, laboratoire ou université",
    "f_subject": "Objet", "f_subject_ph": "Stage, projet, collaboration…",
    "f_message": "Message", "f_message_ph": "Présentez votre offre, votre projet ou votre question. Ajoutez les détails utiles (missions, durée, outils…).",
    "f_send": "Envoyer le message", "ct_direct": "Ou contactez-moi directement",
    "footer_note": "Site conçu et développé par Chems Eddine Adel avec l'aide de l'IA",
}

EN = {
    "lang": "en", "base": "../", "cv_file": "CV_Kebaily_EN.pdf",
    "canonical": SITE + "/en/", "og_locale": "en_GB", "og_image": "og-en.jpg",
    "meta_title": "Chems Eddine Adel Kebaily — Signal and Image Processing",
    "meta_desc": "Portfolio of Chems Eddine Adel Kebaily, Master's student in Signal and Image Processing at ULCO: machine learning, computer vision and software development.",
    "lang_label": "Language",
    "lang_switch": '<a href="../" hreflang="fr" lang="fr">FR</a><span class="on">EN</span>',
    "theme_label": "Toggle theme", "skip": "Skip to content", "top_label": "Back to top",
    "nav_ai": "AI assistant", "nav_approach": "Approach", "nav_projects": "Projects",
    "nav_journey": "Journey", "nav_skills": "Skills", "nav_contact": "Contact me",

    "hero_status": "Available for an internship from 1 April 2027 · up to 5 months",
    "hero_h1_a": "Hi, I'm Chems Eddine Adel.",
    "hero_h1_b": "I design",
    "hero_word_1": "AI agents",
    "hero_lead": "Master's student in Signal and Image Processing at the Université du Littoral Côte d'Opale, moving into AI engineering: AI agents, generative AI and prompt engineering. I combine them with machine learning and software development to build useful solutions.",
    "hero_audience": 'Are you a <button type="button" class="aud c1" data-aud="recruiter">recruiter</button> or a <button type="button" class="aud c2" data-aud="teacher">teacher</button>?',
    "hero_cta_ai": "Ask CK-AI", "or": "or", "hero_cta_cv": "Download my CV",
    "chip_tsi": "AI Agents",
    "stat_fields": "extraction accuracy", "stat_ocr": "fewer OCR errors", "stat_tools": "industry internships", "stat_link": "See the administrative document agent project",

    "ai_pill": "AI assistant", "ai_title_a": "Have a question? Ask",
    "ai_sub": "CK-AI is an AI agent: it looks up my profile, compares an internship offer with my skills and acts on the page for you (show a project, offer my CV, draft a message).",
    "ai_role": "Chems Eddine Adel's AI agent", "ai_online": "Online",
    "ai_welcome": "Hi! I'm CK-AI, Chems Eddine Adel's agent. I can answer questions about his background, show you his projects, give you his CV or draft a message to him. Click 📎 to paste an internship offer: I'll compare it with his profile.",
    "ai_s1": "What is his background?", "ai_s2": "Tell me about his AI projects",
    "ai_s3": "Show me his projects", "ai_s4": "I want to offer him an internship",
    "ai_offer_label": "Paste the job or internship offer",
    "ai_offer_ph": "Title, responsibilities, required profile…",
    "ai_cancel": "Cancel", "ai_offer_send": "Analyse the offer", "ai_offer_btn": "Analyse an offer",
    "ai_placeholder": "Ask a question…", "ai_send": "Send",
    "ai_note": "CK-AI can make mistakes: check important details with Chems Eddine Adel. Messages are not stored.",

    "ap_pill": "Approach", "ap_title_a": "From idea to", "ap_title_b": "AI agent",
    "ap_sub": "How I design a generative AI solution.",
    "ap_text": "A useful AI agent is more than a good model: it needs a clear goal, precise prompts, the right context, well-chosen tools and honest evaluation. A real example: CK-AI, this site's assistant.",
    "ap1_t": "Understand the need", "ap1_d": "Define the use case, the users and what a good answer must contain.",
    "ap2_t": "Prompt engineering", "ap2_d": "Write clear instructions, examples and rules to guide the model.",
    "ap3_t": "Data & context", "ap3_d": "Give the model the right information: documents, profile, knowledge base.",
    "ap4_t": "Agents & tools", "ap4_d": "Connect the model to tools and steps so it can act, not just answer.",
    "ap5_t": "Evaluation & guardrails", "ap5_d": "Test the answers, reduce errors and protect against misuse.",
    "ap6_t": "Integration", "ap6_d": "Deploy the solution in a web or mobile app through a secure API.",
    "ap_cta": "See my projects",

    "pr_pill": "Projects", "pr_title_a": "My", "pr_title_b": "projects",
    "pr_sub": "Two AI agents, a machine learning research project and a computer vision project, from data to measured results.",
    "mock3_ok": "validated", "mock3_review": "human review", "mock3_missing": "missing",
    "p3_title": "AI agent for administrative document processing",
    "p3_ctx": "Personal project · AI in public services · 2026",
    "p3_desc": "A citizen uploads their documents (tax notice, proof of address, bank details…). The agent cleans the image (denoising, Sauvola binarisation, deskewing), reads it with OCR, identifies the document, extracts the fields with an LLM and checks whether the file is complete; uncertain cases go to human validation. Results on 40 labelled documents: 100% classification accuracy, 97.6% field accuracy, OCR error divided by 90 thanks to preprocessing.",
    "p3_link": "View the code and results", "p3_short": "Administrative document agent",
    "mock_legit": "legitimate", "mock_phish": "phishing",
    "mock_patches": "16×16 patches", "mock_classes": "90 classes", "patches": PATCHES,
    "p4_title": "CK-AI — this portfolio's AI agent",
    "p4_ctx": "Personal project · AI agents · 2026",
    "p4_desc": "Bilingual conversational agent on the Claude API: it looks up my profile with tools, compares an internship offer with my skills and acts on the page (show a project, offer my CV, draft a message). Guardrails against prompt injection, rate limits, serverless deployment on Netlify.",
    "p4_link": "Try it", "p4_short": "CK-AI (AI agent)",
    "mock_ag_q": "Here is our generative AI internship offer…", "mock_ag_a": "Good match: Python, LLMs, agents. To clarify: Kubernetes. I've drafted a message to him.",
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
    "sk0": "Generative AI & agents", "t_agents": "AI agents", "t_genai": "Generative AI", "t_llm_api": "LLM APIs (Claude)", "sk1": "Machine learning & vision", "sk2": "Programming", "sk3": "Development", "sk4": "Systems & tools", "sk5": "Methods", "sk6": "Languages",
    "rest_api": "REST APIs", "code_reviews": "Code reviews", "unit_tests": "Unit testing", "tech_doc": "Technical documentation",
    "l_ar": "Arabic — native", "l_fr": "French — B2", "l_en": "English — B2",
    "org_title": "Universities, company and club that shaped my journey",
    "org_uni": "University", "org_company": "Company", "org_club": "Club",

    "ct_kicker": "Let's connect", "ct_title": "Let's work together on your next AI project",
    "ct_sub": "An AI agent project, a collaboration or just a question? Write to me — I'd be glad to talk about it.",
    "f_name": "Full name", "f_name_ph": "Your full name", "f_email": "Email address", "f_email_ph": "name@example.com",
    "f_org": "Company or school (optional)", "f_org_ph": "Company, lab or university",
    "f_subject": "Subject", "f_subject_ph": "Internship, project, collaboration…",
    "f_message": "Message", "f_message_ph": "Tell me about your offer, project or question. Include useful details (tasks, duration, tools…).",
    "f_send": "Send message", "ct_direct": "Or reach me directly",
    "footer_note": "Site designed and built by Chems Eddine Adel with the help of AI",
}

# Strings used by assets/app.js (chat, rotating words, form, offline answers)
JS = {
    "fr": {
        "words": ["agents IA", "prompts", "solutions IA"],
        "steps_label": "Étapes de l'agent",
        "steps": {"get_profile_section": "🔎 Profil consulté", "check_offer_requirements": "📋 Offre comparée au profil", "show_section": "📍 Section affichée", "open_project": "🗂️ Projet ouvert", "offer_cv": "📄 CV proposé", "prefill_contact_form": "✉️ Message préparé"},
        "details": {"education": "formation", "experience": "expériences", "projects": "projets", "skills": "compétences", "languages": "langues", "activities": "activités", "contact": "contact", "assistant": "assistant", "demarche": "démarche", "projets": "projets", "parcours": "parcours", "competences": "compétences", "documents": "agent dossiers administratifs", "ckai": "CK-AI", "phishing": "détection de phishing", "animals": "reconnaissance d'animaux", "fr": "français", "en": "anglais"},
        "prefilled": "✍️ CK-AI a préparé un brouillon : vérifiez-le, modifiez-le si besoin, puis envoyez.",
        "cv_fr": "Télécharger le CV (français)", "cv_en": "Télécharger le CV (anglais)",

        "online": "En ligne", "demo": "Mode démo",
        "typing": "CK-AI écrit…",
        "error": "Désolé, je n'ai pas pu répondre. Réessayez dans un instant ou écrivez directement à chemseddine.keb@gmail.com.",
        "aud": {
            "recruiter": {"q": "Je suis recruteur : pourquoi Chems Eddine Adel pour un stage en IA ?",
                "reply": "Chems Eddine Adel cherche un **stage en IA dès le 1er avril 2027, jusqu'à 5 mois** : agents IA, IA générative, machine learning, vision ou NLP.\n\nCe qui peut vous intéresser :\n• **Agent de dossiers administratifs** : OCR et LLM, 97,6 % des champs extraits exacts sur 40 documents.\n• **CK-AI**, l'agent qui vous répond ici : API Claude et 6 outils.\n• **2 stages** de développement chez Ooredoo Algérie.\n\nJe vous ouvre son projet principal. Son CV est juste en dessous.",
                "actions": [{"type": "open_project", "project": "documents"}, {"type": "offer_cv", "language": "fr"}]},
            "teacher": {"q": "Je suis enseignant : quels sont ses travaux de recherche et ses projets ?",
                "reply": "Chems Eddine Adel est en **Master 1 Traitement du signal et des images** à l'ULCO. Ses travaux :\n• **Détection de phishing** (projet de fin d'études de Licence) : plusieurs modèles de classification comparés, avec rapport.\n• **Vision Transformer** : 90 espèces d'animaux reconnues par transfer learning.\n• **Agent de dossiers administratifs** : prétraitement d'image (débruitage, binarisation de Sauvola), OCR et LLM.\n\nJe vous ouvre le projet phishing et son rapport.",
                "actions": [{"type": "open_project", "project": "phishing"}]}
        },
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
        "words": ["AI agents", "prompts", "AI solutions"],
        "steps_label": "Agent steps",
        "steps": {"get_profile_section": "🔎 Profile checked", "check_offer_requirements": "📋 Offer compared to profile", "show_section": "📍 Section shown", "open_project": "🗂️ Project opened", "offer_cv": "📄 CV offered", "prefill_contact_form": "✉️ Message drafted"},
        "details": {"education": "education", "experience": "experience", "projects": "projects", "skills": "skills", "languages": "languages", "activities": "activities", "contact": "contact", "assistant": "assistant", "demarche": "approach", "projets": "projects", "parcours": "journey", "competences": "skills", "documents": "administrative document agent", "ckai": "CK-AI", "phishing": "phishing detection", "animals": "animal recognition", "fr": "French", "en": "English"},
        "prefilled": "✍️ CK-AI drafted a message: review it, edit if needed, then send.",
        "cv_fr": "Download CV (French)", "cv_en": "Download CV (English)",

        "online": "Online", "demo": "Demo mode",
        "typing": "CK-AI is typing…",
        "error": "Sorry, I couldn't answer. Please try again in a moment or email chemseddine.keb@gmail.com directly.",
        "aud": {
            "recruiter": {"q": "I'm a recruiter: why Chems Eddine Adel for an AI internship?",
                "reply": "Chems Eddine Adel is looking for an **AI internship from 1 April 2027, up to 5 months**: AI agents, generative AI, machine learning, computer vision or NLP.\n\nWhat may interest you:\n• **Administrative document agent**: OCR and LLM, 97.6% of fields extracted correctly on 40 documents.\n• **CK-AI**, the agent answering you here: Claude API and 6 tools.\n• **2 internships** in software development at Ooredoo Algeria.\n\nI'm opening his main project. His CV is just below.",
                "actions": [{"type": "open_project", "project": "documents"}, {"type": "offer_cv", "language": "en"}]},
            "teacher": {"q": "I'm a teacher: what are his research work and projects?",
                "reply": "Chems Eddine Adel is a **Master's student in Signal and Image Processing** at ULCO. His work:\n• **Phishing detection** (Bachelor's final project): several classification models compared, with a report.\n• **Vision Transformer**: 90 animal species recognised with transfer learning.\n• **Administrative document agent**: image preprocessing (denoising, Sauvola binarisation), OCR and LLM.\n\nI'm opening the phishing project and its report.",
                "actions": [{"type": "open_project", "project": "phishing"}]}
        },
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
<link rel="stylesheet" href="{base}assets/styles.css"></head>
<body class="thanks"><main class="thanks-box"><span class="brand-mark">CK</span><h1>{title}</h1><p>{text}</p>
<a class="btn btn-primary" href="./">{back}</a></main></body></html>
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
<link rel="stylesheet" href="/assets/styles.css?v={asset_version()}"></head>
<body class="thanks"><main class="thanks-box"><span class="brand-mark">CK</span>
<h1>404</h1><p>Cette page n'existe pas.<br><span lang="en">This page doesn't exist.</span></p>
<p><a class="btn btn-primary" href="/">Accueil (FR)</a> <a class="btn btn-outline" href="/en/" lang="en">Home (EN)</a></p>
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
