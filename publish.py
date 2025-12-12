import time
from NHIOTMQTT import NHIOTMQTT


if __name__ == "__main__":
    client = NHIOTMQTT()
    client.connect()

    # === Publish loop ===
    count = 1
    try:
        while True:
            message = f"Hello AWS IoT — Count {count}"
            client.publish(message)
            count += 1
            time.sleep(2)
    except KeyboardInterrupt:
        print("Stopping...")

    # Disconnect
    client.disconnect()
