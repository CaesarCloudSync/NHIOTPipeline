import time
import unittest
from NHIOTMQTT import NHIOTMQTT
client = NHIOTMQTT()
client.connect()
class NHUnitPub(unittest.TestCase):
    def test_add_positive(self):
        message = f"run"
        # === Subscribe handler ===
        def on_message_received(topic, payload, **kwargs):
            print(f"[SUBSCRIBED] Topic: {topic} — Message: {payload.decode('utf-8')}")
            self.assertEqual(payload,"success")


        client.subscribe(on_message_received,topic="machineA/recv")
        client.publish(message,topic="machineB/recv")

#  client.disconnect()

