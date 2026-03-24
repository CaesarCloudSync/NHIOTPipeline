import threading
import json
import threading
import unittest
from NHIOTMQTT import NHIOTMQTT


class BaseMQTTTest(unittest.TestCase):
    publish_topic = "machineB/recv"
    subscribe_topic = "machineA/recv"
    timeout = 5

    @classmethod
    def setUpClass(cls):
        cls.client = NHIOTMQTT()
        cls.client.connect(verbose=False)

    @classmethod
    def tearDownClass(cls):
        cls.client.disconnect(verbose=False)

    def _make_callback(self, event, expected_result, parameters, expected_function):
        def callback(topic, payload):
            result_json = json.loads(payload.decode("utf-8"))
            error = result_json.get("error", "")
            device_function = result_json.get("function", "unknown")

            if device_function != expected_function:
                event.set()
                self.fail(f"[FUNCTION MISMATCH] expected '{expected_function}' got '{device_function}'")

            if error:
                event.set()
                self.fail(f"[{device_function}({parameters})] FAILED — {error}")

            result = result_json.get("result", "")
            self.assertEqual(result, expected_result, f"[{device_function}({parameters})] FAILED — expected '{expected_result}' got '{result}'")
            print(f"[{device_function}({parameters})] PASSED — result: {result}")
            event.set()
        return callback

    def run_mqtt_test(self, function_name, parameters, expected_result):
        event = threading.Event()

        callback = self._make_callback(event, expected_result,parameters, function_name)

        self.client.subscribe(
            callback,
            topic=self.subscribe_topic,
            verbose=False
        )

        self.client.publish(
            json.dumps({
                "function": function_name,
                "parameters": parameters
            }),
            topic=self.publish_topic,
            verbose=False
        )

        self.assertTrue(
            event.wait(self.timeout),
            f"No MQTT response within {self.timeout} seconds"
        )


if __name__ == "__main__":
    unittest.main()
