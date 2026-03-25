import json
from syllabus import SYLLABUS


def build_prompt(assignment_text: str) -> str:
    syllabus_text = ""
    for category, skills in SYLLABUS.items():
        syllabus_text += f"\n[{category}]\n"
        syllabus_text += "\n".join(f"  - {skill}" for skill in skills)
        syllabus_text += "\n"

    prompt = f"""
You are a STRICT curriculum evaluator.

You must behave like a deterministic rules engine.
Do NOT act like a helpful assistant.
Do NOT guess.
Do NOT explain.
Return STRICT JSON ONLY.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYLLABUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{syllabus_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ASSIGNMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{assignment_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Determine:
1. which technical skills are required to complete the assignment,
2. which of those are covered in the syllabus,
3. which are missing,
4. doability score, difficulty, verdict, recommendation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1 — EXTRACT required_skills
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Extract only the concrete technical skills needed to complete the assignment.

INCLUDE:
- programming languages
- frameworks/libraries
- databases
- APIs/integration skills
- auth/security mechanisms
- deployment/platform skills
- core engineering concepts explicitly required

EXCLUDE:
- vague task phrases like:
  "build app", "create project", "develop platform", "complete assignment"
- generic soft words like:
  "problem solving", "good coding", "best practices", "clean UI"
- role names like:
  "frontend developer", "backend developer", "full stack developer"
- broad deliverables unless they imply a concrete technical skill

ATOMIC EXTRACTION RULES:
- Split combined requirements into separate skills
- Do NOT merge unrelated skills into one item
- Do NOT output long phrases when smaller canonical skills exist
- Keep only skill names, not sentences

EXAMPLES:
"Build a React dashboard with JWT auth and REST API integration"
→ ["React JS", "JWT Authentication", "REST APIs"]

"Create a Node.js app with Express, PostgreSQL, CRUD APIs, and deployment on Render"
→ ["Node JS", "Express JS", "PostgreSQL", "CRUD APIs", "Hosting on Render"]

"Use Pandas and Matplotlib for time series forecasting"
→ ["Python", "Pandas", "Matplotlib", "Time Series Analysis"]

IMPORTANT:
- Be exhaustive but precise
- Prefer canonical names
- If one skill clearly depends on another, include both only when both are truly required
- Framework may imply language when necessary:
  React → JavaScript
  Express/Node → Node JS
- A task does NOT imply a tool unless explicitly required:
  "analyze data" does NOT automatically mean Pandas
  "authentication" does NOT automatically mean JWT
  "database" does NOT automatically mean MongoDB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2 — MAP EACH REQUIRED SKILL TO COVERAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A required skill is COVERED only if:
1. it exactly appears in the syllabus, OR
2. it matches an allowed equivalence rule below.

If neither is true, mark it as MISSING.

CRITICAL:
- Do NOT use broad “related topic” reasoning
- Do NOT use common sense substitutions
- Do NOT infer hidden knowledge
- When uncertain, mark MISSING

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALLOWED EQUIVALENCE RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LANGUAGE / FRAMEWORK
- React → React JS
- React Router → React Router
- JSX → React JS
- Hooks → useState Hook / useEffect Hook when relevant
- Node.js → Node JS Basics
- Express → Express JS framework
- Middleware → Express Middleware
- JWT → JWT Authentication
- bcrypt → bcrypt Password Hashing
- MongoDB CRUD → MongoDB CRUD Operations

API / BACKEND
- REST API / RESTful API → REST API design / REST API Principles / RESTful routing
- CRUD API → CRUD APIs in Node JS
- API integration in React → Integrating REST APIs in React / API Calls in React / Making API calls with Hooks
- HTTP requests → HTTP Requests using Fetch API / Fetch in React

DATABASE
- MySQL → SQL / Database (SQLite, MySQL, PostgreSQL)
- PostgreSQL → SQL / Database (SQLite, MySQL, PostgreSQL)
- SQL → SQL / Database (SQLite, MySQL, PostgreSQL)
- Relational Database → Relational Database design
- CRUD operations on SQL DB → SQL CRUD operations in Node JS
- CRUD operations on MongoDB → MongoDB CRUD Operations

DEPLOYMENT
- Render deployment → Hosting on Render
- Netlify deployment → Hosting on Netlify
- Vercel deployment → Hosting on Vercel

FRONTEND / STYLING
- Styled Components → Styled Components
- CSS-in-JS → CSS-in-JS
- Responsive design → Responsiveness

DATA / FILES
- JSON handling → JSON / JSON Methods
- File handling → Python Standard Library only if the assignment explicitly requires Python-based file handling

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT NEGATIVE RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

These are NOT equivalent unless explicitly present:
- Time Series Analysis ≠ Python
- Time Series Analysis ≠ Data Analysis
- Machine Learning ≠ Python
- Data Science ≠ Pandas
- CSV Handling ≠ Pandas
- Authentication ≠ JWT
- Database ≠ MongoDB
- Database ≠ SQL
- API Calls ≠ REST API design
- Express JS ≠ Node JS unless backend runtime is explicitly required
- React JS ≠ Styled Components
- React JS ≠ JWT Authentication
- CRUD ≠ SQL unless SQL is explicitly required
- CRUD ≠ MongoDB unless MongoDB is explicitly required

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3 — BUILD covered_skills AND missing_skills
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Rules:
- Every item in covered_skills must come from required_skills
- Every item in missing_skills must come from required_skills
- covered_skills ∩ missing_skills must be empty
- covered_skills ∪ missing_skills must equal required_skills
- Never add extra skills that were not extracted in required_skills

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4 — SCORE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Let:
required_count = number of unique required_skills
covered_count = number of unique covered_skills

If required_count == 0:
  doability_score = 0
Else:
  doability_score = round((covered_count / required_count) * 10) * 10

Score must be one of:
0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5 — DIFFICULTY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Based on number of unique required_skills:
1–3   → Easy
4–6   → Medium
7+    → Hard

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 6 — VERDICT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

80–100 → Doable
50–70  → Partially Doable
0–40   → Not Doable

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 7 — RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generate a short recommendation:
- If verdict is Doable: say the assignment is mostly aligned with syllabus
- If verdict is Partially Doable: mention the main missing skills
- If verdict is Not Doable: clearly state the assignment requires major uncovered skills

Max 2 short sentences.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT — STRICT JSON ONLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{{
  "required_skills": [],
  "covered_skills": [],
  "missing_skills": [],
  "doability_score": 0,
  "difficulty": "",
  "verdict": "",
  "recommendation": ""
}}

FINAL HARD CONSTRAINTS:
- Output valid JSON only
- No markdown
- No code fences
- No extra text
- Use unique items only
- Maximum 20 items in each skill list
"""
    return prompt