"""
Objectives:
- Store user inputs and Claude responses
- Generate Claude responses
"""

class ClaudeChat:
    def __init__(self, model, client, messages=None):
        self.client = client
        self.model = model
        self.messages = messages
        self.stop_sequences = []

    # Store user input into the message history
    def userInput(self, message):
        if self.messages:
            self.messages.append(
                {
                    "role": "user",
                    "content": message.strip()
                }
            )

    # Store Claude response into the message history
    def claudeResponse(self, response):
        if self.messages:
            self.messages.append(
                {
                    "role": "assistant",
                    "content": response.strip()
                }
            )

    # Stream Claude's response to show the response generate in the terminal
    def streamClaudeResponse(self, parameters):
        with self.client.messages.stream(**parameters) as stream:
            for text in stream.text_stream:
                print(text, end="")

            final_message = stream.get_final_message()

            text_blocks = [
                block.text
                for block in final_message.content
                if block.type == "text"
            ]

            return "\n".join(text_blocks).strip()

    # Get Claude's response without streaming
    def getClaudeResponse(self, parameters):
        claude_response = self.client.messages.create(**parameters)

        text_blocks = [
            block.text
            for block in claude_response.content
                if block.type == "text"
        ]

        return "\n".join(text_blocks).strip()

    # Generate Claude response based on request and message history
    def askClaude(self, system_prompt=None, streaming=False):
        parameters={
            "model": self.model,
            "max_tokens": 1000
        }

        if self.messages:
            parameters["messages"] = self.messages

        # Provide context to customize Claude's output
        if system_prompt:
            parameters["system"] = system_prompt

        # Tell Claude when to stop generating output
        if self.stop_sequences:
            parameters["stop_sequences"] = self.stop_sequences

        """
        Stream Claude's output to show the response generate in the terminal
        Only return the desired output for debugging
        """
        if streaming:
            return self.streamClaudeResponse(parameters)
        else:
            return self.getClaudeResponse(parameters)