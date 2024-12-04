import unittest
from typing import Dict

from core.consumer import Consumer


class TestConsumer(unittest.TestCase):
    def test_consumer_receive(self):
        received_messages = []

        def callback(topic: str, message: Dict):
            received_messages.append((topic, message))

        consumer = Consumer("TestConsumer", callback)
        consumer.receive("test_topic", {"key": "value"})
        self.assertEqual(len(received_messages), 1)
        self.assertEqual(received_messages[0], ("test_topic", {"key": "value"}))

