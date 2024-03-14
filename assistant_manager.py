from openai import OpenAI
import time
import logging

class AssistantManager:
    
    def __init__(self, set_api_key, assistant_id, organization_id):
        self.client = OpenAI(api_key=set_api_key, organization=organization_id)  # AI-GEN - CursorAI with GPT4
        logging.debug("AssistantManager: AssistantManager initialized.")  # AI-GEN - CursorAI with GPT4
        self.assistant = self.client.beta.assistants.retrieve(assistant_id)
        logging.debug(f"AssistantManager: Assistant {assistant_id} retrieved.")  # AI-GEN - CursorAI with GPT4
        self.assistant_id = assistant_id  # Store for later use in creating runs
        self.thread_id = self.create_thread()  # Create a thread upon initialization - we only want a single thread for this AssistantManager instance to keep all conversation in the same context window.
        logging.debug(f"AssistantManager: Initialized with thread ID: {self.thread_id}")  # AI-GEN - CursorAI with GPT4

    def create_thread(self):
        thread = self.client.beta.threads.create()
        logging.debug(f"AssistantManager: Thread {thread.id} created.")  # AI-GEN - CursorAI with GPT4
        return thread.id
    
    def create_message(self, content, file_ids=None, metadata=None):
        """Creates a message in a given thread, optionally attaching files.

        Parameters:
            thread_id (str): The ID of the thread to create a message for.
            content (str): The content of the message.
            file_ids (list, optional): A list of File IDs to attach to the message.
            metadata (dict, optional): Additional metadata to attach to the message.

        Returns:
            A message object.
        """
        # Prepare the request payload
        payload = {
            "role": "user",  # Currently, only "user" role is supported
            "content": content
        }

        # Format file_ids correctly as a list if provided
        if file_ids is not None:
            if isinstance(file_ids, str):
                # If file_ids is a single string, convert it to a list containing that string
                payload["file_ids"] = [file_ids]
            elif isinstance(file_ids, list):
                # If file_ids is already a list, use it directly
                payload["file_ids"] = file_ids
            else:
                logging.warning("AssistantManager: file_ids must be a string or a list of strings.")  # AI-GEN - CursorAI with GPT4
                return None
        
        # Optionally include metadata if provided
        if metadata:
            payload["metadata"] = metadata

        # Create the message
        try:
            thread_message = self.client.beta.threads.messages.create(self.thread_id, **payload)
            return thread_message
        except Exception as e:
            logging.error(f"AssistantManager: Error creating message in thread {self.thread_id}: {e}")  # AI-GEN - CursorAI with GPT4
            return None
    
    def create_run(self):
        run = self.client.beta.threads.runs.create(thread_id=self.thread_id, assistant_id=self.assistant.id)
        logging.debug(f"AssistantManager: Run created in thread {self.thread_id} with assistant ID {self.assistant.id}")  # AI-GEN - CursorAI with GPT4
        return run
    
    def get_run_status(self, run_id):
        run = self.client.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=run_id)
        logging.debug(f"AssistantManager: Run status for {run_id} in thread {self.thread_id}: {run.status}")  # AI-GEN - CursorAI with GPT4
        return run
    
    def list_messages(self):
        messages = self.client.beta.threads.messages.list(self.thread_id)
        logging.debug(f"AssistantManager: Listed messages in thread {self.thread_id}.")  # AI-GEN - CursorAI with GPT4
        return messages

    def upload_file(self, file_path):
        """Uploads a file to the assistant's file store and returns its file ID."""
        response = self.client.files.create(file=open(file_path, "rb"), purpose="assistants")
        logging.debug(f"AssistantManager: File uploaded: {file_path}. Received ID: {response.id}")  # AI-GEN - CursorAI with GPT4
        return response.id

    def download_file(self, file_id):
        """Downloads the file content by its ID."""
        content = self.client.files.content(file_id)
        logging.debug(f"AssistantManager: File downloaded with ID: {file_id}")  # AI-GEN - CursorAI with GPT4
        return content.content
    
    def list_message_files(self, message_id):
        """Lists files attached to a specific message."""
        response = self.client.beta.threads.messages.files.list(thread_id=self.thread_id, message_id=message_id)
        logging.debug(f"AssistantManager: Listed files for message {message_id} in thread {self.thread_id}.")  # AI-GEN - CursorAI with GPT4
        return response.data  # List of file objects
    
    def retrieve_message_file(self, message_id, file_id):
        """Retrieves a specific file attached to a message."""
        file = self.client.beta.threads.messages.files.retrieve(thread_id=self.thread_id, message_id=message_id, file_id=file_id)
        logging.debug(f"AssistantManager: Retrieved file {file_id} for message {message_id} in thread {self.thread_id}.")  # AI-GEN - CursorAI with GPT4
        return file
    
    def delete_file(self, file_id):
        """Deletes a file from the assistant's file store by its ID."""
        try:
            self.client.files.delete(file_id)
            logging.debug(f"AssistantManager: File deleted with ID: {file_id}")  # AI-GEN - CursorAI with GPT4
        except Exception as e:
            if "404" in str(e):  # Check if the error message contains a 404 error code
                logging.debug(f"AssistantManager: File with ID {file_id} is already deleted.")  # AI-GEN - CursorAI with GPT4
            else:
                logging.error(f"AssistantManager: Failed to delete file with ID {file_id}. Error: {e}")  # AI-GEN - CursorAI with GPT4

    def cleanup_files(self):
        """Deletes all files attached to each message in the thread."""
        try:
            messages = self.list_messages()  # Retrieve all messages in the thread
            for message in messages.data:
                if message.file_ids:  # Check if there are attached files
                    for file_id in message.file_ids:
                        self.delete_file(file_id)  # Delete each file
            logging.debug("AssistantManager: All files in the thread have been cleaned up.")  # AI-GEN - CursorAI with GPT4
        except Exception as e:
            logging.error(f"AssistantManager: Failed to clean up files. Error: {e}")  # AI-GEN - CursorAI with GPT4

    def suggest_refactoring(self, original_file_id, rules, deprecated_method):
        """Initiates and monitors the refactoring process."""
        logging.debug("AssistantManager: Starting refactoring process...")  # AI-GEN - CursorAI with GPT4
        prompt = self._construct_refactoring_prompt(original_file_id, rules, deprecated_method)
        self.create_message(prompt, file_ids=[original_file_id])
        run = self.create_run()

        # Monitoring loop for run completion
        while run.status in ['queued', 'in_progress', 'requires_action', 'cancelling']:
            time.sleep(2)
            run = self.get_run_status(run.id)
            if run.status == 'requires_action':
                logging.warning("AssistantManager: Run requires action. Handling logic needed.")  # AI-GEN - CursorAI with GPT4
                break

        if run.status == 'completed':
            logging.debug("AssistantManager: Refactoring process completed.")  # AI-GEN - CursorAI with GPT4
            messages = self.list_messages()
            
            # Since messages.data[0] is the latest message, check it for file_ids
            if messages.data and messages.data[0].file_ids:
                # also log the response from the AI tool
                logging.debug(f"AssistantManager: AI Response: {messages.data[0].content}")
                # Assuming the first file ID in the latest message is the refactored file
                refactored_file_id = messages.data[0].file_ids[0]
                if refactored_file_id != original_file_id:
                    # content = self.download_file(refactored_file_id)
                    logging.debug("AssistantManager: Refactored file_id retrieved.")  # AI-GEN - CursorAI with GPT4
                    return refactored_file_id
            else:
                logging.debug("AssistantManager: No refactored file found.")  # AI-GEN - CursorAI with GPT4
                return None
        else:
            logging.error(f"AssistantManager: Refactoring failed or was cancelled: {run.status}")  # AI-GEN - CursorAI with GPT4
            return None

    def _construct_refactoring_prompt(self, original_file_id, rules, deprecated_method):
        """Constructs a detailed prompt or command for the assistant to refactor the code."""
        prompt = f"Please refactor all instances of method {deprecated_method} in file {original_file_id} following these rules: {rules}"
        logging.debug(f"AssistantManager: Refactoring prompt constructed: {prompt}")  # AI-GEN - CursorAI with GPT4
        return prompt
    
    def analyze_code(self, prompt, file_ids):
        """Submits a prompt for code analysis and monitors the process."""
        logging.debug("AssistantManager: Starting code analysis process...")  # AI-GEN - CursorAI with GPT4
        message = self.create_message(prompt, file_ids)  # Assuming adaptation to accept 'prompt'
        run = self.create_run()

        # Monitoring loop for run completion
        while run.status in ['queued', 'in_progress', 'requires_action', 'cancelling']:
            time.sleep(2)  # Wait for 5 seconds before checking again
            run = self.get_run_status(run.id)
            if run.status == 'requires_action':
                logging.warning("AssistantManager: Analysis run requires action. Handling logic needed.")  # AI-GEN - CursorAI with GPT4
                break  # or handle as necessary

        if run.status == 'completed':
            logging.debug("AssistantManager: Code analysis process completed.")  # AI-GEN - CursorAI with GPT4
            thread_messages = self.list_messages()
            messages = thread_messages.data if thread_messages else []

            if messages:
                # Directly use the first message as it is the latest
                last_message = messages[0]  # The latest message is at index[0]
                if last_message.content:
                    # Assuming the content list contains dictionaries and we're interested in the 'text' of the first content item
                    analysis_result = last_message.content[0].text.value if last_message.content else "Analysis result unavailable."
                else:
                    analysis_result = "Analysis result unavailable."
            else:
                analysis_result = "Analysis result unavailable."

            return analysis_result
        else:
            logging.error(f"AssistantManager: Analysis failed or was cancelled: {run.status}")  # AI-GEN - CursorAI with GPT4
            return "Analysis failed or was cancelled."
