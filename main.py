from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import re

from services.prompt_builder import build_prompt
from services.llm_service import evaluate_assignment
from services.extractors.pdf_extractor import extract_text_from_pdf
from services.extractors.docx_extractor import extract_text_from_docx
from services.extractors.googledoc_extractor import extract_text_from_googledoc
from services.extractors.notion_extractor import extract_text_from_notion

app = FastAPI(
    title="Assignment Doability Checker",
    description="Checks if a company assignment is doable based on course syllabus",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_VERDICTS = {"Doable", "Partially Doable", "Not Doable"}
VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}


@app.get("/")
def home():
    return {"message": "Assignment Doability Checker API v2 is running!"}


@app.post("/evaluate")
async def evaluate(
    input_type: str = Form(...),
    assignment_text: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    extracted_text = ""

    try:
        if input_type == "text":
            if not assignment_text:
                return {"error": "No text provided"}
            extracted_text = assignment_text

        elif input_type == "pdf":
            if not file:
                return {"error": "No file uploaded"}
            file_bytes = await file.read()
            extracted_text = extract_text_from_pdf(file_bytes)

        elif input_type == "docx":
            if not file:
                return {"error": "No file uploaded"}
            file_bytes = await file.read()
            extracted_text = extract_text_from_docx(file_bytes)

        elif input_type == "googledoc":
            if not url:
                return {"error": "No URL provided"}
            extracted_text = extract_text_from_googledoc(url)

        elif input_type == "notion":
            if not url:
                return {"error": "No URL provided"}
            extracted_text = extract_text_from_notion(url)

        else:
            return {"error": f"Unknown input_type: {input_type}"}

    except Exception as e:
        return {"error": f"Failed to extract text: {str(e)}"}

    if not extracted_text or not extracted_text.strip():
        return {"error": "Could not extract any text from the input"}

    # Build prompt and call LLM
    prompt = build_prompt(extracted_text)

    try:
        raw_result = evaluate_assignment(prompt)
    except Exception as e:
        return {"error": f"LLM call failed: {str(e)}"}

    # Parse LLM JSON response
    try:
        clean = re.sub(r"```(?:json)?|```", "", raw_result).strip()
        # Handle cases where LLM wraps output in extra text before/after JSON
        json_match = re.search(r"\{.*\}", clean, re.DOTALL)
        if json_match:
            clean = json_match.group(0)
        result = json.loads(clean)
    except Exception:
        return {"error": "Could not parse AI response", "raw": raw_result}

    # Validate and fix score — must always be a multiple of 10
    score = result.get("doability_score", 0)
    if isinstance(score, (int, float)) and score % 10 != 0:
        result["doability_score"] = round(score / 10) * 10

    # Validate verdict and difficulty enums
    if result.get("verdict") not in VALID_VERDICTS:
        result["verdict"] = "Partially Doable"  # safe fallback

    if result.get("difficulty") not in VALID_DIFFICULTIES:
        result["difficulty"] = "Medium"  # safe fallback

    # Validate skill list consistency:
    # covered + missing must equal required (catch LLM omissions)
    required = set(result.get("required_skills", []))
    covered = set(result.get("covered_skills", []))
    missing = set(result.get("missing_skills", []))

    if covered | missing != required:
        # Recompute missing from what the LLM actually marked as covered
        result["missing_skills"] = list(required - covered)

    return result