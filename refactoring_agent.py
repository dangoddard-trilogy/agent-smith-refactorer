from code_comparator import CodeComparator
from file_manager import FileManager
from rule_manager import RuleManager
import os
import logging

class RefactoringAgent:
    def __init__(self, files_list_path, rules_path, assistant_manager, base_path=""):
        logging.debug("RefactoringAgent: Initializing RefactoringAgent...")  # AI-GEN - CursorAI with GPT4
        self.files_list_path = files_list_path
        self.rules_path = rules_path
        self.assistant_manager = assistant_manager
        self.base_path = base_path  # Store the base path
        self.rule_manager = RuleManager(rules_path)
        self.file_manager = FileManager()
        self.code_comparator = CodeComparator(assistant_manager)
        self.index = 0
        self.total_files = 0
        self.passed_files = 0
        self.failed_files = 0
        logging.debug("RefactoringAgent: RefactoringAgent initialized.")  # AI-GEN - CursorAI with GPT4

    def start_refactoring_process(self):
        """Begins the process of refactoring for each file listed."""
        logging.debug("RefactoringAgent: Starting refactoring process...")  # AI-GEN - CursorAI with GPT4
        source_list, total_files = self.file_manager.read_source_list(self.files_list_path)  # Update method name and implementation to handle new JSON format
        self.total_files = total_files
        for item in source_list:
            file_path = os.path.join(self.base_path, item["path"]) if self.base_path else item["path"]
            deprecated_method = item["deprecatedMethod"]
            logging.debug(f"RefactoringAgent: Processing file: {file_path} with deprecated method: {deprecated_method}")  # AI-GEN - CursorAI with GPT4
            success = self.process_file(file_path, deprecated_method)  # Update method to accept deprecated_method as a parameter
            if success:
                self.passed_files += 1  # AI-GEN - CursorAI with GPT4
            else:
                self.failed_files += 1  # AI-GEN - CursorAI with GPT4
            self.index+=1
        
    def print_results(self):
        """Prints the summary of the refactoring process."""
        print(f"Total files processed: {self.index}")  # AI-GEN - CursorAI with GPT4
        print(f"Total files attempted: {self.total_files}")  # AI-GEN - CursorAI with GPT4
        print(f"Files successfully refactored: {self.passed_files}")  # AI-GEN - CursorAI with GPT4
        print(f"Files failed to refactor: {self.failed_files}")  # AI-GEN - CursorAI with GPT4

    def process_file(self, file_path, deprecated_method):
        """Processes each file through the refactoring pipeline."""
        print(f"Processing file {file_path} ({self.index+1}/{self.total_files})")  # AI-GEN - CursorAI with GPT4
        logging.debug(f"RefactoringAgent: Uploading original file for refactoring: {file_path}")  # AI-GEN - CursorAI with GPT4
        # The original file is uploaded to the assistant's file store
        original_file_id = self.assistant_manager.upload_file(file_path)
        refactoring_attempts = 0
        refactoring_success = False

        while not refactoring_success and refactoring_attempts < 5:
            logging.debug(f"RefactoringAgent: Refactoring attempt {refactoring_attempts + 1} for file: {file_path}")  # AI-GEN - CursorAI with GPT4
            refactored_file_id = self.refactor_code(original_file_id, deprecated_method)
            
            # If refactor_code returns None, treat it as a failed attempt and continue to the next iteration
            if refactored_file_id is None:  # AI-GEN - CursorAI with GPT4
                logging.debug("RefactoringAgent: Refactoring returned None, treating as a failed attempt.")  # AI-GEN - CursorAI with GPT4
                refactoring_attempts += 1  # AI-GEN - CursorAI with GPT4
                continue  # Skip the rest of the loop and try again  # AI-GEN - CursorAI with GPT4

            # Compare using file IDs instead of direct code comparison
            if self.code_comparator.compare(original_file_id, refactored_file_id, self.rule_manager.get_rules()):
                # Download the final refactored file and save it locally
                final_refactored_code = self.assistant_manager.download_file(refactored_file_id)
                self.file_manager.write_refactored_file(file_path, final_refactored_code)
                refactoring_success = True
                logging.debug(f"RefactoringAgent: Refactoring successful for {file_path}")  # AI-GEN - CursorAI with GPT4
                print(f"Refactoring successful for {file_path}")  # AI-GEN - CursorAI with GPT4
                self.assistant_manager.cleanup_files()  # Clean up all files related to the thread
            else:
                refactoring_attempts += 1
                # For subsequent attempts, the latest refactored version becomes the "original"
                original_file_id = refactored_file_id
                logging.debug(f"RefactoringAgent: Refactoring pass did not meet goals - will retry")

        if not refactoring_success:
            print(f"RefactoringAgent: Refactoring failed after {refactoring_attempts} attempts for {file_path}")  # AI-GEN - CursorAI with GPT4
            self.assistant_manager.cleanup_files()  # Clean up all files related to the thread

        return refactoring_success


    def refactor_code(self, original_file_id, deprecated_method):
        """Initiates the refactoring process using the AssistantManager based on the rules."""
        logging.debug("RefactoringAgent: Initiating code refactoring...")  # AI-GEN - CursorAI with GPT4
        # Retrieve the current set of rules
        rules = self.rule_manager.get_rules()
        # Directly use the file ID for refactoring, assuming suggest_refactoring now handles file IDs and returns a file ID
        refactored_file_id = self.assistant_manager.suggest_refactoring(original_file_id, rules, deprecated_method)
        return refactored_file_id  # AI-GEN - CursorAI with GPT4
