"""
Objectives:
- Generate evaluation datasets with Claude
- Grade the prompt based on the output, using the evaluation dataset with Claude
"""
import json

class ClaudeDataset:
    def __init__(self, model, client):
        self.model = model
        self.client = client
        self.messages = []
        self.stop_sequences = []
        self.dataset_file = ""

    # Store user input into message history
    def storeUserInput(self, message):
        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )
    
    # Store Claude response into message history
    def storeClaudeResponse(self, response):
        self.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

    # Store the dataset in dataset.json
    def setEvaluationDataset(self, dataset):
        jsonDataset = json.loads(dataset)

        with open(self.dataset_file, 'w') as file:
            json.dump(jsonDataset, file, indent=2)

    # Get the dataset from dataset.json
    def getEvaluationDataset(self):
        with open(self.dataset_file, "r") as file:
            dataset = json.load(file)
        
        return dataset

    # Use Claude to generate the evaluation dataset and store them in dataset.json
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
        
        claude_response = self.client.messages.create(**parameters)

        for block in claude_response.content:
            if block.type == "text":
                self.setEvaluationDataset(block.text)
                return