import unittest
from typing import Dict
from unittest.mock import patch, mock_open

from core.broker import Broker
from core.consumer import Consumer
from file_monitor import FileMonitorHandler


class TestFileMonitorHandler(unittest.TestCase):
    @patch("os.walk")
    @patch("builtins.open", new_callable=mock_open, read_data="initial content")
    def setUp(self, mock_file, mock_walk):
        mock_walk.return_value = [
            ("./file-server", ["subdir"], ["file1.txt", "file2.txt"])
        ]
        self.broker = Broker()
        self.file_handler = FileMonitorHandler(self.broker, "./file-server")
        self.file_handler.file_snapshots = {
            "file1.txt": "initial content",
            "file2.txt": "initial content",
        }

    @patch("builtins.open", new_callable=mock_open, read_data="new content")
    def test_detect_modified_file(self, mock_file):
        events = []

        def capture_event(topic: str, message: Dict):
            events.append((topic, message))

        consumer = Consumer("Logger", capture_event)
        self.broker.subscribe(consumer, "~")

        # Simulate a change in file content
        self.file_handler._check_for_changes()
        self.assertEqual(len(events), 1)
        self.assertIn("file1.txt", events[0][0])
        self.assertIn("diff", events[0][1])

    @patch("os.walk")
    @patch("builtins.open", new_callable=mock_open, read_data="initial content")
    def test_detect_new_file(self, mock_file, mock_walk):
        events = []

        def capture_event(topic: str, message: Dict):
            events.append((topic, message))

        consumer = Consumer("Logger", capture_event)
        self.broker.subscribe(consumer, "~")

        # Simulate a new file being added
        mock_walk.return_value = [
            ("./root_dir", ["subdir"], ["file1.txt", "file2.txt", "file3.txt"])
        ]
        self.file_handler._check_for_changes()
        self.assertEqual(len(events), 1)
        self.assertIn("file3.txt", events[0][0])

    @patch("os.walk")
    def test_detect_deleted_file(self, mock_walk):
        events = []

        def capture_event(topic: str, message: Dict):
            events.append((topic, message))

        consumer = Consumer("Logger", capture_event)
        self.broker.subscribe(consumer, "~")

        # Simulate a file being deleted
        mock_walk.return_value = [
            ("./root_dir", ["subdir"], ["file1.txt"])
        ]
        self.file_handler._check_for_changes()
        self.assertEqual(len(events), 0)  # Deletion doesn't trigger events
