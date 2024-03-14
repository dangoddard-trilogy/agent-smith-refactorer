import unittest
import sys
import logging

# Configure logging to output to the console at the DEBUG level
logging.basicConfig(level=logging.info, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    # Extract the test path from the command line arguments
    test_path_index = sys.argv.index('--test-path') + 1
    test_path = sys.argv[test_path_index] if test_path_index < len(sys.argv) else '.'
    
    # Create a test loader and discover all tests in the specified directory
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_path, pattern='test_*.py')
    
    # Run the tests
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    
    # Exit with a non-zero exit code if tests failed
    sys.exit(not result.wasSuccessful())

if __name__ == '__main__':
    main() # AI-GEN - CursorAI with GPT4