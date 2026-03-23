from typing import List, Optional

import requests

from NHIOTSub.config import Envs
from NHIOTSub.models.dtos import Artifact, WorkflowRun
from NHIOTSub.models.responses import ArtifactsResponse, WorkflowRunsResponse
from NHIOTSub.config import Config


class GitHubClient:
    def __init__(self):
        pass

        self.workflow_url = (
            f"{Config.BASE_URL}"
            f"{Envs.OWNER}/{Envs.REPO}"
            f"/actions/workflows/{Envs.WORKFLOW_ID}/runs"
        )
        


    def get_latest_run(self) -> Optional[WorkflowRun]:
        response = requests.get(self.workflow_url, headers=Config.GITHUB_HEADERS, params={"per_page": 1})
        response.raise_for_status()
        data = WorkflowRunsResponse(**response.json())
        return data.workflow_runs[0] if data.workflow_runs else None

    def get_artifacts(self,run: WorkflowRun) -> List[Artifact]:
        artifact_url = (
            f"{Config.BASE_URL}"
            f"{Envs.OWNER}/{Envs.REPO}"
            f"/actions/runs/{run.id}/artifacts"
        )
        response = requests.get(artifact_url, headers=Config.GITHUB_HEADERS)
        response.raise_for_status()
        return ArtifactsResponse(**response.json()).artifacts