import os
from dotenv import load_dotenv
load_dotenv("./NHIOTMQTT/.env")
class NHIOTEnvs:
    ENDPOINT = os.getenv("ENDPOINT")
    CA_FILE = os.getenv("CA_FILE")
    CERT_FILE = os.getenv("CERT_FILE")
    PRIVATE_KEY_FILE = os.getenv("PRIVATE_KEY_FILE")
    TOPIC = os.getenv("TOPIC")

    