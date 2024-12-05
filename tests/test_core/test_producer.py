import unittest
from unittest.mock import MagicMock
from core.producer import Producer
from core.event import FileChangeEvent


class TestProducer(unittest.TestCase):
    def setUp(self):
        self.mock_broker = MagicMock()
        self.producer = Producer(self.mock_broker)

    def test_publish_event(self):
        file_path = "file1.txt"
        diff = "Changed content"
        content = "New file content"
        self.producer.publish_event(file_path, diff, content)

        # Assert broker.publish was called with correct parameters
        self.mock_broker.publish.assert_called_once()
        args, kwargs = self.mock_broker.publish.call_args
        self.assertEqual(args[0], file_path)

        # Validate the event structure
        event = args[1]
        self.assertIsInstance(event, FileChangeEvent)
        self.assertEqual(event.diff, diff)
        self.assertEqual(event.content, content)
        self.assertTrue(hasattr(event, "time"))  # Check if time attribute exists

