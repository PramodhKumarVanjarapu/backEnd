from services.prompt_builder import build_prompt
from services.llm_service import evaluate_assignment

assignment = "Build a REST API using Node.js and JWT authentication with a SQL database"

prompt = build_prompt(assignment)
result = evaluate_assignment(prompt)

print(result)