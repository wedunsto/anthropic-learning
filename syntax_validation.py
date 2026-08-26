"""
Objective: Provide helper functions to validate JSON, Python, and regular expression outputs
"""
import json
import ast
import re

class SyntaxValidation:

    """
    Validate JSON response by parsing the output as JSON
    If the JSON is valid, give the test case a score of 10
    """
    def validate_json(self, text):
        try:
            json.loads(text.strip())
            return 10
        except json.JSONDecodeError:
            return 0
        
    """
    Validate Python response by parsing the output to a Python Abstract Syntax Tree
    If the Python is valid, give the test case a score of 10
    """
    def validate_python(self, text):
        try:
            ast.parse(text.strip())
            return 10
        except SyntaxError:
            return 0
        
    """
    Validate regex response by compiling the output as a regex
    If the regex is valid, give the test case a score of 10
    """
    def validate_regex(self, text):
        try:
            re.compile(text.strip())
            return 10
        except re.error:
            return 0