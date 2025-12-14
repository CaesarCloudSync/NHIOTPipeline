import time
import json
import unittest
from functools import partial
from NHIOTMQTT.NHIOTMQTT import NHIOTMQTT


class NHUnitPub(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = NHIOTMQTT()
        cls.client.connect()

    @classmethod
    def tearDownClass(cls):
        cls.client.disconnect()

    def test_add_positive(self):
        expected = "success"

        # === Subscribe handler ===
        def on_message_received(topic, payload, expected_value):
            print(f"[SUBSCRIBED] Topic: {topic} — Message: {payload.decode('utf-8')}")
            self.assertEqual(payload.decode("utf-8"), expected_value)

        # Wrap handler with kwargs
        wrapped = partial(on_message_received, expected_value=expected)

        # Subscribe to topic
        self.client.subscribe(wrapped, topic="machineA/recv")

        # Publish message
        
        self.client.publish(json.dumps({"function":"add","parameters":[1,2]}), topic="machineB/recv")

        # Wait for MQTT delivery
        time.sleep(2)  # Adjust if needed


if __name__ == "__main__":
    unittest.main()
