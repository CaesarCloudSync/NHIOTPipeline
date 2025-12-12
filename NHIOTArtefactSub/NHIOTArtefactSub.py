import io
import os
import subprocess
import zipfile
import requests
import time
from NHIOTArtefactSub.NHIOTArtefactSubEnvs import NHIOTArtefactSubEnvs
import time
from NHIOTMQTT import NHIOTMQTT

# --- Configuration ---
class NHIOTArtefactSub:
    def __init__(self):
        self.headers = {
            "Authorization": f"token {NHIOTArtefactSubEnvs.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        self.url = f"https://api.github.com/repos/{NHIOTArtefactSubEnvs.OWNER}/{NHIOTArtefactSubEnvs.REPO}/actions/workflows/{NHIOTArtefactSubEnvs.WORKFLOW_ID}/runs"
        client = NHIOTMQTT()
        client.connect()
    def get_latest_workflow_run(self):
        
        params = {"branch": NHIOTArtefactSubEnvs.BRANCH, "per_page": 1}
        response = requests.get(self.url, headers=self.headers, params=params)
        response.raise_for_status()
        runs = response.json()["workflow_runs"]
        if runs:
            return runs[0]
        return None
    def get_all_artefacts(self,run_id):
        url = f"https://api.github.com/repos/{NHIOTArtefactSubEnvs.OWNER}/{NHIOTArtefactSubEnvs.REPO}/actions/runs/{run_id}/artifacts"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        artifacts = response.json()["artifacts"]
        return artifacts
    def download_artifact(self,artifact):
        name = artifact["name"]
        download_url = artifact["archive_download_url"]

        print(f"Downloading artifact '{name}'...")

        # 2. Download the artifact as a ZIP in memory
        response = requests.get(download_url, headers=self.headers, stream=True)
        response.raise_for_status()
        zip_bytes = io.BytesIO(response.content)

        # 3. Extract all files in memory to a target folder
        extract_path = f"./Executables/{name}"
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(zip_bytes) as zip_file:
            zip_file.extractall(extract_path)

        print(f"Artifact extracted to: {extract_path}")
        file_path = f"{extract_path}/{name}"
        return file_path

    def run_artifact(self,):
        subprocess.run()

    def monitor_workflow(self):
        print("Monitoring workflow...")

        # === Subscribe handler ===
        def on_message_received(topic, payload, **kwargs):
            print(f"[SUBSCRIBED] Topic: {topic} — Message: {payload.decode('utf-8')}")


        # subscribe_result = client.subscribe(on_message_received)
        try:
            while True:
                run = self.get_latest_workflow_run()
                if not run:
                    print("No workflow run found. Waiting...")
                else:
                    run_id = run["id"]
                    name = run["name"]
                    head_branch = run["head_branch"]
                    status = run["status"]  # 'queued', 'in_progress', 'completed'
                    conclusion = run.get("conclusion")  # 'success', 'failure', etc.
                    print(f"Workflow {name} {run_id} {head_branch} status: {status}, conclusion: {conclusion}")
                    if status == "completed":
                        # "artifacts_url"
                        artifacts = self.get_all_artefacts(run_id)
                        artifact = artifacts[0]
                        self.download_artifact(artifact)
                        # TODO Aafter this you would instal the app according to the 
                        print(f"Workflow finished with conclusion: {conclusion}")
                        return conclusion
                    time.sleep(int(NHIOTArtefactSubEnvs.POLL_INTERVAL))
        except KeyboardInterrupt:
            print("[SUBSCRIBER] Disconnecting...")
            #disconnect_future = client.disconnect()
            print("[SUBSCRIBER] Disconnected!")




