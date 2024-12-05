# Message Broker System
This is a message broker system implemented in python

The `core` package contains the broker, consumer and producer components of the message broker system.
And `tests` contains the unittest for all the modules including file-monitor system.

`file-server` is mock directory serving as storing files, which is in turn monitored by the `FileMonitorHandler`.

Any changes detected is published on the broker using the core package.
Different consumers can subscribe to different topics (file-dirs/paths) and implement custom functions as per the need.


Running the `main.py` module simulates such example to publish changes made in the file-server to the Broker which is then consumed by various consumers subscribed to the particular topics.