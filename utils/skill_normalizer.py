def normalize_skill(skill: str) -> str:
    return (
        skill.lower()
        .replace(".", "")
        .replace("-", " ")
        .replace("/", " ")
        .strip()
    )