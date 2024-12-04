# Message Broker System
This is a message broker system implemented in python

The core-package contains the broker, consumer and optional producer components of the message broker system.

In this project it is used to monitor the changes in the file-server directory.

Running the `main.py` module simulates such example to publish changes made in the file-server to the Broker which is then consumed by various consumers subscribed to the particular topics.