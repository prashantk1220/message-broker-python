import time
from typing import Dict

from core.broker import Broker
from core.consumer import Consumer
from file_monitor import FileMonitorHandler


ROOT_DIR = "./file-server"
broker = Broker()


# Example consumer
def print_changes(topic: str, message: Dict) -> None:
    print(f"Change detected in {topic} at {time.ctime(message['time'])}")
    print(f"Diff:\n{message['diff']}")


consumer = Consumer("FileChangeLogger", print_changes)
broker.subscribe(consumer, "~")


def process_important_files(topic, message):
    """Process changes to important files."""
    print(f"[Important] {topic}: {message['diff']}")


def audit_all_files(topic, message):
    """Log changes to all files."""
    with open("audit.log", "a") as log_file:
        log_file.write(f"{time.ctime(message['time'])}, {topic}\n")


# Important files consumer
important_consumer = Consumer("ImportantFileProcessor", process_important_files)
broker.subscribe(important_consumer, "important_stuff/~")

# Audit log consumer
audit_consumer = Consumer("AuditLogger", audit_all_files)
broker.subscribe(audit_consumer, "~")


# Start file monitoring
file_monitor = FileMonitorHandler(broker, ROOT_DIR)
file_monitor.start()
