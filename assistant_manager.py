from openai import OpenAI
import logging
import threading
import time

class AssistantManager:
    def __init__(self, api_key, assistant_id, organization_id):
        self.client = OpenAI(api_key=api_key, organization=organization_id)  # AI-GEN - CursorAI with GPT4
        self.thread_name = threading.current_thread().name  # AI-GEN - CursorAI with GPT4
        logging.info(f"{self.thread_name}: OpenAI client created with API key and organization ID.")  # AI-GEN - CursorAI with GPT4
        logging.info(f"{self.thread_name}: AssistantManager initialized.")  # AI-GEN - CursorAI with GPT4
        self.assistant = self.client.beta.assistants.retrieve(assistant_id)  # AI-GEN - CursorAI with GPT4
        logging.debug(f"{self.thread_name}: Retrieving assistant with ID: {assistant_id}.")  # AI-GEN - CursorAI with GPT4
        logging.info(f"{self.thread_name}: Assistant {assistant_id} retrieved.")  # AI-GEN - CursorAI with GPT4
        self.assistant_id = assistant_id  # Store for later use in creating runs  # AI-GEN - CursorAI with GPT4
        self.file_ids = []  # Initialize an empty list to store file IDs  # AI-GEN - CursorAI with GPT4
        logging.info(f"{self.thread_name}: Initialized empty list for storing file IDs.")  # AI-GEN - CursorAI with GPT4
        self.thread_id = self.create_new_thread()  # Create a new thread upon instantiation and use it throughout the class  # AI-GEN - CursorAI with GPT4
        logging.info(f"{self.thread_name}: New thread created with ID: {self.thread_id}.")  # AI-GEN - CursorAI with GPT4

    def create_new_thread(self):
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id  # Replace self.thread_id with the new thread's ID  // AI-GEN - CursorAI with GPT4
        logging.info(f"{self.thread_name}: Thread {self.thread_id} created.")  # AI-GEN - CursorAI with GPT4
        return self.thread_id  # AI-GEN - CursorAI with GPT4
    
    def delete_thread(self):
        """Deletes the thread."""
        response = self.client.beta.threads.delete(self.thread_id)
        logging.info(f"{self.thread_name}: Thread {self.thread_id} deleted.")  # AI-GEN - CursorAI with GPT4
    
    def create_message(self, instruction):
        """Creates a message in the current thread, optionally attaching files.

        Parameters:
            instruction (dict): A dictionary that contains the instruction.
                The instruction can contain the following fields:
                - content (str): The content of the message.
                - file_ids (list, optional): A list of File IDs to attach to the message.
                - metadata (dict, optional): Additional metadata to attach to the message.

        Returns:
            A message object.
        """
        # Prepare the request payload
        payload = {
            "role": "user",  # Currently, only "user" role is supported
            "content": instruction["content"]
        }

        # Format file_ids correctly as a list if provided
        if "file_ids" in instruction:
            file_ids = instruction["file_ids"]
            if isinstance(file_ids, str):
                # If file_ids is a single string, convert it to a list containing that string
                payload["file_ids"] = [file_ids]
            elif isinstance(file_ids, list):
                # If file_ids is already a list, use it directly
                payload["file_ids"] = file_ids
            else:
                logging.warning(f"{self.thread_name}: file_ids must be a string or a list of strings.")  # AI-GEN - CursorAI with GPT4
                return None

        # Create the message
        try:
            thread_message = self.client.beta.threads.messages.create(self.thread_id, **payload)
            return thread_message
        except Exception as e:
            logging.error(f"{self.thread_name}: Error creating message in thread {self.thread_id}: {e}")  # AI-GEN - CursorAI with GPT4
            return None
    
    def create_run(self):
        run = self.client.beta.threads.runs.create(thread_id=self.thread_id, assistant_id=self.assistant.id)
        logging.info(f"{self.thread_name}: Run created in thread {self.thread_id} with assistant ID {self.assistant.id}")  # AI-GEN - CursorAI with GPT4
        return run
    
    def get_run_status(self, run_id):
        run = self.client.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=run_id)
        logging.info(f"{self.thread_name}: Run status for {run_id} in thread {self.thread_id}: {run.status}")  # AI-GEN - CursorAI with GPT4
        return run
    
    def list_messages(self):
        messages = self.client.beta.threads.messages.list(self.thread_id)
        logging.info(f"{self.thread_name}: Listed messages in thread {self.thread_id}.")  # AI-GEN - CursorAI with GPT4
        return messages

    def upload_file(self, file_path):
        """Uploads a file to the assistant's file store and returns its file ID."""
        response = self.client.files.create(file=open(file_path, "rb"), purpose="assistants")
        logging.info(f"{self.thread_name}: File uploaded: {file_path}. Received ID: {response.id}")  # AI-GEN - CursorAI with GPT4
        self.file_ids.append(response.id)  # Add the new file ID to the list  # AI-GEN - CursorAI with GPT4
        return response.id

    def download_file(self, file_id):
        """Downloads the file content by its ID."""
        content = self.client.files.content(file_id)
        logging.info(f"{self.thread_name}: File downloaded with ID: {file_id}")  # AI-GEN - CursorAI with GPT4
        return content.content
    
    def delete_file(self, file_id):
        """Deletes a file from the assistant's file store by its ID."""
        try:
            self.client.files.delete(file_id)
            logging.info(f"AssistantManager: File deleted with ID: {file_id}")  # AI-GEN - CursorAI with GPT4
            if file_id in self.file_ids:
                self.file_ids.remove(file_id)  # Remove the file ID from the list after deletion  # AI-GEN - CursorAI with GPT4
        except Exception as e:
            if "404" in str(e):  # Check if the error message contains a 404 error code
                logging.info(f"AssistantManager: File with ID {file_id} is already deleted.")  # AI-GEN - CursorAI with GPT4
                if file_id in self.file_ids:
                    self.file_ids.remove(file_id)  # Ensure the file ID is removed even if already deleted  # AI-GEN - CursorAI with GPT4
            else:
                logging.error(f"AssistantManager: Failed to delete file with ID {file_id}. Error: {e}")  # AI-GEN - CursorAI with GPT4

    def list_message_files(self, message_id):
        """Lists files attached to a specific message."""
        response = self.client.beta.threads.messages.files.list(thread_id=self.thread_id, message_id=message_id)
        logging.info(f"{self.thread_name}: Listed files for message {message_id} in thread {self.thread_id}.")  # AI-GEN - CursorAI with GPT4
        return response.data  # List of file objects
    
    def retrieve_message_file(self, message_id, file_id):
        """Retrieves a specific file attached to a message."""
        file = self.client.beta.threads.messages.files.retrieve(thread_id=self.thread_id, message_id=message_id, file_id=file_id)
        logging.info(f"{self.thread_name}: Retrieved file {file_id} for message {message_id} in thread {self.thread_id}.")  # AI-GEN - CursorAI with GPT4
        return file
    
    def convert_deprecated_method_to_shorthand(self, deprecated_method):
        """Converts a deprecated method with full classpath into a shorthand method name without the classpath.

        Parameters:
            deprecated_method (str): The full classpath of the deprecated method.

        Returns:
            str: The shorthand method name without the classpath.
        """
        # Extract the shorthand method name by splitting the classpath and taking the last part
        shorthand_method_name = deprecated_method.split('.')[-1]  # AI-GEN - CursorAI with GPT4
        return shorthand_method_name  # AI-GEN - CursorAI with GPT4

    def call_agent(self, prompt):
        thread_name = threading.current_thread().name  # Get the current thread's name // AI-GEN - CursorAI with GPT4
        if not self.thread_id:
            logging.error(f"{thread_name}: AssistantManager: No thread_id set before calling call_agent.")  # AI-GEN - CursorAI with GPT4
            return None
        """Submits a prompt to the agent for processing and monitors the process."""
        logging.info(f"{thread_name}: AssistantManager: Starting agent call process...")  # AI-GEN - CursorAI with GPT4
        message = self.create_message({"content": prompt, "file_ids": self.file_ids})  # Adapted to match create_message signature // AI-GEN - CursorAI with GPT4
        run = self.create_run()  # AI-GEN - CursorAI with GPT4

        # Monitoring loop for run completion
        while run.status in ['queued', 'in_progress', 'requires_action', 'cancelling']:  # AI-GEN - CursorAI with GPT4
            time.sleep(2)  # Wait for 2 seconds before checking again // AI-GEN - CursorAI with GPT4
            run = self.get_run_status(run.id)  # AI-GEN - CursorAI with GPT4
            if run.status == 'requires_action':  # AI-GEN - CursorAI with GPT4
                logging.warning(f"{thread_name}: AssistantManager: Agent call requires action. Handling logic needed.")  # AI-GEN - CursorAI with GPT4
                break  # or handle as necessary // AI-GEN - CursorAI with GPT4

        if run.status == 'completed':  # AI-GEN - CursorAI with GPT4
            logging.info(f"{thread_name}: AssistantManager: Agent call process completed.")  # AI-GEN - CursorAI with GPT4
            thread_messages = self.list_messages()  # AI-GEN - CursorAI with GPT4
            messages = thread_messages.data if thread_messages else []  # AI-GEN - CursorAI with GPT4

            if messages:
                # Directly use the first message as it is the latest
                last_message = messages[0]  # The latest message is at index[0] // AI-GEN - CursorAI with GPT4
                if last_message.content:
                    # Assuming the content list contains dictionaries and we're interested in the 'text' of the first content item
                    analysis_result = last_message.content[0].text if last_message.content else "Analysis result unavailable."  # AI-GEN - CursorAI with GPT4
                else:
                    analysis_result = "Analysis result unavailable."  # AI-GEN - CursorAI with GPT4
            else:
                analysis_result = "Analysis result unavailable."  # AI-GEN - CursorAI with GPT4

            return analysis_result  # AI-GEN - CursorAI with GPT4
        else:
            logging.error(f"{thread_name}: AssistantManager: Agent call failed or was cancelled: {run.status}")  # AI-GEN - CursorAI with GPT4
            return None  # AI-GEN - CursorAI with GPT4

    def cleanup_files(self):  # AI-GEN - CursorAI with GPT4
        if not self.thread_id:
            logging.error("AssistantManager: No thread_id set before calling cleanup_files.")  # AI-GEN - CursorAI with GPT4
            return None
        """Deletes all files attached to each message in the thread."""
        try:
            messages = self.list_messages()  # Retrieve all messages in the thread
            for message in messages.data:
                if message.file_ids:  # Check if there are attached files
                    for file_id in message.file_ids:
                        self.delete_file(file_id)  # Delete each file
            logging.info("AssistantManager: All files in the thread have been cleaned up.")  # AI-GEN - CursorAI with GPT4
        except Exception as e:
            logging.error(f"AssistantManager: Failed to clean up files. Error: {e}")  # AI-GEN - CursorAI with GPT4

    def final_cleanup(self):
        """Deletes all files attached to each message in the thread and verifies all tracked files are deleted."""
        self.cleanup_files()  # Call the original cleanup_files method to delete files attached to messages  # AI-GEN - CursorAI with GPT4
        for file_id in list(self.file_ids):  # Iterate over a copy of the list to safely modify it during iteration  # AI-GEN - CursorAI with GPT4
            self.delete_file(file_id)  # Delete each file  # AI-GEN - CursorAI with GPT4
        if not self.file_ids:  # Check if all files have been successfully deleted  # AI-GEN - CursorAI with GPT4
            logging.info("AssistantManager: All tracked files have been successfully deleted.")  # AI-GEN - CursorAI with GPT4
        else:
            logging.error(f"AssistantManager: Some files could not be deleted: {self.file_ids}")  # AI-GEN - CursorAI with GPT4