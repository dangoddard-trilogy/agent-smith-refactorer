import os
import logging  # AI-GEN - CursorAI with GPT4
import json

class FileManager:
    def read_file(self, file_path):
        """Reads and returns the content of a file.

        Parameters:
            file_path (str): The path to the file to be read.

        Returns:
            str: The content of the file.
        """
        logging.debug(f"FileManager: Attempting to read file at {file_path}")  # AI-GEN - CursorAI with GPT4
        try:
            with open(file_path, 'r') as file:
                content = file.read()  # AI-GEN - CursorAI with GPT4
                logging.debug(f"FileManager: Successfully read file {file_path}")  # AI-GEN - CursorAI with GPT4
                return content  # AI-GEN - CursorAI with GPT4
        except IOError as e:
            logging.error(f"FileManager: Error reading file {file_path}: {e}")  # AI-GEN - CursorAI with GPT4
            return None

    def write_refactored_file(self, original_file_path, refactored_code):
        """Writes the refactored code to a new file alongside the original file.

        Parameters:
            original_file_path (str): The path to the original file.
            refactored_code (str): The refactored code to be written to the new file.

        Returns:
            str: The path to the new refactored file.
        """
        logging.debug(f"FileManager: Preparing to write refactored file based on {original_file_path}")  # AI-GEN - CursorAI with GPT4
        # # Generating a new filename for the refactored file
        # base, ext = os.path.splitext(original_file_path)
        # new_file_path = f"{base}_refactored{ext}"

        # Assuming the user has git running, then we can safely overwrite the source file and use git diff to check the changes
        new_file_path = original_file_path
        logging.debug(f"FileManager: New file path generated: {new_file_path}")  # AI-GEN - CursorAI with GPT4

        try:
            with open(new_file_path, 'wb') as file:
                file.write(refactored_code)
                logging.debug(f"FileManager: Successfully wrote refactored file {new_file_path}")  # AI-GEN - CursorAI with GPT4
            return new_file_path
        except IOError as e:
            logging.error(f"FileManager: Error writing refactored file {new_file_path}: {e}")  # AI-GEN - CursorAI with GPT4
            return None

    def get_file_name(self, file_path):
        """Extracts and returns the file name from a file path.

        Parameters:
            file_path (str): The full path to the file.

        Returns:
            str: The file name.
        """
        logging.debug(f"FileManager: Extracting file name from path {file_path}")  # AI-GEN - CursorAI with GPT4
        return os.path.basename(file_path)  # AI-GEN - CursorAI with GPT4

    def read_source_list(self, source_list_path):
        """Reads a JSON file containing a list of file paths and their associated deprecated methods, returning these as a list of dictionaries and the count of files.

        Parameters:
            source_list_path (str): The path to the JSON file containing the list of files and deprecated methods.

        Returns:
            tuple: A tuple containing a list of dictionaries, each with the file path and its associated deprecated method, and the count of files in the list.
        """
        logging.debug(f"FileManager: Reading source list from {source_list_path}")  # AI-GEN - CursorAI with GPT4
        try:
            with open(source_list_path, 'r') as file:
                source_list = json.load(file)  # Reads the JSON file into a list of dictionaries
                logging.debug(f"FileManager: Successfully read source list from {source_list_path}")  # AI-GEN - CursorAI with GPT4
                return source_list, len(source_list)  # AI-GEN - CursorAI with GPT4
        except IOError as e:
            logging.error(f"FileManager: Error reading source list {source_list_path}: {e}")  # AI-GEN - CursorAI with GPT4
            return [], 0  # AI-GEN - CursorAI with GPT4
        except json.JSONDecodeError as e:
            logging.error(f"FileManager: Error decoding JSON from the source list at {source_list_path}: {e}")  # AI-GEN - CursorAI with GPT4
            return [], 0  # AI-GEN - CursorAI with GPT4
