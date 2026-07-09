"""
Objective: Improve the Model grader that was discussed in the Prompt Evaluation section
Give the Model Grader more context on what a good solution looks like
"""
class PromptEvaluations:
    def __init__(self, client, model):
        self.client = client
        self.model = model
        self.messages = []
        self.stop_sequences = []

    # Store user inputs to the message history
    def storeUserInputs(self, message):
        self.messages.append({"role": "user", "content": message})

    # Store Claude's response to the message history
    def storeClaudeResponse(self, response):
        self.messages.append({
            "role": "assistant", "content": response.strip()
            })

    # Stream Claude's output and get the the final message
    def streamClaudeResponse(self, parameter):
        with self.client.messages.stream(**parameter) as stream:
            for text in stream.text_stream:
                print(text, end="")
            
            final_message = stream.get_final_message()

        text_block = [
            block.text
            for block in final_message.content
                if block.type == "text"
        ]

        return text_block

    """
    Get Claude's response to the latest user's input 
    with the context of the message history
    """
    def askClaude(self, system_prompt=None):
        parameters = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": self.messages
        }

        if system_prompt:
            parameters["system"] = system_prompt

        if self.stop_sequences:
            parameters["stop_sequences"] = self.stop_sequences

        claude_response = self.streamClaudeResponse(parameters)

        return "\n".join(claude_response)
    
    # Use Claude to generate the evaluation dataset
    def generateDataset(self, system_prompt=None):
        parameters = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": self.messages
        }

        if system_prompt:
            parameters["system"] = system_prompt

        if self.stop_sequences:
            parameters["stop_sequences"] = self.stop_sequences

        claudeResponse = self.client.messages.create(**parameters)

        for block in claudeResponse.content:
            if block.type == "text":
                return block.text