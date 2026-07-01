from dotenv import load_dotenv
from anthropic import Anthropic
from python_bot_exercise import PythonBotExercise

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5"

pythonBotExercise = PythonBotExercise(client, model)

system_prompt = "You are a Python engineer who writes very concise code"

# Prompt the user what they would like to know
initial_prompt = "What question about Python programming would you like to know?"

print(initial_prompt)

user_input = input()

# Store the user inputs in the message history
pythonBotExercise.storeUserInput(initial_prompt)
pythonBotExercise.storeUserInput(user_input)

# Capture Claude response
claude_response = pythonBotExercise.askClaude(system_prompt)

# Store Claude response in the message history
pythonBotExercise.storeClaudeResponse(claude_response)

print(claude_response)