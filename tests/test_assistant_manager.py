import unittest
from unittest.mock import patch, MagicMock, ANY
from assistant_manager import AssistantManager

class TestAssistantManager(unittest.TestCase):

    @patch('assistant_manager.OpenAI')
    def setUp(self, mock_openai):
        self.api_key = 'test_api_key'
        self.assistant_id = 'test_assistant_id'
        self.organization_id = 'test_organization_id'
        # Mock the thread creation response for the constructor
        mock_openai.return_value.beta.threads.create.return_value = MagicMock(id="init_thread_id")
        self.assistant_manager = AssistantManager(self.api_key, self.assistant_id, self.organization_id)
        self.mock_openai = mock_openai

    def test_constructor_thread_creation(self):
        # Test that a thread is created during initialization
        self.assertEqual(self.assistant_manager.thread_id, "init_thread_id")
        self.mock_openai.return_value.beta.threads.create.assert_called_once()

    def test_create_message(self):
        # Mock the message creation response
        self.mock_openai.return_value.beta.threads.messages.create.return_value = MagicMock(id="test_message_id")
        message_content = "Hello, world!"
        message = self.assistant_manager.create_message(content=message_content)
        self.assertIsNotNone(message)
        self.mock_openai.return_value.beta.threads.messages.create.assert_called_once()

    def test_upload_file(self):
            # Mock the file upload response
            self.mock_openai.return_value.files.create.return_value = MagicMock(id="test_file_id")
            file_path = "tests/test_file.txt"
            file_id = self.assistant_manager.upload_file(file_path)
            self.assertEqual(file_id, "test_file_id")
            # Use ANY for the file argument
            self.mock_openai.return_value.files.create.assert_called_once_with(file=ANY, purpose="assistants")
    
    # Add more tests here for other methods

if __name__ == '__main__':
    unittest.main()