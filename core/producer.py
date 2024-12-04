

class Producer:
    def __init__(self, broker):
        self.broker = broker

    def publish(self, topic, message):
        """Publish a message via the broker."""
        self.broker.publish(topic, message)
