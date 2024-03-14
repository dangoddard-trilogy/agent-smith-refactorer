import json
import logging  # AI-GEN - CursorAI with GPT4
import os

class RuleManager:
    def __init__(self, rules_path):
        logging.info(f"RuleManager: Initializing RuleManager with rules path: {rules_path}")  # AI-GEN - CursorAI with GPT4
        self.rules = self.load_rules(rules_path)

    def load_rules(self, rules_path):
        """Loads the refactoring rules from a JSON file."""
        try:
            logging.info(f"Attempting to open rules file at absolute path: {os.path.abspath(rules_path)}")
            with open(rules_path, 'r') as file:
                rules = json.load(file)
                logging.info(f"RuleManager: Successfully loaded rules from {rules_path}")  # AI-GEN - CursorAI with GPT4
                return rules
        except FileNotFoundError:
            logging.error(f"RuleManager: Rules file not found at {rules_path} Error: {e}")  # AI-GEN - CursorAI with GPT4
            return {}
        except json.JSONDecodeError:
            logging.error(f"RuleManager: Error decoding JSON from the rules file at {rules_path} Error: {e}")  # AI-GEN - CursorAI with GPT4
            return {}

    def get_refactoring_description(self):
        """Returns a description of the required refactoring."""
        description = self.rules.get("refactoringDescription", [])  # AI-GEN - CursorAI with GPT4
        logging.info("RuleManager: Retrieving refactoring description")  # AI-GEN - CursorAI with GPT4
        return description

    def get_rules(self):
        """Returns the entire set of refactoring rules."""
        logging.info("RuleManager: Retrieving all refactoring rules")  # AI-GEN - CursorAI with GPT4
        logging.info(f"RuleManager: Current rules: {self.rules}") 
        return self.rules

    # Additional methods to query or manipulate rules can be added here
