import json
import os
import tempfile
import unittest
from unittest.mock import mock_open, patch

from src.json_handler import JSONHandler


class TestJSONHandler(unittest.TestCase):
    """Test cases for JSON file handling edge cases."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.json")
        self.test_data = {"key": "value"}

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            os.rmdir(self.temp_dir)

    def test_permission_handling(self):
        """Test handling of permission errors in different scenarios."""
        # Test read-only file
        with open(self.test_file, 'w') as f:
            json.dump(self.test_data, f)
        os.chmod(self.test_file, 0o444)  # Read-only
        with self.assertRaises(PermissionError):
            JSONHandler.save_to_file(self.test_data, self.test_file)

        # Test permission error through mocking
        mock_file = mock_open()
        mock_file.side_effect = PermissionError("No permission")
        with patch('builtins.open', mock_file):
            with self.assertRaises(PermissionError):
                JSONHandler.save_to_file(self.test_data, self.test_file)

    def test_invalid_json_handling(self):
        """Test handling of invalid JSON in different scenarios."""
        # Test empty file
        with open(self.test_file, 'w') as f:
            pass
        with self.assertRaises(json.JSONDecodeError):
            JSONHandler.load_from_file(self.test_file)

        # Test invalid JSON format
        with open(self.test_file, 'w') as f:
            f.write("{invalid json}")
        with self.assertRaises(json.JSONDecodeError):
            JSONHandler.load_from_file(self.test_file)

    def test_backup_creation(self):
        """Test backup creation and verification."""
        # Create initial file
        with open(self.test_file, 'w') as f:
            json.dump({"version": 0}, f)

        # Create multiple backups by saving new versions
        for i in range(1, 4):
            new_data = {"version": i}
            JSONHandler.save_to_file(new_data, self.test_file)

        # Check number of backup files
        backup_files = [
            f for f in os.listdir(
                self.temp_dir) if f.endswith('.bak')]
        self.assertEqual(
            len(backup_files),
            3,
            f"Expected 3 backup files, got {
                len(backup_files)}")

        # Verify backup contents
        backup_files.sort()  # Sort by timestamp
        for i, backup_file in enumerate(backup_files):
            backup_path = os.path.join(self.temp_dir, backup_file)
            with open(backup_path, 'r') as f:
                backup_data = json.load(f)
            self.assertEqual(
                backup_data, {
                    "version": i}, f"Backup {i} should contain version {i}, got {backup_data}")

        # Verify final file content
        with open(self.test_file, 'r') as f:
            final_data = json.load(f)
        self.assertEqual(
            final_data, {
                "version": 3}, f"Final file should contain version 3, got {final_data}")

    def test_json_data_handling(self):
        """Test handling of different JSON data structures."""
        test_cases = [{"name": "nested_json",
                       "data": {"user": {"name": "John",
                                         "address": {"city": "New York",
                                                     "zip": "10001"}}}},
                      {"name": "special_characters",
                       "data": {"text": "Special chars: !@#$%^&*()_+{}|:\"<>?",
                                "unicode": "Unicode: 你好, 世界"}},
                      {"name": "large_structure",
                       "data": {"items": [{"id": i,
                                           "value": f"item_{i}"} for i in range(1000)]}}]

        for test_case in test_cases:
            with self.subTest(test_case=test_case["name"]):
                # Save data
                JSONHandler.save_to_file(test_case["data"], self.test_file)

                # Load and verify
                loaded_data = JSONHandler.load_from_file(self.test_file)
                self.assertEqual(loaded_data, test_case["data"])

                # For large structure, verify length
                if test_case["name"] == "large_structure":
                    self.assertEqual(len(loaded_data["items"]), 1000)

    def test_concurrent_access(self):
        """Test handling of concurrent file access."""
        with open(self.test_file, 'w') as f:
            json.dump(self.test_data, f)

        # Simulate concurrent access
        with open(self.test_file, 'r') as f1, open(self.test_file, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
            self.assertEqual(data1, data2)


if __name__ == "__main__":
    unittest.main()
