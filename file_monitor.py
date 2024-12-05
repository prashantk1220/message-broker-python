import os
import time
from typing import Dict
import difflib

from core.producer import Producer


class FileMonitorHandler:
    def __init__(self, broker: "Broker", root_directory: str, interval: float = 1.0) -> None:
        """
        Initializes the file monitor.

        :param broker: The message broker instance for publishing events.
        :param root_directory: The directory to monitor.
        :param interval: Polling interval in seconds.
        """
        self.broker = broker
        self.producer = Producer(broker)
        self.root_directory = root_directory
        self.interval = interval
        self.file_snapshots: Dict[str, str] = self._snapshot_directory()

    def start(self) -> None:
        """Starts monitoring the directory."""
        print(f"Starting file monitoring in {self.root_directory}...")
        try:
            while True:
                self._check_for_changes()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("Stopping file monitoring.")

    def _snapshot_directory(self) -> Dict[str, str]:
        """
        Takes a snapshot of the directory, storing the content of each file.

        :return: A dictionary mapping relative file paths to their content.
        """
        snapshots = {}
        for root, _, files in os.walk(self.root_directory):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, self.root_directory)
                snapshots[relative_path] = self._read_file(full_path)
        return snapshots

    def _check_for_changes(self) -> None:
        """Checks for changes in the monitored directory."""
        current_snapshot = self._snapshot_directory()

        # Check for modified or added files
        for file_path, current_content in current_snapshot.items():
            previous_content = self.file_snapshots.get(file_path)
            if previous_content is None:
                # New file detected
                print(f"New file detected: {file_path}")
                self.producer.publish_event(file_path, "", current_content)
            elif current_content != previous_content:
                # File modified
                diff = self._generate_diff(previous_content, current_content)
                print(f"File modified: {file_path}")
                self.producer.publish_event(file_path, diff, "")

        # Check for deleted files
        for file_path in list(self.file_snapshots.keys()):
            if file_path not in current_snapshot:
                print(f"File deleted: {file_path}")
                del self.file_snapshots[file_path]
                self.producer.publish_event(file_path, "", "")

        # Update the snapshot
        self.file_snapshots = current_snapshot

    def _read_file(self, file_path: str) -> str:
        """
        Reads the content of a file.

        :param file_path: The full path of the file to read.
        :return: The content of the file as a string.
        """
        try:
            # Explicitly flush OS-level cache for the file
            os.sync()
            with open(file_path, 'r') as f:
                return f.read()
        except (FileNotFoundError, IOError):
            return ""

    def _generate_diff(self, old_content: str, new_content: str) -> str:
        """
        Generates a diff between two versions of file content.

        :param old_content: The old file content.
        :param new_content: The new file content.
        :return: A string representing the diff.
        """
        return "\n".join(difflib.unified_diff(
            old_content.splitlines(),
            new_content.splitlines(),
            lineterm=""
        ))
