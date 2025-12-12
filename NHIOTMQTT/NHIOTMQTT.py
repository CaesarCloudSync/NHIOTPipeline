import uuid
from awscrt import mqtt
from awsiot import mqtt_connection_builder
from typing import Literal,Any
from concurrent.futures import Future
from NHIOTMQTT.NHIOTEnvs import NHIOTEnvs
class NHIOTMQTT:
    def __init__(self):
        # === Configuration ===
        self.ENDPOINT = NHIOTEnvs.ENDPOINT
        self.CA_FILE = NHIOTEnvs.CA_FILE
        self.CERT_FILE = NHIOTEnvs.CERT_FILE
        self.PRIVATE_KEY_FILE = NHIOTEnvs.PRIVATE_KEY_FILE
        self.TOPIC = NHIOTEnvs.TOPIC
        self.QOS = mqtt.QoS.AT_LEAST_ONCE

        # Unique client ID
        self.client_id = f"python_v2_client_{uuid.uuid4()}"



    def connect(self,verbose=True) -> Future:
        """Create and connect MQTT client"""
        if verbose: 
            print("Connecting to AWS IoT Core...")
        # === Build MQTT connection ===
        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.ENDPOINT,
            cert_filepath=self.CERT_FILE,
            pri_key_filepath=self.PRIVATE_KEY_FILE,
            ca_filepath=self.CA_FILE,
            client_id=self.client_id,
            clean_session=True,
            keep_alive_secs=30
        )
  
        connection_future = self.mqtt_connection.connect()
        connection_future.result()
        if verbose:
            print("Connected!")

    def subscribe(self, callback,verbose=True) -> Any:
        """Subscribe to a topic"""
        if not self.mqtt_connection:
            raise RuntimeError("MQTT client not connected")
        if verbose:
            print(f"Subscribing to topic '{self.TOPIC}'...")
        subscribe_future, _ = self.mqtt_connection.subscribe(
            topic=self.TOPIC,
            qos=self.QOS,
            callback=callback
        )
        subscribe_result = subscribe_future.result()
        if verbose: 
            print(f"Subscribed to topic '{self.TOPIC}'")
        return subscribe_result
 
        

    def publish(self, message,verbose=True):
        """Publish a message to the topic"""
        if not self.mqtt_connection:
            raise RuntimeError("MQTT client not connected")
        if verbose:
            print(f"[PUBLISHING] Topic: {self.TOPIC} — Message: {message}")
        self.mqtt_connection.publish(topic=self.TOPIC, payload=message, qos=self.QOS)
        if verbose: 
            print(f"Published message: {message}")

    def disconnect(self,verbose=True):
        """Disconnect the MQTT client"""
        if self.mqtt_connection:
            disconnection_future = self.mqtt_connection.disconnect()
            disconnection_future.result()
            if verbose: 
                print("Disconnected!")

