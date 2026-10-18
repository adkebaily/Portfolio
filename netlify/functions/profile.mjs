// Profil utilisé par CK-AI. Mettre à jour ce texte en même temps que le CV.
export const PROFILE = `
Full name: Chems Eddine Adel Kebaily. Given names (first names): Chems Eddine Adel. Family name: Kebaily. Refer to him as "Chems Eddine Adel".
Location: Calais, France
Status: Master's student (M1) in Signal and Image Processing (Traitement du signal et des images), Université du Littoral Côte d'Opale (ULCO), 2026–2027, ongoing. Open to internship opportunities in signal processing, image processing and AI. Exact availability dates: not stated — suggest contacting him.
Contact: chemseddine.keb@gmail.com (preferred) or the contact form on the website; his phone number is not shared on the website · LinkedIn: linkedin.com/in/chemseddineadel-keb · GitHub: github.com/adkebaily · Driving licence B
CVs: French and English CVs can be downloaded from the website.

Education:
- 2026–2027: Master 1 Traitement du signal et des images (ongoing), Université du Littoral Côte d'Opale (ULCO), France.
- 2022–2025: Licence (Bachelor's) in Computer Systems (Systèmes informatiques), Université M'Hamed Bougara de Boumerdès (UMBB), Algeria.
- 2022: Baccalauréat in Technical Mathematics, Civil Engineering, with honours (mention Bien), Lycée Ali Chekiri, Chéraga, Algeria.
- Feb. 2025: "AI to Fullstack" bootcamp, DevUp Club, University of Boumerdès, grade "Très bien" (Very Good).

Professional experience:
- Dec. 2024 – Jan. 2025: Mobile development intern, Ooredoo Algeria. Contributed to cross-platform mobile apps with Flutter; took part in every stage of the Agile development cycle (requirements, development, testing, review); exposure to datacenter infrastructure and hybrid cloud (GCP and on-premise).
- Dec. 2023 – Jan. 2024: Web development intern, Ooredoo Algeria. Developed a web application for managing cash flows of point-of-sale (POS) terminals with Spring Boot and React; SQL queries; maintenance and optimisation of Oracle databases; functional enhancements, unit tests, technical documentation (API, database schemas), code reviews and Git versioning.

Projects:
- AI agent for administrative document processing (Agent IA de traitement de dossiers administratifs) — personal project, 2026. A citizen or a public-service agent (CAF, CROUS, mairie, préfecture) uploads scanned documents (tax notice, proof of address, bank details, school certificate…). Pipeline: image preprocessing with OpenCV (non-local means denoising, Sauvola local binarisation, small-speck removal, projection-profile deskewing), OCR with Tesseract (French), document classification and structured field extraction with an LLM (Claude API, JSON schema output, per-field confidence), deterministic business rules in Python (expired ID, proof of address older than 3 months, IBAN checksum, name consistency across documents), dossier completeness check against a checklist per procedure, and human validation of uncertain cases. Built with FastAPI, PostgreSQL, n8n orchestration (webhook, email approval), Docker Compose and a Streamlit dashboard. Evaluated on 40 synthetic labelled documents (no real personal data): 100% document classification accuracy, 97.6% field exact-match accuracy (F1 0.976), 10% of documents sent to human review; preprocessing reduces the OCR character error rate from 0.625 to 0.007 (about 90 times lower), and an ablation study showed the gain comes from denoising and local binarisation rather than deskewing. Code: https://github.com/adkebaily/agent-dossiers-administratifs
- Phishing detection with machine learning — Bachelor's final project (research), 2025. Built a dataset, extracted features and compared several classification models with Python and scikit-learn; evaluated the models (precision, recall, F1-score) and wrote a research report. Report: https://drive.google.com/file/d/1_rFw27PhBd6QnFyeZe5N6PHuoE_wE1JD/view
- Animal recognition (90 species) — computer vision. Multi-class image classification with a pre-trained Vision Transformer (ViT) and transfer learning in PyTorch; data preparation and augmentation, GPU training on Google Colab and Kaggle, results analysis. Code: https://github.com/adkebaily/Animal-Recognition

Skills:
- AI agents & LLM: Claude API, structured outputs, n8n, FastAPI, prompt engineering, human-in-the-loop validation, evaluation on labelled data.
- Image processing: OpenCV, Tesseract OCR, denoising, binarisation (Sauvola), deskewing.
- Tools: Docker, PostgreSQL.
- AI & data: PyTorch, TensorFlow, scikit-learn, Vision Transformer, transfer learning, classification, Kaggle, Google Colab.
- Programming languages: Python, C, C++, Java, JavaScript, PHP, SQL (Oracle), HTML/CSS.
- Development: Spring Boot, React, Node.js, Flutter, REST APIs.
- Systems & networks: Linux (Ubuntu), Windows Server, VirtualBox, Cisco Packet Tracer.
- Tools & methods: Git/GitHub, VS Code, IntelliJ IDEA, WampServer, Photoshop; Agile, code reviews, unit testing, technical documentation.
- Soft skills: organisation, communication, autonomy, adaptability, teamwork.

Languages: Arabic (native), French (B2), English (B2).

Student involvement (DevUp Club, University of Boumerdès):
- 2025–2026: Co-manager of the Visual Department.
- 2024–2025: Member of the Development Department.

Current focus and career goal: AI engineering — AI agents, generative AI and prompt engineering (writing, testing and improving prompts; giving LLMs the right context; connecting them to tools). Looking for an internship in this field.
Example of his work in this field: CK-AI, the assistant on his portfolio website — an LLM-based agent (Claude API) with a written system prompt, his profile as context, input limits and guardrails, deployed as a serverless function on Netlify.
Interests: AI agents, computer vision, image processing.
`;
