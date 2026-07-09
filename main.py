from dotenv import load_dotenv
from anthropic import Anthropic
import json
from prompt_evaluations_exercise import PromptEvaluations
from evaluation_dataset import EvaluationData

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5"

promptEvaluations = PromptEvaluations(client, model)

evaluationData = EvaluationData('dataset.json')

# Prompt engineering rules to replace prefilling
plain_text_prompt_rules = """
Rules:
- Return only plain text
- Do not use markdown
- Do not include comments
- Do not include explanations
- After the plain text, write END_OF_COMMANDS
"""

json_prompt_rules = """
Rules:
- Return only valid JSON
- Do not use markdown
- Do not include comments
- Do not include explanations outside the JSON
- Do not include trailing commas
- After the JSON, write END_OF_COMMANDS
"""

# Provide Claude with context to customize how Claude responds to user input
evaluation_system_prompt = """
You are an expert regarding AWS and how to create Python function, JSON policy documents,
and regular expressions that interact with AWS. You adhere to industry best practices
"""

promptEvaluations.stop_sequences.append("END_OF_COMMANDS")

# Observe the output of the first prompt draft
def initialPromptCall():
    # Tasks for the prompt evaluation exercise
    task = "Create a Python function to extract the AWS account ID from an ARN"

    """
    Starting point for grading and improving prompts
    Add the task to the f-string
    Add prompt rules after the task to replace prefilling
    """
    initial_prompt = f"""
    Please provide a solution to the following task:
    {task}
    {plain_text_prompt_rules}
    """

    promptEvaluations.storeUserInputs(initial_prompt)
    
    claudeResponse = promptEvaluations.askClaude(evaluation_system_prompt)
    
    promptEvaluations.storeClaudeResponse(claudeResponse)

# Output a JSON file containing the Claude generated evaluation dataset
def generateEvaluationDataset():
    """
    Generate test datasets that contains sample inputs representing the types
    of questions or requests the prompt will handle
    """
    dataset_prompt = f"""
    Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate
    Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task
    that requires Python, JSON, or a Regex to complete.

    Example output:
    ```json
    [
        {{
            "task": "Description of task",
        }},
        ...additional
    ]
    ```
    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
    * Focus on tasks that do not require writing much code

    Please generate 3 objects.
    {plain_text_prompt_rules}
    """

    dataset_system_prompt = """
    You are an expert in creating accurate, useful, and exhaustive evaludation datasets.
    You follow industry best practices when it comes to generating prompt evaluation datasets
    """
    
    promptEvaluations.storeUserInputs(dataset_prompt)
    
    claudeGeneratedDataset = promptEvaluations.generateDataset(dataset_system_prompt)

    evaluationData.setEvaluationDataset(claudeGeneratedDataset)

# Feed Evaluation Dataset through Claude
def testInitialPromptDraft():
    dataset = evaluationData.getEvaluationDataset()

    for data in dataset:
        prompt = f"""
        Please provide a solution to the following task:
        {data}
        {plain_text_prompt_rules}
        """
        promptEvaluations.storeUserInputs(prompt)

        claudeResponse = promptEvaluations.askClaude(evaluation_system_prompt)

        promptEvaluations.storeClaudeResponse(claudeResponse)

# Evaluate Claude's output using Claude
def gradeByModel():
    model_grading_results = []
    model_grading_scores = []
    grading_prompt = f"""
    Evalulate this AI-generated solution
    """

    system_prompt = "You are an expert code reviewer"

    dataset = evaluationData.getEvaluationDataset()

    for data in dataset:
        prompt = f"""
        Please provide a solution to the following task:
        {data}
        {plain_text_prompt_rules}
        """
        promptEvaluations.storeUserInputs(prompt)

        claudeResponse = promptEvaluations.askClaude(evaluation_system_prompt)

        promptEvaluations.storeClaudeResponse(claudeResponse)

        model_grading_prompt = f"""
        {grading_prompt}
        Task: {data}
        Solution: {claudeResponse}

        Return only valid JSON in this exact shape:
        {{
        "strengths": ["very short strength"],
        "weaknesses": ["very short weakness"],
        "reasoning": "One very short sentence.",
        "score": 7
        }}

        {json_prompt_rules}
        """

        promptEvaluations.storeUserInputs(model_grading_prompt)

        claudeGradingResult = promptEvaluations.askClaude(system_prompt)

        claudeJSONGradingResult = json.loads(claudeGradingResult)

        model_grading_results.append(promptEvaluations.generateTestCaseReport(data, claudeResponse, claudeJSONGradingResult))

        promptEvaluations.storeClaudeResponse(claudeGradingResult)

    for result in model_grading_results:
        model_grading_scores.append(result["score"])

    average = promptEvaluations.calculateAverage(model_grading_scores)

    print(f"Average score: {average}")

gradeByModel()
