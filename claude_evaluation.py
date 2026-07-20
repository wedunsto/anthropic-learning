"""
Objective: Evaluate prompts against Claude generated datasets
Model based grading: Test the prompt with the dataset. Assign a score to the output
Code based grading: Verify the generated code has valid syntax and follows the correct format
"""
from claude_chat import ClaudeChat
from statistics import mean
import json

class ClaudeEvaluation:
    def __init__(self, client, model):
        self.claude_chat = ClaudeChat(model, client)

    """
    Run the dataset against the prompt
    Returns Claude's solution
    """
    def testPrompt(self, dataset, prompt, prompt_rules):
        prompt_test_results = []

        self.claude_chat.stop_sequences.append("END_OF_COMMANDS")

        system_prompt = "You are an expert at analyzing scholarly articles and identifying the topics in the articles"

        for data in dataset:
            solution_criteria = data["solution_criteria"]
            extended_prompt = f"""
            {prompt}
            {data}
            Criteria you should use to evaluate the solution
            {solution_criteria}
            {prompt_rules}
            """

            claude_response = self.claude_chat.askClaudeSingle(extended_prompt, system_prompt)

            prompt_test_results.append(claude_response)

        return prompt_test_results

    # Test the prompt with the dataset. Assign it a score
    def modelBasedGrading(self, dataset, dataset_results, prompt_rules):
        claude_grading_results = []

        system_prompt = "You are an expert at analyzing the effectiveness of AI-generated solutions for a given prompt"

        for index, data in enumerate(dataset):
            model_grading_prompt = f"""
            Evaluate this AI-generated solution
            Task: {data}
            Solution: {dataset_results[index]}

            Return only valid JSON in this exact shape:
            {{
            "strengths": ["very short strength."],
            "weaknesses": ["very short weakness"],
            "reasoning": "One very short sentence.",
            "score": 7
            }}

            {prompt_rules}
            - Return exactly one valid JSON object
            - Do not wrap the JSON in ```json or ```
            """

            claude_response = self.claude_chat.askClaudeSingle(model_grading_prompt, system_prompt)

            claude_grading_results.append(claude_response)

        return claude_grading_results
    
    # Verify the generated code has valid syntax and follows the correct format
    def codeBasedGrading(self, dataset_results):
        code_grading_results = []
        for output in dataset_results:
            # If the string is valid, give the test case a score of 10
            if isinstance(output, str):
                # Ensure dictionaries are stored to work with JSON more easily
                code_grading_results.append({
                    "solution": output,
                    "score": 10
                })
            else:
                code_grading_results.append({
                    "solution": output,
                    "score": 0
                })
        return code_grading_results
    
    # Calculate the average of the model based grade and the code based grade
    def calculateAverage(self, model_grades, code_grades):
        scores = []
        for index, grade in enumerate(model_grades):
            # Convert JSON to dictionary
            parsed_model_grade = json.loads(grade)
            
            scores.append(parsed_model_grade["score"])

            code_grade = code_grades[index]
            scores.append(code_grade["score"])

        return mean(scores)