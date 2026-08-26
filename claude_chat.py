"""
Objectives:
- Store user inputs and Claude responses
- Generate Claude responses
"""

class ClaudeChat:
    def __init__(self, model, client):
        self.client = client
        self.model = model
        self.messages = []
        self.stop_sequences = []

    # Store user input into the message history
    def userInput(self, message):
        self.messages.append({
            "role": "user",
            "content": message.strip()
        })

    # Return tool function results back to Claude
    def returnToolFunctionResult(self, result, tool_use_id):
        self.messages.append({
            "role": "user",
            "content": [{
                "tool_use_id": tool_use_id,
                "type": "tool_result",
                "content": result,
                "is_error": False
            }]
        })

    # Store Claude response into the message history
    def claudeResponse(self, response):
        claude_response = {
            "role": "assistant"
        }

        if isinstance(response, list):
            claude_response["content"] = response
        else:
            claude_response["content"] = response.strip()
        
        self.messages.append(claude_response)

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
            "max_tokens": 1000,
            "messages": self.messages
        }

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
    
    """
    Do not store conversation history for prompt evaluations or dataset generation.
    With history, a list of all results is stored
    """
    def askClaudeSingle(self, prompt, system_prompt=None, streaming=False):
        parameters = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": [{
                "role": "user",
                "content": prompt
                }]
        }

        if system_prompt:
            parameters["system"] = system_prompt

        if self.stop_sequences:
            parameters["stop_sequences"] = self.stop_sequences

        if streaming:
            return self.streamClaudeResponse(parameters)
        else:
            return self.getClaudeResponse(parameters)
        
    # Make tool enabled API calls
    def askClaudeWithTools(self, tool_schema, system_prompt=None, streaming=False):
        parameters = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": self.messages,
            "tools": [tool_schema]
        }

        if system_prompt:
            parameters["system"] = system_prompt

        if self.stop_sequences:
            parameters["stop_sequences"] = self.stop_sequences

        claude_response = self.client.messages.create(**parameters)

        return claude_response.content
        
    
    def clearChatHistory(self):
        self.messages = []