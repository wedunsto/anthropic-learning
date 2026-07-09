from dotenv import load_dotenv
from anthropic import Anthropic
from prompt_evaluations_exercise import PromptEvaluations

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5"

promptEvaluations = PromptEvaluations(client, model)

# Prompt engineering rules to replace prefilling
promptRules = """
Rules:
- Return only plain text
- Do not use markdown
- Do not include comments
- Do not include explanations
- After the plain text, write END_OF_COMMANDS
"""

# Tasks for the prompt evaluation exercise
tasks = [
    {
        "task": "Create a Python function to extract the AWS account ID from an ARN"
    },
    {
        "task": "Write a JSON policy document that allows read-only access to a specific S3 bucket"
    },
    {
        "task": "Write a regular expression that validates whether a string is in a valid email address format"
    }
]

"""
Starting point for grading and improving prompts
Add the task to the f-string
Add prompt rules after the task to replace prefilling
"""
initial_prompt = f"""
Please provide a solution to the following task:
{tasks[0]["task"]}
{promptRules}
"""

promptEvaluations.storeUserInputs(initial_prompt)

# Provide Claude with context to customize how Claude responds to user input
system_prompt = """
You are an expert regarding AWS and how to create Python function, JSON policy documents,
and regular expressions that interact with AWS. You adhere to industry best practices
"""

promptEvaluations.stop_sequences.append("END_OF_COMMANDS")

claudeResponse = promptEvaluations.askClaude(system_prompt)

promptEvaluations.storeClaudeResponse(claudeResponse)