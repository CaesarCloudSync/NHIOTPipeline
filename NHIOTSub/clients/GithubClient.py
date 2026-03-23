from typing import List, Optional

import requests

from NHIOTSub.models.dtos import Artifact, WorkflowRun
from NHIOTSub.models.responses import ArtifactsResponse, WorkflowRunsResponse


class GitHubClient:
    def __init__(self, headers: dict):
        self.headers = headers

    def get_latest_run(self, url: str) -> Optional[WorkflowRun]:
        response = requests.get(url, headers=self.headers, params={"per_page": 1})
        response.raise_for_status()
        data = WorkflowRunsResponse(**response.json())
        return data.workflow_runs[0] if data.workflow_runs else None

    def get_artifacts(self, url: str) -> List[Artifact]:
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return ArtifactsResponse(**response.json()).artifacts