"""
Objective: Read and write the JSON file containing the evaluation dataset
"""
import json

class EvaluationData:
    def __init__(self, file_path):
        self.file_path = file_path

    def getEvaluationDataset(self):
        with open(self.file_path, 'r') as file:
            dataset = json.load(file)

        return dataset
    
    def setEvaluationDataset(self, claudeGeneratedDataset):
        jsonDataset = json.loads(claudeGeneratedDataset)

        with open(self.file_path, 'w') as file:
            json.dump(jsonDataset, file, indent=2)