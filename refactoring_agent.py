import os
import logging
import json
import re
import threading
import time
from code_comparator import CodeComparator
from file_manager import FileManager
from rule_manager import RuleManager
from assistant_manager import AssistantManager

class RefactoringAgent:
    def __init__(self, files_list_path, rules_path, api_key, assistant_id, organization_id, base_path=""):  # AI-GEN - CursorAI with GPT4
        logging.info("RefactoringAgent: Initializing RefactoringAgent...")  # AI-GEN - CursorAI with GPT4
        self.files_list_path = files_list_path
        self.rules_path = rules_path
        self.base_path = base_path  # Store the base path
        self.rule_manager = RuleManager(rules_path)
        self.file_manager = FileManager()
        self.index = 0
        self.total_files = 0
        self.passed_files = 0
        self.failed_files = 0
        #self.thread_ids = []
        self.assistant_managers = []  # Initialize an array to hold AssistantManager instances // AI-GEN - CursorAI with GPT4
        self.api_key = api_key
        self.assistant_id = assistant_id
        self.organization_id = organization_id
        logging.info("RefactoringAgent: RefactoringAgent initialized.")  # AI-GEN - CursorAI with GPT4


    def start_refactoring_process(self):
        logging.info("RefactoringAgent: Starting refactoring process...")
        
        source_list, total_files = self.file_manager.read_source_list(self.files_list_path)
        self.total_files = total_files
        threads = []
        thread_name_index = 0;
        for item in source_list:
            # Use the enumerate function to get an index for each item, and use it as part of the thread name
            thread_name_index += 1
            t = threading.Thread(target=self.process_file_thread, args=(item,), name=f"Thread-{thread_name_index}")
            threads.append(t)
            t.start()
            time.sleep(0.5)
        
        for t in threads:
            t.join()

    def process_file_thread(self, item):
        thread_name = threading.current_thread().name  # Get the current thread's name // AI-GEN - CursorAI with GPT4
        logging.info(f"{thread_name}: Starting to process file {item['path']}")  # Include the thread name in the log // AI-GEN - CursorAI with GPT4
        file_path = os.path.join(self.base_path, item["path"]) if self.base_path else item["path"]  # Determine the full file path // AI-GEN - CursorAI with GPT4
        deprecated_method = item["deprecatedMethod"]  # Extract the deprecated method from the item // AI-GEN - CursorAI with GPT4
        
        logging.info(f"{thread_name}: Initializing AssistantManager with API key {self.api_key}, Assistant ID {self.assistant_id}, and Organization ID {self.organization_id}.")  # Verbose logging for AssistantManager creation // AI-GEN - CursorAI with GPT4
        assistant_manager = AssistantManager(api_key=self.api_key, assistant_id=self.assistant_id, organization_id=self.organization_id)  # Create a new instance for each thread // AI-GEN - CursorAI with GPT4
        self.assistant_managers.append(assistant_manager)  # Add the AssistantManager instance to the array // AI-GEN - CursorAI with GPT4
        logging.info(f"{thread_name}: AssistantManager created. Now processing file {file_path} for deprecated method {deprecated_method}.")  # Verbose logging for file processing // AI-GEN - CursorAI with GPT4
        self.process_file(file_path, deprecated_method, assistant_manager)  # Process the file with the given deprecated method // AI-GEN - CursorAI with GPT4
        return  # End the current thread's processing // AI-GEN - CursorAI with GPT4

    def process_file(self, file_path, deprecated_method, assistant_manager):
            thread_name = threading.current_thread().name
            # Load the rules from the JSON file
            with open(self.rules_path, 'r') as file:
                rules = json.load(file)
            
            result = self.interpret_instructions(rules, file_path, deprecated_method, assistant_manager)
            
            return
    
            if result.value == "Pass":
                # If the result is "Pass", continue to the next step
                            # If all steps are successful, print the result
                print(f"Refactoring successful for {file_path}")  # AI-GEN - CursorAI with GPT4
                self.passed_files += 1  # AI-GEN - CursorAI with GPT4
                self.index+=1
            else:
                self.failed_files += 1
                self.index+=1

            return

    def interpret_instructions(self, rules, file_path, deprecated_method, assistant_manager):
        thread_name = threading.current_thread().name
        source_file_id = None
        new_file_id = None
        local_instructions = rules["instructions"].copy()  # Create a local copy of the instructions

        for index, instruction in enumerate(local_instructions):
            if instruction["who"] == "code":
                if instruction["step"] == "Upload Source Code":
                    source_file_id = assistant_manager.upload_file(file_path)
                    self.replace_placeholder_values(local_instructions, {"source_file_id": source_file_id})
                    formatted_result = {"result": {"source_file_id": source_file_id}}  # Format the result as specified
                    local_instructions[index]["result"] = formatted_result  # Update the local copy with the formatted result
                elif instruction.get("command") == "foreach":
                    input_data = self.parse_input_data(instruction.get("input"), local_instructions)
                    results = []  # Initialize an empty list to collect results from each subtask call
                    for item in input_data:
                        subtask_instruction = instruction["subtask"].copy()  # Make a copy of the subtask instruction
                        self.replace_placeholder_values(subtask_instruction, item)  # Replace placeholders
                        subtask_result = self.interpret_instructions({"instructions": [subtask_instruction]}, file_path, deprecated_method, assistant_manager)
                        results.append(subtask_result)  # Collect the result
                    local_instructions[index]["results"] = results  # Update the local copy with the results
            elif instruction["who"] == "agent":
                if instruction["step"] == "Identify Deprecated Usage":
                    shorthand_method_name = assistant_manager.convert_deprecated_method_to_shorthand(deprecated_method)
                    self.replace_placeholder_values(local_instructions, {"shorthand_method_name": shorthand_method_name, "deprecated_method": deprecated_method})
                    prompt = self.create_prompt_from_instruction(instruction)
                    result = assistant_manager.call_agent(prompt)
                    logging.info(f"{thread_name}: Prompt output: {result.value}")
                    json_result = self.extract_json_from_string(result.value)
                    logging.info(f"{thread_name}: Extracted JSON result: {json_result}")
                    local_instructions[index]["result"] = json_result  # Update the local copy with the result
                elif instruction["step"] == "Plan Refactoring":
                    input_data = self.parse_input_data(instruction.get("input"), local_instructions)
                    self.replace_placeholder_values(instruction, input_data)  # Replace placeholders
                    prompt = self.create_prompt_from_instruction(instruction)
                    result = assistant_manager.call_agent(prompt)
                    logging.info(f"{thread_name}: Prompt output: {result.value}")
                    json_result = self.extract_json_from_string(result.value)
                    logging.info(f"{thread_name}: Extracted JSON result: {json_result}")
                    local_instructions[index]["result"] = json_result  # Update the local copy with the result
                elif instruction["step"] == "Execute Refactoring":
                    pass  # Similar handling for other steps
                elif instruction["step"] == "Review and Verify":
                    pass  # Similar handling for other steps

        return local_instructions  # Return the updated local copy of instructions with result
    
    def create_prompt_from_instruction(self, instruction):
        """
        Creates a prompt for the agent based on the given instruction.

        :param instruction: A dictionary representing the instruction.
        :return: A JSON string representing the prompt and expected return format.
        """
        # Extract necessary parts from the instruction
        step = instruction.get("step", "")
        detail = instruction.get("detail", "")
        input_data = instruction.get("input", "")
        
        # Initialize input_placeholders as an empty list
        input_placeholders = []

        # Check if input_data is a dictionary and handle accordingly
        if isinstance(input_data, dict):
            # If input_data is a dictionary, extract keys as placeholders
            input_placeholders = list(input_data.keys())
        elif isinstance(input_data, str):
            # If input_data is a string, split it as before
            input_placeholders = input_data.split(", ")

        # Construct the prompt text
        prompt_text = f"{step}: {detail}"
        for placeholder in input_placeholders:
            # Assuming placeholders are formatted as {placeholder_name} in the detail text
            if placeholder in instruction:  # Check if the placeholder value is provided in the instruction
                prompt_text = prompt_text.replace(f"{{{placeholder}}}", str(instruction[placeholder]))

        # Construct the output JSON
        prompt_json = {
            "prompt": prompt_text,
            "return": instruction.get("return", [])
        }

        return json.dumps(prompt_json)  # Convert the dictionary to a JSON string and return it

    def replace_placeholder_values(self, instructions, placeholders):
        """
        Recursively replaces placeholder values in instructions or a single instruction with new values specified in placeholders.
        This method handles both lists of instructions and individual instruction dictionaries, including any nested subtasks.

        :param instructions: A list of instruction dictionaries or a single instruction dictionary to be updated.
        :param placeholders: A dictionary of placeholder names and their new values.
        """
        if isinstance(instructions, dict):  # If instructions is a single instruction dictionary
            self._replace_placeholders_in_item(instructions, placeholders)
        elif isinstance(instructions, list):  # If instructions is a list of instruction dictionaries
            for instruction in instructions:
                self._replace_placeholders_in_item(instruction, placeholders)

    def _replace_placeholders_in_item(self, item, placeholders):
        """
        Recursively replaces placeholders in an item, which could be an instruction or a subtask.

        :param item: The item (instruction or subtask) to update.
        :param placeholders: A dictionary of placeholder names and their new values.
        """
        for key, value in item.items():
            if isinstance(value, str):  # Replace placeholders in strings
                for placeholder, new_value in placeholders.items():
                    value = value.replace(f"{{{placeholder}}}", str(new_value))
                item[key] = value
            elif isinstance(value, dict):  # Recursively handle dictionaries
                self._replace_placeholders_in_item(value, placeholders)
            elif isinstance(value, list):  # Recursively handle lists, for cases like nested subtasks
                for subitem in value:
                    if isinstance(subitem, (dict, list)):
                        self._replace_placeholders_in_item(subitem, placeholders)

    def parse_input_data(self, input_spec, local_instructions):
        """
        Parses the input data based on the input specification.

        :param input_spec: The input specification from the instruction.
        :param source_file_id: The ID of the source file uploaded.
        :param deprecated_method: The deprecated method being refactored.
        :param local_instructions: The local copy of instructions with their results.
        :return: The parsed input data.
        """
        if isinstance(input_spec, dict):
            if input_spec.get("result_from_step"):
                # The input is expected to come from the result of a previous step
                result_from_step = input_spec["result_from_step"]
                # Find the instruction that matches the result_from_step
                for instruction in local_instructions:
                    if instruction.get("step") == result_from_step:
                        # Extract the result from the matched instruction
                        return instruction.get("result", [])
            else:
                return input_spec

        elif isinstance(input_spec, str):
            # Handle other types of input specifications if necessary
            pass

        # Default return if no matching condition is found
        return []

    def print_results(self):
        """Prints the summary of the refactoring process."""
        print(f"Total files processed: {self.index}")  # AI-GEN - CursorAI with GPT4
        print(f"Total files attempted: {self.total_files}")  # AI-GEN - CursorAI with GPT4
        print(f"Files successfully refactored: {self.passed_files}")  # AI-GEN - CursorAI with GPT4
        print(f"Files failed to refactor: {self.failed_files}")  # AI-GEN - CursorAI with GPT4

    def _process_file(self, file_path, deprecated_method, assistant_manager):
        thread_name = threading.current_thread().name
        """Processes each file through the refactoring pipeline."""
        print(f"{thread_name}: Processing file {file_path} ({self.index+1}/{self.total_files})")  # AI-GEN - CursorAI with GPT4
        logging.info(f"{thread_name}: RefactoringAgent: Uploading original file for refactoring: {file_path}")  # AI-GEN - CursorAI with GPT4

        # Create a new thread for this file
        thread_id = self.assistant_manager.create_new_thread()

        # The original file is uploaded to the assistant's file store
        original_file_id = self.assistant_manager.upload_file(file_path)
        refactoring_attempts = 0
        refactoring_success = False

        while not refactoring_success and refactoring_attempts < 5:
            logging.info(f"{thread_name}: RefactoringAgent: Refactoring attempt {refactoring_attempts + 1} for file: {file_path}")  # AI-GEN - CursorAI with GPT4
            refactored_file_id = self.refactor_code(original_file_id, deprecated_method, refactoring_attempts)
            
            # If refactor_code returns None, treat it as a failed attempt and continue to the next iteration
            if refactored_file_id is None:  # AI-GEN - CursorAI with GPT4
                logging.info(f"{thread_name}: RefactoringAgent: Refactoring returned None, treating as a failed attempt.")  # AI-GEN - CursorAI with GPT4
                refactoring_attempts += 1  # AI-GEN - CursorAI with GPT4
                continue  # Skip the rest of the loop and try again  # AI-GEN - CursorAI with GPT4

            code_comparator = CodeComparator(assistant_manager)

            # Compare using file IDs instead of direct code comparison
            if code_comparator.compare(original_file_id, refactored_file_id, self.rule_manager.get_rules()):
                # Download the final refactored file and save it locally
                final_refactored_code = self.assistant_manager.download_file(refactored_file_id)
                self.file_manager.write_refactored_file(file_path, final_refactored_code)
                refactoring_success = True
                logging.info(f"{thread_name}: RefactoringAgent: Refactoring successful for {file_path}")  # AI-GEN - CursorAI with GPT4
                print(f"{thread_name}: Refactoring successful for {file_path}")  # AI-GEN - CursorAI with GPT4
                self.assistant_manager.cleanup_files()  # Clean up all files related to the thread
            else:
                refactoring_attempts += 1
                # For subsequent attempts, the latest refactored version becomes the "original"
                # original_file_id = refactored_file_id
                logging.info(f"{thread_name}: RefactoringAgent: Refactoring pass did not meet goals - will retry")

        if not refactoring_success:
            print(f"{thread_name}: RefactoringAgent: Refactoring failed after {refactoring_attempts} attempts for {file_path}")  # AI-GEN - CursorAI with GPT4
            self.assistant_manager.cleanup_files()  # Clean up all files related to the thread

        # Clean up all files related to the current thread
        self.assistant_manager.cleanup_files()
        # Finally, delete the thread
        self.assistant_manager.delete_thread()

        return refactoring_success


    def refactor_code(self, original_file_id, deprecated_method, refactoring_attempts):
        thread_name = threading.current_thread().name
        """Initiates the refactoring process using the AssistantManager based on the rules."""
        logging.info(f"{thread_name}: RefactoringAgent: Initiating code refactoring...")  # AI-GEN - CursorAI with GPT4
        # Retrieve the current set of rules
        rules = self.rule_manager.get_rules()
        # Directly use the file ID for refactoring, assuming suggest_refactoring now handles file IDs and returns a file ID
        refactored_file_id = self.assistant_manager.suggest_refactoring(original_file_id, rules, deprecated_method, refactoring_attempts)
        return refactored_file_id  # AI-GEN - CursorAI with GPT4


    def extract_json_from_string(self, input_string):
        """
        Extracts a JSON object embedded within a markdown code block or plain text from the given string.

        :param input_string: The input string containing the JSON object.
        :return: A Python object parsed from the JSON string, or None if parsing fails.
        """
        # Regular expression to find a JSON object within markdown code block or plain text
        json_pattern = r'```json\n([\s\S]*?)\n```|(\[\s*\{[\s\S]*?\}\s*\])'

        match = re.search(json_pattern, input_string)
        if match:
            json_string = match.group(1) or match.group(2)  # Group 1 for markdown, Group 2 for plain JSON
            try:
                return json.loads(json_string)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
        else:
            print("No JSON object found in the input string.")
            return None

    def final_cleanup(self):
        """Calls final cleanup on each system thread's assistant manager."""
        for am in self.assistant_managers:
            am.final_cleanup()  # AI-GEN - CursorAI with GPT4
        logging.info("RefactoringAgent: Final cleanup completed for all threads.")  # AI-GEN - CursorAI with GPT4

