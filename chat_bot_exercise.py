"""
Objective: Make a chat bot using the three helper functions
from Multi-turn conversations
"""
class ChatBotExercise:
    def __init__(self, client, model):
        self.client = client
        self.model = model
        self.messages=[]

    # Add user's input to the message history
    def storeUserInput(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

    # Add Claude's response to the message history
    def storeClaudeResponse(self, claude_response):
        self.messages.append({"role": "assistant", "content": claude_response})

    # Capture Claude's response
    def askClaude(self):
        claudeResponse = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=self.messages
        )

        for block in claudeResponse.content:
            if block.type == "text":
                return block.text