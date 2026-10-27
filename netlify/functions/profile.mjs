// Profil utilisé par CK-AI. Mettre à jour ce fichier en même temps que le CV.
// SUMMARY est toujours dans le prompt ; le détail des SECTIONS est lu par l'agent
// avec l'outil get_profile_section ; SKILLS sert à l'outil check_offer_requirements.

export const SUMMARY = `
Full name: Chems Eddine Adel Kebaily. Given names: Chems Eddine Adel. Family name: Kebaily. Refer to him as "Chems Eddine Adel".
Master's student (M1) in Signal and Image Processing at Université du Littoral Côte d'Opale (ULCO), Calais, France (2026–2027).
Moving into AI engineering: AI agents, generative AI and prompt engineering.
Internship search: available from 1 April 2027, for up to 5 months, in AI, AI engineering, machine learning, deep learning, AI agents, generative AI and prompt engineering, computer vision or NLP.
Background: Bachelor's in Computer Systems (Algeria), two internships at Ooredoo Algeria (web and mobile development), machine learning and computer vision projects.
`.trim();

export const SECTIONS = {
  education: `
- 2026–2027: Master 1 Traitement du signal et des images (Signal and Image Processing), ongoing, Université du Littoral Côte d'Opale (ULCO), France.
- 2022–2025: Licence (Bachelor's) in Computer Systems (Systèmes informatiques), Université M'Hamed Bougara de Boumerdès (UMBB), Algeria.
- 2022: Baccalauréat in Technical Mathematics, Civil Engineering, with honours (mention Bien), Lycée Ali Chekiri, Chéraga, Algeria.
- Feb. 2025: "AI to Fullstack" bootcamp, DevUp Club, University of Boumerdès, grade "Très bien" (Very Good).`,

  experience: `
- Dec. 2024 – Jan. 2025: Mobile development intern, Ooredoo Algeria. Cross-platform mobile apps with Flutter; every stage of the Agile cycle (requirements, development, testing, review); exposure to datacenter infrastructure and hybrid cloud (GCP and on-premise).
- Dec. 2023 – Jan. 2024: Web development intern, Ooredoo Algeria. Web application for managing cash flows of point-of-sale (POS) terminals with Spring Boot and React; SQL queries; maintenance and optimisation of Oracle databases; functional enhancements, unit tests, technical documentation (API, database schemas), code reviews and Git versioning.`,

  projects: `
- AI agent for administrative document processing (Agent IA de traitement de dossiers administratifs) — personal project, 2026. A citizen or a public-service agent (CAF, CROUS, mairie, préfecture) uploads scanned documents (tax notice, proof of address, bank details, school certificate…). Pipeline: image preprocessing with OpenCV (non-local means denoising, Sauvola local binarisation, small-speck removal, projection-profile deskewing), OCR with Tesseract (French), document classification and structured field extraction with an LLM (Claude API, JSON schema output, per-field confidence), deterministic business rules in Python (expired ID, proof of address older than 3 months, IBAN checksum, name consistency across documents), dossier completeness check against a checklist per procedure, and human validation of uncertain cases. Built with FastAPI, PostgreSQL, n8n orchestration (webhook, email approval), Docker Compose and a Streamlit dashboard. Evaluated on 40 synthetic labelled documents (no real personal data): 100% document classification accuracy, 97.6% field exact-match accuracy (F1 0.976), 10% of documents sent to human review; preprocessing reduces the OCR character error rate from 0.625 to 0.007 (about 90 times lower), and an ablation study showed the gain comes from denoising and local binarisation rather than deskewing. Code: https://github.com/adkebaily/agent-dossiers-administratifs
- CK-AI (2026): the AI assistant of his portfolio (this assistant). LLM-based agent on the Claude API with a written system prompt, tools (profile lookup, offer requirement checking, page actions such as navigation and contact-form drafting), input limits, rate limiting and prompt-injection guardrails, deployed as a serverless function on Netlify.
- Phishing detection with machine learning — Bachelor's final project (research), 2025. Dataset building, feature extraction, comparison of several classification models with Python and scikit-learn; evaluation (precision, recall, F1-score) and research report. Report: https://drive.google.com/file/d/1_rFw27PhBd6QnFyeZe5N6PHuoE_wE1JD/view
- Animal recognition (90 species) — computer vision. Multi-class image classification with a pre-trained Vision Transformer (ViT) and transfer learning in PyTorch; data preparation and augmentation, GPU training on Google Colab and Kaggle. Code: https://github.com/adkebaily/Animal-Recognition`,

  skills: `
- Generative AI & agents: AI agents, prompt engineering, generative AI, LLM APIs (Claude), structured outputs, tool use, n8n, human-in-the-loop validation, evaluation on labelled data.
- Image processing: OpenCV, Tesseract OCR, denoising, binarisation (Sauvola), deskewing.
- Backend & tools: FastAPI, PostgreSQL, Docker / Docker Compose, Streamlit.
- Machine learning & vision: PyTorch, TensorFlow, scikit-learn, Vision Transformer, transfer learning, classification, Kaggle, Google Colab.
- Programming languages: Python, C, C++, Java, JavaScript, PHP, SQL (Oracle), HTML/CSS.
- Development: Spring Boot, React, Node.js, Flutter, REST APIs.
- Systems & tools: Linux (Ubuntu), Windows Server, VirtualBox, Cisco Packet Tracer, Git/GitHub, VS Code, IntelliJ IDEA.
- Methods: Agile, code reviews, unit testing, technical documentation.
- Soft skills: organisation, communication, autonomy, adaptability, teamwork.`,

  languages: `Arabic (native), French (B2), English (B2).`,

  activities: `
- 2025–2026: Co-manager of the Visual Department, DevUp Club (computer science club), University of Boumerdès.
- 2024–2025: Member of the Development Department, DevUp Club.`,

  contact: `
Email: chemseddine.keb@gmail.com (preferred) · LinkedIn: linkedin.com/in/chemseddineadel-keb · GitHub: github.com/adkebaily · or the contact form on the website.
His phone number and street address are not shared on the website. Based in Calais, France. Driving licence B.
French and English CVs can be downloaded from the website. Internship: available from 1 April 2027, maximum duration 5 months (end of August 2027 at the latest). Fields: AI, AI engineering, machine learning, deep learning, AI agents, generative AI and prompt engineering, computer vision or NLP. Location preferences are not stated: suggest contacting him.`,
};

// Index utilisé pour comparer les exigences d'une offre au profil.
// terms : mots-clés reconnus (minuscules) ; evidence : preuve affichée.
export const SKILLS = [
  { skill: "Python", terms: ["python"], evidence: "Phishing detection (scikit-learn), animal recognition (PyTorch)" },
  { skill: "Machine learning", terms: ["machine learning", "apprentissage automatique", "ml", "classification", "scikit"], evidence: "Phishing detection project: comparison of classification models" },
  { skill: "Deep learning / PyTorch", terms: ["deep learning", "pytorch", "réseaux de neurones", "neural network"], evidence: "Animal recognition with a Vision Transformer in PyTorch" },
  { skill: "TensorFlow", terms: ["tensorflow", "keras"], evidence: "Listed in skills" },
  { skill: "Computer vision", terms: ["computer vision", "vision par ordinateur", "image", "vit", "transformer", "cnn"], evidence: "Animal recognition (90 species) with ViT; Master's in Signal and Image Processing" },
  { skill: "Image processing / OpenCV", terms: ["opencv", "image processing", "traitement d'image", "traitement des images", "binarisation", "denoising", "débruitage"], evidence: "Administrative document agent: OpenCV denoising, Sauvola binarisation, deskewing (OCR error divided by ~90)" },
  { skill: "OCR / document AI", terms: ["ocr", "tesseract", "document", "extraction", "idp"], evidence: "Administrative document agent: Tesseract OCR + LLM field extraction, 97.6% field accuracy on 40 labelled documents" },
  { skill: "n8n / workflow automation", terms: ["n8n", "workflow", "orchestration", "make", "zapier"], evidence: "Administrative document agent orchestrated with n8n (webhook, email approval)" },
  { skill: "FastAPI", terms: ["fastapi", "flask", "django", "backend"], evidence: "Administrative document agent API built with FastAPI" },
  { skill: "Docker", terms: ["docker", "container", "conteneur", "compose"], evidence: "Administrative document agent deployed with Docker Compose" },
  { skill: "PostgreSQL", terms: ["postgres", "postgresql"], evidence: "Administrative document agent stores dossiers in PostgreSQL" },
  { skill: "Evaluation / metrics", terms: ["evaluation", "évaluation", "metrics", "métriques", "benchmark", "f1"], evidence: "Labelled evaluation set and ablation study (document agent); precision/recall/F1 (phishing)" },
  { skill: "Signal processing", terms: ["signal", "traitement du signal"], evidence: "Master 1 Signal and Image Processing (ongoing, ULCO)" },
  { skill: "LLM / generative AI", terms: ["llm", "generative", "générative", "genai", "gpt", "claude", "large language"], evidence: "LLM field extraction with JSON schema output (document agent); CK-AI on the Claude API" },
  { skill: "AI agents", terms: ["agent", "agentic", "tool use", "function calling", "automation", "automatisation"], evidence: "Administrative document agent (OCR + LLM + business rules + human review); CK-AI with tools and page actions" },
  { skill: "Prompt engineering", terms: ["prompt"], evidence: "Wrote CK-AI's system prompt, tool descriptions and guardrails" },
  { skill: "Java / Spring Boot", terms: ["java", "spring"], evidence: "Web development internship at Ooredoo (Spring Boot)" },
  { skill: "JavaScript / React", terms: ["javascript", "react", "front", "frontend", "web"], evidence: "Web development internship at Ooredoo (React); this portfolio" },
  { skill: "HTML / CSS", terms: ["html", "css"], evidence: "Listed in skills; built this portfolio (HTML, CSS, JavaScript)" },
  { skill: "Degree level", terms: ["master", "bac+5", "bac +5", "bac+4", "m1", "m2", "ingénieur", "engineering degree", "étudiant", "student"], evidence: "Currently in Master 1 (first year of a two-year Master) in Signal and Image Processing, ULCO; Bachelor's in Computer Systems" },
  { skill: "Node.js", terms: ["node"], evidence: "CK-AI serverless function (Node.js); listed in skills" },
  { skill: "Flutter / mobile", terms: ["flutter", "mobile", "dart"], evidence: "Mobile development internship at Ooredoo (Flutter)" },
  { skill: "SQL / databases", terms: ["sql", "oracle", "database", "base de données", "bdd"], evidence: "SQL queries and Oracle database maintenance at Ooredoo" },
  { skill: "REST APIs", terms: ["api", "rest"], evidence: "Spring Boot web app at Ooredoo; CK-AI API" },
  { skill: "Cloud / serverless", terms: ["cloud", "gcp", "serverless", "netlify", "deploy", "déploiement"], evidence: "Exposure to hybrid cloud (GCP) at Ooredoo; CK-AI deployed serverless on Netlify" },
  { skill: "Git", terms: ["git", "github", "versioning"], evidence: "Git versioning and code reviews at Ooredoo" },
  { skill: "Linux", terms: ["linux", "ubuntu", "bash"], evidence: "Listed in skills" },
  { skill: "C / C++", terms: ["c++", "langage c"], evidence: "Listed in skills" },
  { skill: "Agile", terms: ["agile", "scrum"], evidence: "Agile cycle during the mobile internship at Ooredoo" },
  { skill: "Testing", terms: ["test", "unit"], evidence: "Unit tests during the web internship at Ooredoo" },
  { skill: "French", terms: ["french", "français", "francais"], evidence: "French B2" },
  { skill: "English", terms: ["english", "anglais"], evidence: "English B2" },
];
