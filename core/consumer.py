from typing import Callable, Dict


class Consumer:
    def __init__(self, name: str, process_function:
                    Callable[[str, Dict], None]) -> None:
        self.name = name
        self.process_function = process_function

    def receive(self, topic: str, message: Dict) -> None:
        """Process received message."""
        self.process_function(topic, message)
