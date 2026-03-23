import io
from logging import Logger
import os
from typing import List, Optional
import zipfile

import requests

from NHIOTSub.models.dtos import Artifact


class ArtifactService:
    def __init__(self, logger: Logger):
        self.logger = logger
    def choose(self, artifacts: List[Artifact], target_name: str) -> Optional[Artifact]:
        return next((a for a in artifacts if a.name == target_name), None)

    def download(self, artifact: Artifact, headers: dict) -> str:
        self.logger.info(f"Downloading {artifact.name}")

        response = requests.get(artifact.archive_download_url, headers=headers)
        response.raise_for_status()

        extract_path = f"./Executables/{artifact.name}"
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(extract_path)

        return f"{extract_path}/{artifact.name}"