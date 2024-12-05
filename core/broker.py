from collections import defaultdict
from typing import Dict, List

from core.event import Event


class Broker:
    def __init__(self) -> None:
        self.subscriptions: Dict[str, List["Consumer"]] = defaultdict(list)

    def subscribe(self, consumer: "Consumer", topic_pattern: str) -> None:
        """Subscribe a consumer to a topic pattern."""
        self.subscriptions[topic_pattern].append(consumer)

    def publish(self, topic: str, message: Event) -> None:
        """Publish a message to a topic."""
        for topic_pattern, consumers in self.subscriptions.items():
            if self._matches(topic, topic_pattern):
                for consumer in consumers:
                    consumer.receive(topic, message)

    def _matches(self, topic: str, topic_pattern: str) -> bool:
        """Check if a topic matches a topic pattern with wildcard."""
        if topic_pattern == "~":  # Matches all topics
            return True
        if topic_pattern.endswith("~") and topic.startswith(topic_pattern[:-1]):
            return True
        return topic == topic_pattern
