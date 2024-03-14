import unittest
from unittest.mock import patch, mock_open
from rule_manager import RuleManager
import json
import os

class TestRuleManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestRuleManager, cls).setUpClass()
        cls.rules_path = "./tests/test_rules.json"
        assert os.path.exists(cls.rules_path), f"Rules file does not exist at {cls.rules_path}"
        cls.sample_rules = {
            "deprecatedMethods": ["old_method1", "old_method2"],
            "refactoringDescription": "Use new_method instead of old_method"
        }
        # Patching here to ensure RuleManager instance uses mocked data
        with patch("builtins.open", mock_open(read_data=json.dumps(cls.sample_rules))), \
             patch("json.load", return_value=cls.sample_rules):
            cls.manager = RuleManager(cls.rules_path)

    def test_load_rules_success(self):
        self.assertEqual(self.manager.rules, self.sample_rules)

    def test_get_deprecated_methods(self):
        self.assertEqual(self.manager.get_deprecated_methods(), ["old_method1", "old_method2"])

    def test_get_refactoring_description(self):
        self.assertEqual(self.manager.get_refactoring_description(), "Use new_method instead of old_method")

    def test_get_rules(self):
        self.assertEqual(self.manager.get_rules(), self.sample_rules)

# Additional tests for error scenarios can be implemented similarly,
# but might require individual setup or patching depending on the case.

if __name__ == '__main__':
    unittest.main()