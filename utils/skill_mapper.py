from utils.skill_normalizer import normalize_skill

EQUIVALENTS = {
    # Frontend
    "react": "React JS",
    "reactjs": "React JS",
    "react or next js": "React JS",
    "nextjs": "React JS",

    "tailwind css": "CSS",

    # Backend
    "nodejs": "Node JS Basics",
    "node js": "Node JS Basics",
    "expressjs": "Express JS framework",
    "express js": "Express JS framework",

    # Database
    "mysql": "SQL / Database",
    "postgresql": "SQL / Database",

    # APIs
    "rest api": "REST API design",
    "rest api design": "REST API design",

    # CRUD
    "crud operations": "CRUD APIs in Node JS",

    # Auth
    "jwt": "JWT Authentication",
    "jwt authentication": "JWT Authentication",
    "bcrypt": "bcrypt Password Hashing",

    # Env
    "environment variables": "Environment Variables in Node JS",

    # Testing
    "api testing": "API testing basics",
}


def map_skill(skill: str, syllabus_skills: list) -> str:
    norm = normalize_skill(skill)

    # Step 1: direct mapping
    if norm in EQUIVALENTS:
        return EQUIVALENTS[norm]

    # Step 2: fuzzy containment
    for s in syllabus_skills:
        if norm in normalize_skill(s):
            return s

    return skill