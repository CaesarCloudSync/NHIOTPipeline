
import time
from NHIOTSub.config import NHIOTSubEnvs


class NHIOTSubscriber:
    def __init__(
        self,
        github,
        artifacts,
        executor,
        mqtt_client,
        mqtt_handler,
        logger,
    ):
        self.github = github
        self.artifacts = artifacts
        self.executor = executor
        self.client = mqtt_client
        self.mqtt = mqtt_handler
        self.logger = logger

        self.headers = {
            "Authorization": f"token {NHIOTSubEnvs.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

        self.workflow_url = (
            f"https://api.github.com/repos/"
            f"{NHIOTSubEnvs.OWNER}/{NHIOTSubEnvs.REPO}"
            f"/actions/workflows/{NHIOTSubEnvs.WORKFLOW_ID}/runs"
        )

        self.client.connect()

    def monitor_workflow(self):
        downloaded = False
        file_path = None

        while True:
            run = self.github.get_latest_run(self.workflow_url)

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
                    file_path = self.artifacts.download(artifact, self.headers)

                    self.client.subscribe(
                        self.mqtt.handle(file_path),
                        topic="machineB/recv"
                    )

                    downloaded = True

            elif run.status == "in_progress":
                downloaded = False

            time.sleep(int(NHIOTSubEnvs.POLL_INTERVAL))