from typing import Callable

from core.event import Event


class Consumer:
    def __init__(self, name: str, process_function:
                    Callable[[str, Event], None]) -> None:
        self.name = name
        self.process_function = process_function

    def receive(self, topic: str, message: Event) -> None:
        """Process received message."""
        self.process_function(topic, message)
