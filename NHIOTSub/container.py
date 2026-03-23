from NHIOTMQTT import NHIOTMQTT
from NHIOTSub.clients.GithubClient import GitHubClient
from NHIOTSub.dependencies import create_logger
from NHIOTSub.executors import Executor
from NHIOTSub.handlers import MQTTHandler
from NHIOTSub.services.ArtifactService import ArtifactService


class Container:
    def __init__(self):
        self.logger = create_logger("NHIOT")
    def mqtt_client(self):
        return NHIOTMQTT()

    def github_client(self):
        return GitHubClient(headers=..., logger=self.logger)

    def executor(self):
        return Executor(logger=self.logger)
    def artifact_service(self):
        return ArtifactService(self.logger)
    def mqtt_handler(self):
        return MQTTHandler(self.mqtt_client(), self.executor(),self.logger)