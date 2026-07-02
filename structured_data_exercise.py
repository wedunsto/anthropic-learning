"""
Objective: Use message prefilling and stop sequences to get three different commands in a single response
    Claude's output should not include any comments or explanation 
"""

class StructuredDataExercise:
    def __init__(self, client, model):
        self.client = client
        self.model = model
        self.messages = []
        self.prefilling = ""
        self.stop_sequences = []

    def storeUserInput(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

    def storeClaudeResponse(self, claude_response):
        self.messages.append({"role": "assistant", "content": claude_response})

    def askClaude(self, system_prompt=None):
         
        parameters = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": self.messages
        }

        if system_prompt:
            parameters["system"] = system_prompt

        # Add stop sequences to the parameters
        if self.stop_sequences:
            parameters["stop_sequences"] = self.stop_sequences

        with self.client.messages.stream(**parameters) as stream:
            for text in stream.text_stream:
                print(text, end="")

            final_message = stream.get_final_message()

        text_blocks = [
            block.text
            for block in final_message.content
                if block.type == "text"
        ]

        return "\n".join(text_blocks)