"""
Helper functions for the chat bot exercise
"""

class ChatBot:
    def __init__(self, client, model):
        self.client = client
        self.model = model

        # Conversation history adds context to the future of the conversation
        self.messages = []

    # Store user input into the conversation history
    def storeUserInput(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })

    # Store Claude's response into the conversation history
    def storeClaudeResponse(self, message):
        self.messages.append({
            "role": "assistant",
            "content": message
        })

    """
    Get Claude's response to the most recent user input
    Leverages conversation history
    """
    def askClaude(self):
        parameters = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": self.messages
        }

        response = self.client.messages.create(**parameters)

        for block in response.content:
            if block.type == "text":
                return block.text