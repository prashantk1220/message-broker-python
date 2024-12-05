from abc import ABC
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Event(defaultdict):
    """
    Base class for all events.
    """
    time: float


@dataclass
class FileChangeEvent(Event):
    """
    Represents an event for a file change.
    """
    time: float
    diff: str
    content: str
