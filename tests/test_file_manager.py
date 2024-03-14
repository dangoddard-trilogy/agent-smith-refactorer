import unittest
import os
from file_manager import FileManager
from tempfile import NamedTemporaryFile, TemporaryDirectory

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.file_manager = FileManager()
        self.temp_dir = TemporaryDirectory()
        self.temp_file = NamedTemporaryFile(delete=False, dir=self.temp_dir.name)
        self.temp_file.write(b"Hello, world!")
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)
        self.temp_dir.cleanup()

    def test_read_file(self):
        content = self.file_manager.read_file(self.temp_file.name)
        self.assertEqual(content, "Hello, world!")

    def test_write_refactored_file(self):
        refactored_content = "Refactored code"
        new_file_path = self.file_manager.write_refactored_file(self.temp_file.name, refactored_content)
        self.assertTrue(os.path.exists(new_file_path))
        with open(new_file_path, 'r') as file:
            content = file.read()
        self.assertEqual(content, refactored_content)

    def test_get_file_name(self):
        file_name = self.file_manager.get_file_name(self.temp_file.name)
        self.assertEqual(file_name, os.path.basename(self.temp_file.name))

    def test_read_files_list(self):
        # Create a temporary file list
        list_file_path = os.path.join(self.temp_dir.name, "file_list.txt")
        with open(list_file_path, 'w') as list_file:
            list_file.write(self.temp_file.name + "\n")
        files_list = self.file_manager.read_files_list(list_file_path)
        self.assertEqual(files_list, [self.temp_file.name])

if __name__ == '__main__':
    unittest.main()