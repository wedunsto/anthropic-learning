from dotenv import load_dotenv
from anthropic import Anthropic
from chat_bot_exercise import ChatBotExercise

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5"

chatBotExercise = ChatBotExercise(client, model)

# End case to stop the conversation
continue_conversation = "yes"

# Prompt the user to enter some input using the built-in "input" function
initial_prompt = "Where do you want to go on vacation next? "
print(initial_prompt)
user_input = input()

# Add it to a list of messages
chatBotExercise.storeUserInput(initial_prompt)
chatBotExercise.storeUserInput(user_input)

# Call the API
next_prompt = "What can you tell me about " + user_input + " in one sentence"
chatBotExercise.storeUserInput(next_prompt)
claude_response = chatBotExercise.askClaude()

# Add generated text to the list of messages
chatBotExercise.storeClaudeResponse(claude_response)

# Print the generated text
print(claude_response)

while(continue_conversation == "yes"):
    print("Ask your next question")
    user_input = input()

    truncated_user_input = user_input + ", answer in one sentence"
    chatBotExercise.storeUserInput(user_input)

    # Utilize the message history to give Claude context on the conversation
    claude_response = chatBotExercise.askClaude()

    # Add generated text to the list of messages
    chatBotExercise.storeClaudeResponse(claude_response)

    # Print the generated text
    print(claude_response)

    print("Would you like to ask another question? yes / no")
    continue_conversation = input()