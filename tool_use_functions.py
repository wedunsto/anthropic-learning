"""
Objectives: Create tool functions to create structured ways for Claude to request fresh information
"""
import json
import inspect

from claude_chat import ClaudeChat
from datetime import timedelta, datetime

class ClaudeTool:
    def __init__(self, model, client):
        self.claude_chat = ClaudeChat(model, client)
        self.claude_chat.stop_sequences.append("END_OF_COMMANDS")

    # Tool function for Claude to get the current date
    def getCurrentDateTime(self, date_format="%Y-%m-%d %H:%M:%S"):
        if not date_format:
            return ValueError("date_format cannot be empty")
        return datetime.now().strftime(date_format)
    
    # Tool function for Claude to get a future date
    def calculateFutureDate(self, weekday):
        weekdays = {
            "monday": 0,
            "tuesday":1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 0,
        }
        
        normalized_weekday = weekday.strip().lower()
        
        # Replace this with the output of the current date tool function call
        current_date = datetime.now()
        
        target_weekday = weekdays[normalized_weekday]
        
        days_ahead = (target_weekday - current_date.weekday()) % 7
        
        target_date = current_date + timedelta(days=days_ahead)
        
        return target_date
    
    # Tool function to set the a reminder for a future date
    def setAppointmentReminder(self, future_date):
        print(f"I have set a reminder for your appointment on: {future_date}")

    # Helper function to leverage Claude to generate JSON tool schemas for the tool functions
    def generateToolSchema(self, tool_function):
        tool_schema_example = ""

        """
        Prompt engineering rules to replace prefilling
        Rules for generating the JSON schema for tool functions
        """
        tool_schema_generation_prompt_rules = """
        Rules:
        - Return only valid JSON
        - Do not use markdown
        - Do not wrap the JSON in ```json or ```
        - Do not include comments
        - Do not include explanations outside the JSON
        - Do not include trailing commas
        - Include only parameters accepted by the function
        - Do not create parameters that are not present in the function signature
        - Mark a parameter as required unless it has a default value
        - Use valid JSON Schema types
        - Set additionalProperties to false
        - After the JSON, write END_OF_COMMANDS
        """

        sample_function = inspect.getsource(self.getCurrentDateTime)

        with open("tool_schema_example.json", "r") as file:
            tool_schema_example = json.load(file)

        tool_schema_prompt = f"""
        Write a valid JSON schema spec for the purposes of tool calling for this function. Follow the best practices for creating tool schemas.

        <input_function>
        {tool_function}
        </input_function>

        Here is an example input with an ideal response
        <sample_input>
        {sample_function}
        </sample_input>

        <ideal_output>
        {tool_schema_example}
        </ideal_output>

        {tool_schema_generation_prompt_rules}
        """

        tool_schema_system_prompt = "You are an expert at creating valid JSON tool function schemas. You adhere to the professional best practices from Anthropic on how to create tool function schema"
        
        claude_response = self.claude_chat.askClaudeSingle(tool_schema_prompt, tool_schema_system_prompt)

        return claude_response
    