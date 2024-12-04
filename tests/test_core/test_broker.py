import unittest

from typing import Dict
from core.broker import Broker
from core.consumer import Consumer


class TestBroker(unittest.TestCase):
    def setUp(self):
        self.broker = Broker()
        self.messages = []

        def consumer_callback(topic: str, message: Dict):
            self.messages.append((topic, message))

        self.consumer = Consumer("TestConsumer", consumer_callback)

    def test_subscription(self):
        self.broker.subscribe(self.consumer, "test_topic")
        self.assertIn("test_topic", self.broker.subscriptions)
        self.assertIn(self.consumer, self.broker.subscriptions["test_topic"])

    def test_publish_to_subscribed_topic(self):
        self.broker.subscribe(self.consumer, "test_topic")
        message = {"key": "value"}
        self.broker.publish("test_topic", message)
        self.assertEqual(len(self.messages), 1)
        self.assertEqual(self.messages[0], ("test_topic", message))

    def test_publish_to_unsubscribed_topic(self):
        self.broker.subscribe(self.consumer, "other_topic")
        message = {"key": "value"}
        self.broker.publish("test_topic", message)
        self.assertEqual(len(self.messages), 0)

    def test_publish_with_wildcard(self):
        self.broker.subscribe(self.consumer, "test~")
        message = {"key": "value"}
        self.broker.publish("test_topic", message)
        self.assertEqual(len(self.messages), 1)
        self.assertEqual(self.messages[0], ("test_topic", message))

    def test_publish_to_global_wildcard(self):
        self.broker.subscribe(self.consumer, "~")
        message = {"key": "value"}
        self.broker.publish("any_topic", message)
        self.assertEqual(len(self.messages), 1)
        self.assertEqual(self.messages[0], ("any_topic", message))
