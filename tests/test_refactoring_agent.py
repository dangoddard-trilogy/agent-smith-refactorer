import unittest
from unittest.mock import MagicMock, patch
from refactoring_agent import RefactoringAgent

class TestRefactoringAgent(unittest.TestCase):
    @patch('refactoring_agent.FileManager')
    @patch('refactoring_agent.RuleManager')
    @patch('refactoring_agent.CodeComparator')
    def setUp(self, MockCodeComparator, MockRuleManager, MockFileManager):
        self.mock_assistant_manager = MagicMock()
        self.files_list_path = "path/to/files_list.txt"
        self.rules_path = "path/to/rules.txt"
        self.base_path = "/base/path"
        self.agent = RefactoringAgent(self.files_list_path, self.rules_path, self.mock_assistant_manager, self.base_path)
        self.MockFileManager = MockFileManager
        self.MockRuleManager = MockRuleManager
        self.MockCodeComparator = MockCodeComparator

    def test_init(self):
        self.assertEqual(self.agent.files_list_path, self.files_list_path)
        self.assertEqual(self.agent.rules_path, self.rules_path)
        self.assertEqual(self.agent.assistant_manager, self.mock_assistant_manager)
        self.assertEqual(self.agent.base_path, self.base_path)
        self.assertTrue(self.MockFileManager.called)
        self.assertTrue(self.MockRuleManager.called_with(self.rules_path))
        self.assertTrue(self.MockCodeComparator.called_with(self.mock_assistant_manager))

    @patch('refactoring_agent.os.path.join')
    def test_start_refactoring_process(self, mock_join):
        mock_file_list = ['file1.py', 'file2.py']
        self.agent.file_manager.read_files_list.return_value = mock_file_list
        mock_join.side_effect = lambda base, path: f"{base}/{path}"

        with patch.object(self.agent, 'process_file') as mock_process_file:
            self.agent.start_refactoring_process()
            self.assertEqual(mock_process_file.call_count, len(mock_file_list))
            mock_process_file.assert_any_call(f"{self.base_path}/file1.py")
            mock_process_file.assert_any_call(f"{self.base_path}/file2.py")

    @patch('refactoring_agent.os.path.join', side_effect=lambda base, path: f"{base}/{path}")
    def test_process_file(self, mock_join):
        file_path = "some/file/path.py"
        self.agent.assistant_manager.upload_file.return_value = "original_file_id"
        self.agent.assistant_manager.download_file.return_value = "refactored_code"
        self.agent.code_comparator.compare.return_value = True

        with patch.object(self.agent.file_manager, 'write_refactored_file') as mock_write:
            self.agent.process_file(file_path)
            self.agent.assistant_manager.upload_file.assert_called_once_with(file_path)
            self.assertTrue(self.agent.code_comparator.compare.called)
            mock_write.assert_called_once_with(file_path, "refactored_code")

    def test_refactor_code(self):
        original_file_id = "origFileID"
        expected_refactored_file_id = "refactoredFileID"
        self.agent.assistant_manager.suggest_refactoring.return_value = expected_refactored_file_id

        refactored_file_id = self.agent.refactor_code(original_file_id)

        self.agent.assistant_manager.suggest_refactoring.assert_called_once_with(original_file_id, self.agent.rule_manager.get_rules())
        self.assertEqual(refactored_file_id, expected_refactored_file_id)

    @patch('refactoring_agent.os.path.join', side_effect=lambda base, path: f"{base}/{path}")
    def test_process_file_failure(self, mock_join):
        file_path = "failed/refactor/path.py"
        self.agent.assistant_manager.upload_file.return_value = "original_file_id"
        self.agent.code_comparator.compare.return_value = False  # Simulate failure in comparison

        with self.assertLogs(level='INFO') as log:
            self.agent.process_file(file_path)
            if log.output:  # Check if log.output is not empty
                self.assertIn("Refactoring failed after 5 attempts for", log.output[-1])
            else:
                self.fail("Expected log message not found")

    @patch('refactoring_agent.os.path.join', side_effect=lambda base, path: f"{base}/{path}")
    def test_process_file_success(self, mock_join):
        file_path = "success/refactor/path.py"
        self.agent.assistant_manager.upload_file.return_value = "original_file_id"
        self.agent.assistant_manager.download_file.return_value = "refactored_code"
        self.agent.code_comparator.compare.return_value = True  # Simulate success in comparison

        with patch.object(self.agent.file_manager, 'write_refactored_file') as mock_write:
            self.agent.process_file(file_path)
            mock_write.assert_called_once_with(file_path, "refactored_code")

if __name__ == '__main__':
    unittest.main()