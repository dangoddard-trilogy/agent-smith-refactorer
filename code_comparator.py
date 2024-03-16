import json
import logging  # AI-GEN - CursorAI with GPT4

class CodeComparator:
    def __init__(self, assistant_manager):
        self.assistant_manager = assistant_manager
        logging.info("CodeComparator: Initialized with assistant manager.")  # AI-GEN - CursorAI with GPT4

    def compare(self, original_file_id, refactored_file_id, rules):
        """
        Uses the AI assistant to compare the original and refactored code files.
        
        Parameters:
            original_file_id (str): The identifier for the original source file in the assistant's file store.
            refactored_file_id (str): The identifier for the refactored source file in the assistant's file store.
            rules (dict): The rules used for refactoring.
        
        Returns:
            bool: True if the refactoring is correct, False otherwise.
        """
        logging.info(f"CodeComparator: Comparing original file ID {original_file_id} with refactored file ID {refactored_file_id} using given rules.")  # AI-GEN - CursorAI with GPT4
        # Construct a prompt for the AI to analyze the codes based on file IDs
        prompt = self._generate_analysis_prompt(original_file_id, refactored_file_id, rules)
        
        # Use the AssistantManager to get the analysis result
        analysis_result = self.assistant_manager.analyze_code(prompt, [original_file_id, refactored_file_id])
        logging.info("CodeComparator: Analysis result obtained from assistant manager.")  # AI-GEN - CursorAI with GPT4
        
        # Interpret the AI assistant's response to determine pass/fail
        return self._interpret_analysis_result(analysis_result)

    def _generate_analysis_prompt(self, original_file_id, refactored_file_id, rules):
        """
        Generates a prompt for the AI to analyze the original and refactored code files.
        
        This function creates a narrative for the AI, asking it to analyze the files identified
        by their IDs in the context of the refactoring rules, and to evaluate if the refactoring
        is correctly implemented.
        
        Parameters:
            original_file_id (str): The identifier for the original file.
            refactored_file_id (str): The identifier for the refactored file.
            rules (dict): The rules used for refactoring.
        
        Returns:
            str: The generated prompt for the AI.
        """
        logging.info("CodeComparator: Generating analysis prompt for AI.")  # AI-GEN - CursorAI with GPT4
        rules_descriptions = json.dumps(rules, indent=2)
        prompt = (
            f"Analyze the refactoring changes made from the original file (ID: {original_file_id}) "
            f"to the refactored file (ID: {refactored_file_id}). "
            f"Consider the following refactoring rules: {rules_descriptions}\n\n"
            "To the best of your knowledge, does the refactored file correctly implement the original logic without violating the refactoring rules? \n" 
            "Please respond only with a JSON object with the following parameters:\n"
            "{"
            "   \"result\": [\"Yes\", \"No\"],"
            "   \"details\": \"text-based description\","
            "}"
        )
        return prompt  # AI-GEN - CursorAI with GPT4

    def _parse_analysis_result(self, analysis_result):
        """ Parses the analysis result string, removing markdown backticks, any language identifiers, and ensuring it's a valid JSON string. 
        
        Parameters: 
            analysis_result (str): The analysis result string potentially wrapped in markdown code block syntax or containing extra characters. 
        
        Returns: 
            str: A cleaned string in proper JSON format. 
        """ 
        
        # First, strip any markdown code block syntax or extra whitespace
        cleaned_result = analysis_result.strip("`").strip()

        # Attempt to find the start and end of a valid JSON object if there's extra data
        try:
            start = cleaned_result.index('{')
            end = cleaned_result.rindex('}') + 1
            valid_json_str = cleaned_result[start:end]
            return valid_json_str  # Return the extracted valid JSON string
        except ValueError as e:  # Catch cases where '{' or '}' are not found
            logging.error(f"Error extracting valid JSON from result: {e}")
            return "{}"  # Return an empty JSON object as a fallback

        return cleaned_result  # Fallback return (should not be reached)
    
    def _interpret_analysis_result(self, analysis_result): 
        """ Interprets the AI assistant's analysis result. 
        Parameters: 
            analysis_result (str): The analysis result from the AI assistant. 
        Returns: 
            bool: True if the analysis indicates the refactoring is correct, False otherwise. 
        """ 
        logging.info("CodeComparator: Interpreting analysis result from AI.") # AI-GEN - CursorAI with GPT4 
        
        cleaned_analysis_result = self._parse_analysis_result(analysis_result) # Clean the result string 
        
        logging.info(f"CodeComparator: Analysis Message: {cleaned_analysis_result}")

        try: 
            analysis_result_json = json.loads(cleaned_analysis_result)  # Convert the cleaned string to a JSON object  # AI-GEN - CursorAI with GPT4
        except json.JSONDecodeError as e: 
            logging.error(f"Failed to decode JSON: {e}")  # Log the error  # AI-GEN - CursorAI with GPT4
            return False  # Return False in case of JSON decoding failure  # AI-GEN - CursorAI with GPT4
        
        result = analysis_result_json.get('result', 'No')  # AI-GEN - CursorAI with GPT4
        if isinstance(result, bool):  # Check if result is a boolean  # AI-GEN - CursorAI with GPT4
            return result  # Directly return the boolean value  # AI-GEN - CursorAI with GPT4
        elif isinstance(result, list):  # Check if result is a list  # AI-GEN - CursorAI with GPT4
            result = result[0].lower() if result else 'no'  # Take the first item if list is not empty and convert to lowercase  # AI-GEN - CursorAI with GPT4
        elif isinstance(result, str):  # Check if result is a string  # AI-GEN - CursorAI with GPT4
            result = result.lower()  # Convert to lowercase  # AI-GEN - CursorAI with GPT4
        else:
            return False  # Return False if result is neither a list, string, nor boolean  # AI-GEN - CursorAI with GPT4

        return result == 'yes'  # Return True if the result is 'yes', False