import time
from core.broker import Broker
from core.event import FileChangeEvent


class Producer:
    """
    Handles the production of file change events.
    """
    def __init__(self, broker: Broker):
        """
        Initializes the Producer.

        :param broker: The message broker to publish events.
        """
        self.broker = broker

    def publish_event(self, file_path: str, diff: str = "", current_content: str = "") -> None:
        """
        Publishes an event for a file change.

        :param file_path: The relative path of the changed file.
        :param diff: The diff of changes made to the file.
        :param current_content: The current content of the file.
        """
        event = FileChangeEvent(time=time.time(), diff=diff, content=current_content)
        self.broker.publish(file_path, event)
