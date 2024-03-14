from code_comparator import CodeComparator
from file_manager import FileManager
from rule_manager import RuleManager
import os
import logging

class RefactoringAgent:
    def __init__(self, files_list_path, rules_path, assistant_manager, base_path=""):
        logging.info("RefactoringAgent: Initializing RefactoringAgent...")  # AI-GEN - CursorAI with GPT4
        self.files_list_path = files_list_path
        self.rules_path = rules_path
        self.assistant_manager = assistant_manager
        self.base_path = base_path  # Store the base path
        self.rule_manager = RuleManager(rules_path)
        self.file_manager = FileManager()
        self.code_comparator = CodeComparator(assistant_manager)
        logging.info("RefactoringAgent: RefactoringAgent initialized.")  # AI-GEN - CursorAI with GPT4

    def start_refactoring_process(self):
        """Begins the process of refactoring for each file listed."""
        logging.info("RefactoringAgent: Starting refactoring process...")  # AI-GEN - CursorAI with GPT4
        files_list = self.file_manager.read_files_list(self.files_list_path)
        for relative_path in files_list:
            # If a base path is specified, prefix it to the file path
            file_path = os.path.join(self.base_path, relative_path) if self.base_path else relative_path
            logging.info(f"RefactoringAgent: Processing file: {file_path}")  # AI-GEN - CursorAI with GPT4
            self.process_file(file_path)

    def process_file(self, file_path):
        """Processes each file through the refactoring pipeline."""
        logging.info(f"RefactoringAgent: Uploading original file for refactoring: {file_path}")  # AI-GEN - CursorAI with GPT4
        # The original file is uploaded to the assistant's file store
        original_file_id = self.assistant_manager.upload_file(file_path)
        refactoring_attempts = 0
        refactoring_success = False

        while not refactoring_success and refactoring_attempts < 5:
            logging.info(f"RefactoringAgent: Refactoring attempt {refactoring_attempts + 1} for file: {file_path}")  # AI-GEN - CursorAI with GPT4
            refactored_file_id = self.refactor_code(original_file_id)
            
            # If refactor_code returns None, treat it as a failed attempt and continue to the next iteration
            if refactored_file_id is None:  # AI-GEN - CursorAI with GPT4
                logging.info("RefactoringAgent: Refactoring returned None, treating as a failed attempt.")  # AI-GEN - CursorAI with GPT4
                refactoring_attempts += 1  # AI-GEN - CursorAI with GPT4
                continue  # Skip the rest of the loop and try again  # AI-GEN - CursorAI with GPT4

            # Compare using file IDs instead of direct code comparison
            if self.code_comparator.compare(original_file_id, refactored_file_id, self.rule_manager.get_rules()):
                # Download the final refactored file and save it locally
                final_refactored_code = self.assistant_manager.download_file(refactored_file_id)
                self.file_manager.write_refactored_file(file_path, final_refactored_code)
                refactoring_success = True
                logging.info(f"RefactoringAgent: Refactoring successful for {file_path}")  # AI-GEN - CursorAI with GPT4
                self.assistant_manager.cleanup_files()  # Clean up all files related to the thread
            else:
                refactoring_attempts += 1
                # For subsequent attempts, the latest refactored version becomes the "original"
                original_file_id = refactored_file_id
                logging.info(f"RefactoringAgent: Refactoring pass did not meet goals - will retry")

        if not refactoring_success:
            logging.info(f"RefactoringAgent: Refactoring failed after {refactoring_attempts} attempts for {file_path}")  # AI-GEN - CursorAI with GPT4
            self.assistant_manager.cleanup_files()  # Clean up all files related to the thread


    def refactor_code(self, original_file_id):
        """Initiates the refactoring process using the AssistantManager based on the rules."""
        logging.info("RefactoringAgent: Initiating code refactoring...")  # AI-GEN - CursorAI with GPT4
        # Retrieve the current set of rules
        rules = self.rule_manager.get_rules()
        # Directly use the file ID for refactoring, assuming suggest_refactoring now handles file IDs and returns a file ID
        refactored_file_id = self.assistant_manager.suggest_refactoring(original_file_id, rules)
        return refactored_file_id  # AI-GEN - CursorAI with GPT4
