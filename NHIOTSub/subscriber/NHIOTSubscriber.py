
from logging import Logger
import time
from NHIOTMQTT.NHIOTMQTT import NHIOTMQTT
from NHIOTSub.clients.GithubClient import GitHubClient
from NHIOTSub.config import NHIOTSubEnvs
from NHIOTSub.executors.Executor import Executor
from NHIOTSub.handlers.MQTTHandler import MQTTHandler
from NHIOTSub.security.Headers import Headers
from NHIOTSub.services.ArtifactService import ArtifactService


class NHIOTSubscriber:
    def __init__(
        self,
        github : GitHubClient,
        artifacts : ArtifactService,
        executor :Executor,
        mqtt_client : NHIOTMQTT,
        mqtt_handler :MQTTHandler,
        logger : Logger,
    ):
        self.github = github 
        self.artifacts = artifacts
        self.executor = executor
        self.client = mqtt_client
        self.mqtt = mqtt_handler
        self.logger = logger

        self.client.connect()

    def monitor_workflow(self):
        downloaded = False
        file_path = None

        while True:
            run = self.github.get_latest_run()

            if not run:
                self.logger.warning("No workflow run")
                time.sleep(5)
                continue

            self.logger.info(f"{run.name} {run.status}")

            if run.status == "completed" and not downloaded:
                artifact_url = (
                    f"https://api.github.com/repos/"
                    f"{NHIOTSubEnvs.OWNER}/{NHIOTSubEnvs.REPO}"
                    f"/actions/runs/{run.id}/artifacts"
                )

                artifacts = self.github.get_artifacts(artifact_url)

                target = f"{NHIOTSubEnvs.ARTIFACT_NAME}_{NHIOTSubEnvs.SUBSCRIBER_ARCHITECTURE}"
                artifact = self.artifacts.choose(artifacts, target)

                if artifact:
                    file_path = self.artifacts.download(artifact)

                    self.client.subscribe(
                        self.mqtt.handle(file_path),
                        topic="machineB/recv"
                    )

                    downloaded = True

            elif run.status == "in_progress":
                downloaded = False

            time.sleep(int(NHIOTSubEnvs.POLL_INTERVAL))