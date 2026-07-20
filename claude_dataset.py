"""
Objectives:
- Generate evaluation datasets with Claude
- Grade the prompt based on the output, using the evaluation dataset with Claude
"""
from claude_chat import ClaudeChat
import json

class ClaudeDataset:
    def __init__(self, model, client):
        self.claude_chat = ClaudeChat(model, client)
        self.dataset_file = ""

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
    def generateDataset(self, dataset_prompt):
        self.dataset_file = "dataset.json"

        self.claude_chat.stop_sequences.append("END_OF_COMMANDS")
        
        dataset_system_prompt = """
        You are an expert in creating accurate, useful, and exhaustive evaluation datasets.
        You follow industry best practices when it comes to generating prompt evaluation datasets
        """
        claude_response = self.claude_chat.askClaudeSingle(dataset_prompt, dataset_system_prompt)

        self.setEvaluationDataset(claude_response)