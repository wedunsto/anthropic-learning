from dotenv import load_dotenv
from anthropic import Anthropic
from structured_data_exercise import StructuredDataExercise

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5"

structuredDataExercise = StructuredDataExercise(client, model)

initial_prompt = """
Generate exactly three different sample AWS CLI commands.

Rules:
- Return only plain text.
- Do not use markdown.
- Do not use code fences.
- Put each command on its own line.
- Do not include comments.
- Do not include explanations.
- After the third command, write END_OF_COMMANDS.
"""

structuredDataExercise.prefilling = "```bash"
structuredDataExercise.stop_sequences.append("END_OF_COMMANDS")

structuredDataExercise.storeUserInput(initial_prompt)

claudeResponse = structuredDataExercise.askClaude("You are an expert around all things AWS. Return only AWS CLI commands. No comments. No explanation.")

structuredDataExercise.storeClaudeResponse(claudeResponse)