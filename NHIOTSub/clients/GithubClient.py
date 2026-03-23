from typing import List, Optional

import requests

from NHIOTSub.config import NHIOTSubEnvs
from NHIOTSub.models.dtos import Artifact, WorkflowRun
from NHIOTSub.models.responses import ArtifactsResponse, WorkflowRunsResponse
from NHIOTSub.security import Headers


class GitHubClient:
    def __init__(self):
        pass

        self.workflow_url = (
            f"https://api.github.com/repos/"
            f"{NHIOTSubEnvs.OWNER}/{NHIOTSubEnvs.REPO}"
            f"/actions/workflows/{NHIOTSubEnvs.WORKFLOW_ID}/runs"
        )


    def get_latest_run(self) -> Optional[WorkflowRun]:
        response = requests.get(self.workflow_url, headers=Headers.github_headers, params={"per_page": 1})
        response.raise_for_status()
        data = WorkflowRunsResponse(**response.json())
        return data.workflow_runs[0] if data.workflow_runs else None

    def get_artifacts(self, url: str) -> List[Artifact]:
        response = requests.get(url, headers=Headers.github_headers)
        response.raise_for_status()
        return ArtifactsResponse(**response.json()).artifacts