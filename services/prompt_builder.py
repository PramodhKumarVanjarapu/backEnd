import json
from syllabus import SYLLABUS


def build_prompt(assignment_text: str) -> str:

    # Build categorised syllabus block so the LLM sees groupings
    syllabus_text = ""
    for category, skills in SYLLABUS.items():
        syllabus_text += f"\n[{category}]\n"
        syllabus_text += "\n".join(f"  - {skill}" for skill in skills)
        syllabus_text += "\n"

    prompt = prompt = f"""
You are a STRICT curriculum evaluator. You must behave like a rule-based system — NOT an intelligent guesser.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYLLABUS — skills the student has learned:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{syllabus_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ASSIGNMENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{assignment_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1 — Extract required_skills
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Extract ALL high-level skills required.

IMPORTANT:
- Be exhaustive
- Do NOT merge different skills
- Use canonical names

Examples:
"Time Series Forecasting using Pandas and Matplotlib"
→ ["Python", "Pandas", "Matplotlib", "Time Series Analysis"]

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2 — Coverage Matching (CRITICAL)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STRICT RULES (NO EXCEPTIONS):

A skill is COVERED if:

1. Exact match exists in syllabus, OR
2. Same concept exists with different wording, OR
3. Clearly taught under a related topic

IMPORTANT:
- Normalize naming differences (Node.js vs Node JS)
- Treat synonyms as SAME skill
- Do NOT mark as missing if concept is clearly covered

❌ DO NOT:
- Assume
- Generalize
- Infer
- Use "common sense"

If not explicitly mapped → mark as MISSING

---

### ✅ EQUIVALENCE RULES (CUSTOM FOR THIS SYLLABUS)

#### DATA HANDLING
CSV / JSON Data Handling → covered by ["JavaScript Object Notation (JSON)", "HTTP Requests", "Fetch API"]
File Handling → covered by ["Python"]

#### DATABASE
MySQL / PostgreSQL → covered by ["SQL / Database"]
CRUD → covered by ["SQL Querying", "MongoDB CRUD"]

#### BACKEND
REST API → covered by ["REST APIs"]
API Calls → covered by ["Fetch", "HTTP"]

#### AUTH
JWT → covered by ["JWT"]
bcrypt → covered by ["bcrypt"]

#### FRONTEND
React Router → covered by ["React JS"]
Styled Components → covered by ["Styled Components"]

---

### ❌ STRICT NEGATIVE RULES

The following are NOT covered unless explicitly present:

❌ Time Series Analysis ≠ Data Analysis  
❌ Machine Learning ≠ Python  
❌ Data Science ≠ Pandas  
❌ CSV Handling ≠ Pandas (unless explicitly stated)

---

### ✅ EXAMPLES

INPUT:
required_skills = ["Time Series Analysis", "CSV/JSON Data Handling"]

CORRECT:
covered_skills = ["CSV/JSON Data Handling"]
missing_skills = ["Time Series Analysis"]

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3 — Compute Score
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

score = round((covered / required) * 10) * 10

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4 — Difficulty
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1–3 → Easy  
4–6 → Medium  
7+ → Hard  

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5 — Verdict
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

>=80 → Doable  
50–70 → Partially Doable  
<50 → Not Doable  

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT (STRICT JSON ONLY)
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

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LIMIT OUTPUT SIZE (CRITICAL)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- required_skills: maximum 20
- covered_skills: maximum 20
- missing_skills: maximum 20
- Keep response concise

CONSTRAINTS:
- covered + missing = required
- NO extra text
"""

    return prompt