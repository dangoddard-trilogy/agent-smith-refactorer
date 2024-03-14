import unittest
from unittest.mock import MagicMock, patch
from code_comparator import CodeComparator

class TestCodeComparator(unittest.TestCase):
    def setUp(self):
        # Mock the assistant_manager to be used in tests
        self.mock_assistant_manager = MagicMock()
        self.code_comparator = CodeComparator(self.mock_assistant_manager)

    def test_generate_analysis_prompt(self):
        # Test the prompt generation with a simple rule set
        original_file_id = "origFile123"
        refactored_file_id = "refactoredFile123"
        rules = {"rule1": "Do not use global variables"}
        expected_prompt_start = "Analyze the refactoring changes made from the original file (ID: origFile123) to the refactored file (ID: refactoredFile123)."
        generated_prompt = self.code_comparator._generate_analysis_prompt(original_file_id, refactored_file_id, rules)
        
        self.assertIn(expected_prompt_start, generated_prompt)  # Check if the prompt starts with the expected text
        self.assertIn("Do not use global variables", generated_prompt)  # Check if the rule is included in the prompt

    def test_interpret_analysis_result_correct(self):
        # Test interpretation of a correct analysis result
        analysis_result = '{"result": "Yes", "details": "Refactoring is correct."}'
        self.assertTrue(self.code_comparator._interpret_analysis_result(analysis_result))  # Should return True

    def test_interpret_analysis_result_incorrect(self):
        # Test interpretation of an incorrect analysis result
        analysis_result = '{"result": "No", "details": "Refactoring violates rules."}'
        self.assertFalse(self.code_comparator._interpret_analysis_result(analysis_result))  # Should return False

    def test_compare_method(self):
        # Mocking the assistant_manager's analyze_code method
        self.mock_assistant_manager.analyze_code.return_value = '{"result": "Yes", "details": "Refactoring is correct."}'
        original_file_id = "origFile123"
        refactored_file_id = "refactoredFile123"
        rules = {"rule1": "Do not use global variables"}

        # Test the compare method
        result = self.code_comparator.compare(original_file_id, refactored_file_id, rules)
        self.assertTrue(result)  # Expect True since the mock returns a 'Yes' result

    def test_parse_analysis_result(self):
        # Test the parse_analysis_result method
        analysis_result = "```json\n{\"result\": \"Yes\", \"details\": \"Refactoring is correct.\"}\n```"
        expected_result = "{\"result\": \"Yes\", \"details\": \"Refactoring is correct.\"}"
        parsed_result = self.code_comparator._parse_analysis_result(analysis_result)
        self.assertEqual(parsed_result, expected_result)  # Check if the parsing is correct

    @patch.object(CodeComparator, '_parse_analysis_result')
    def test_interpret_analysis_result_with_parsing(self, mock_parse):
        # Mock _parse_analysis_result to return a specific JSON string
        mock_parse.return_value = '{"result": "Yes", "details": "Refactoring is correct."}'
        
        # Directly test _interpret_analysis_result assuming _parse_analysis_result works correctly
        analysis_result = "Some raw analysis result"
        result = self.code_comparator._interpret_analysis_result(analysis_result)
        self.assertTrue(result)  # Expect True since the mock returns a 'Yes' result

        # Ensure _parse_analysis_result was called with the raw analysis result
        mock_parse.assert_called_once_with(analysis_result)

if __name__ == '__main__':
    unittest.main()