import time
from NHIOTMQTT import NHIOTMQTT



if __name__ == "__main__":
    print("Connecting to AWS IoT Core...")
    client = NHIOTMQTT()
    client.connect()


    # === Subscribe handler ===
    def on_message_received(topic, payload, **kwargs):
        print(f"[SUBSCRIBED] Topic: {topic} — Message: {payload.decode('utf-8')}")


    subscribe_result = client.subscribe(on_message_received)
    # Keep subscriber running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[SUBSCRIBER] Disconnecting...")
        disconnect_future = client.disconnect()
        print("[SUBSCRIBER] Disconnected!")
