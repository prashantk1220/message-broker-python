import unittest
from unittest.mock import patch, MagicMock
from typing import Dict

from core.broker import Broker
from core.consumer import Consumer
from file_monitor import FileMonitorHandler


class TestFileMonitorHandler(unittest.TestCase):
    """This module tests the functionality of the file-monitor
     for different event types"""

    def setUp(self):
        """
        Initialises the broker and file monitor handler and
        patches os.walk and FileMonitorHandler._read_file
        """
        patcher_walk = patch("os.walk")
        patcher_read_file = patch.object(FileMonitorHandler, "_read_file")

        self.mock_walk = patcher_walk.start()
        self.mock_read_file = patcher_read_file.start()

        # Ensure patches stop during tearDown
        self.addCleanup(patcher_walk.stop)
        self.addCleanup(patcher_read_file.stop)

        # Mock directory structure and file reading
        self.mock_walk.return_value = [
            ("./root_dir", ["subdir"], ["file1.txt", "file2.txt"])
        ]
        self.mock_read_file.side_effect = lambda x: "initial content"

        # Initialize Broker and FileMonitorHandler
        self.broker = Broker()
        self.file_handler = FileMonitorHandler(self.broker, "./root_dir")
        self.file_handler.file_snapshots = {
            "file1.txt": "initial content",
            "file2.txt": "initial content",
        }
        self.events = []

    def tearDown(self):
        # Ensure resources are reset
        self.broker = None
        self.file_handler = None
        self.events = None

    def test_detect_modified_file(self):

        def capture_event(topic: str, message: Dict):
            self.events.append((topic, message))

        consumer = Consumer("Logger", capture_event)
        self.broker.subscribe(consumer, "~")

        # Simulate a file modification
        self.mock_read_file.side_effect = (
            lambda x: "new content" if "file1" in x else "initial content"
        )
        self.file_handler._check_for_changes()

        self.assertEqual(len(self.events), 1)
        self.assertIn("file1.txt", self.events[0][0])
        self.assertNotEqual(self.events[0][1].diff, "")  # diff is not empty in the event

    def test_detect_new_file(self):

        def capture_event(topic: str, message: Dict):
            self.events.append((topic, message))

        consumer = Consumer("Logger", capture_event)
        self.broker.subscribe(consumer, "~")

        # Simulate a new file being added
        self.mock_walk.return_value = [
            ("./root_dir", ["subdir"], ["file1.txt", "file2.txt", "file3.txt"])
        ]
        self.mock_read_file.side_effect = (
            lambda x: "new content" if "file3" in x else "initial content"
        )
        self.file_handler._check_for_changes()

        self.assertEqual(len(self.events), 1)
        self.assertIn("file3.txt", self.events[0][0])
        self.assertTrue(self.events[0][1].content)  # Content is not empty

    def test_detect_deleted_file(self):
        def capture_event(topic: str, message: Dict):
            self.events.append((topic, message))

        consumer = Consumer("Logger", capture_event)
        self.broker.subscribe(consumer, "~")

        # Simulate a file being deleted
        self.mock_walk.return_value = [
            ("./root_dir", ["subdir"], ["file1.txt"])
        ]
        self.file_handler._check_for_changes()

        self.assertEqual(len(self.events), 1)
        self.assertFalse(self.events[0][1].diff)  # No Diff
        self.assertFalse(self.events[0][1].content)  # No content in the event
        self.assertNotIn("file2.txt", self.file_handler.file_snapshots)
