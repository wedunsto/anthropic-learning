"""
Objective: Use Claude to write a Python function that
checks a string for duplicate characters
"""
class PythonBotExercise:
    def __init__(self, client, model):
        self.client = client
        self.model = model
        self.messages = []

    # Add user's input to the message history
    def storeUserInput(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

    # Add Claude's response to the message history
    def storeClaudeResponse(self, claude_response):
        self.messages.append({"role": "assistant", "content": claude_response})

    # Capture Claude's response
    def askClaude(self, system_prompt=None):
        parameters = {
            "model":self.model,
            "max_tokens":1000,
            "messages":self.messages
        }

        if system_prompt:
            parameters["system"] = system_prompt

        claudeResponse=self.client.messages.create(**parameters)

        for block in claudeResponse.content:
            if block.type == "text":
                return block.text