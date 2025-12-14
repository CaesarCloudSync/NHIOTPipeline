import time
import json
import unittest
from functools import partial
from NHIOTMQTT.NHIOTMQTT import NHIOTMQTT



import threading


class NHUnitPub(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = NHIOTMQTT()
        cls.client.connect(verbose=False)

    @classmethod
    def tearDownClass(cls):
        cls.client.disconnect(verbose=False)

    def _run_mqtt_test(
        self,
        function_name,
        parameters,
        expected_result,
        publish_topic="machineB/recv",
        subscribe_topic="machineA/recv",
        timeout=5,
    ):
        """
        Generic MQTT test helper
        """
        event = threading.Event()

        def on_message_received(topic, payload, expected_value):
            result_json = json.loads(payload.decode("utf-8"))
            result = result_json.get("result", "")
            self.assertEqual(result, expected_value)
            event.set()

        wrapped = partial(on_message_received, expected_value=expected_result)

        self.client.subscribe(wrapped, topic=subscribe_topic,verbose=False)

        self.client.publish(
            json.dumps({
                "function": function_name,
                "parameters": parameters
            }),
            topic=publish_topic
            ,verbose=False
        )

        # Wait for response or timeout
        self.assertTrue(
            event.wait(timeout),
            f"Did not receive MQTT response within {timeout} seconds"
        )

    # === Tests ===

    def test_add_positive(self):
        self._run_mqtt_test(
            function_name="add",
            parameters=[1, 2],
            expected_result="3",
        )

    def test_add_negative(self):
        self._run_mqtt_test(
            function_name="add",
            parameters=[-5, 2],
            expected_result="-3",
        )

    def test_multiply(self):
        self._run_mqtt_test(
            function_name="multiply",
            parameters=[3, 4],
            expected_result="12",
        )
    def test_multiply_2(self):
        self._run_mqtt_test(
            function_name="multiply",
            parameters=[8, 7],
            expected_result="56",
        )


if __name__ == "__main__":
    unittest.main()
