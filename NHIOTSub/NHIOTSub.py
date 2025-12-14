import io
import os
import subprocess
import zipfile
import requests
import json
import time
from NHIOTSub.NHIOTSubEnvs import NHIOTSubEnvs
import time
from NHIOTMQTT import NHIOTMQTT

# --- Configuration ---
class NHIOTSub:
    def __init__(self):
        self.headers = {
            "Authorization": f"token {NHIOTSubEnvs.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        self.url = f"https://api.github.com/repos/{NHIOTSubEnvs.OWNER}/{NHIOTSubEnvs.REPO}/actions/workflows/{NHIOTSubEnvs.WORKFLOW_ID}/runs"
        self.client = NHIOTMQTT()
        self.client.connect()
    def get_latest_workflow_run(self):
        
        params = {"branch": NHIOTSubEnvs.BRANCH, "per_page": 1}
        response = requests.get(self.url, headers=self.headers, params=params)
        response.raise_for_status()
        runs = response.json()["workflow_runs"]
        if runs:
            return runs[0]
        return None
    def get_all_artefacts(self,run_id):
        url = f"https://api.github.com/repos/{NHIOTSubEnvs.OWNER}/{NHIOTSubEnvs.REPO}/actions/runs/{run_id}/artifacts"
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

    def run_artifact(self,file_path,function,parameters=[]):
        os.chmod(file_path, 0o755)
        converted_str_paremeters = list(map(str, parameters))
        result = subprocess.run([file_path,function] + converted_str_paremeters, capture_output=True, text=True)
        stdout = result.stdout
        stderr = result.stderr
        return stdout,stderr

    def monitor_workflow(self):
        print("Monitoring workflow...")

        # === Subscribe handler ===
        def on_message_received(topic, payload, **kwargs):
            payload_json = json.loads(payload.decode('utf-8'))
            print(f"[SUBSCRIBED] Topic: {topic} — Message: {payload_json}")
            function = payload_json.get("function","")
            parameters = payload_json.get("parameters",[])
            stdout,stderr = self.run_artifact(file_path,function,parameters) # TODO This will only work on the Raspberry PI becuase it was built in th AARCH architecture and not AMD.
            self.client.publish(json.dumps({"result":stdout,"error":stderr}),topic="machineA/recv")
            print(f"Workflow finished with conclusion: {conclusion}")


        

        downloaded = False

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
                    if conclusion != "success": # status == "completed" and downloaded == False
                        # "artifacts_url"
                        artifacts = self.get_all_artefacts(run_id)
                        artifact = artifacts[0]
                        file_path = self.download_artifact(artifact)
                        
                        self.client.subscribe(on_message_received,topic="machineB/recv")
                        downloaded = True

                        #return conclusion
                    time.sleep(int(NHIOTSubEnvs.POLL_INTERVAL))
        except KeyboardInterrupt:
            print("[SUBSCRIBER] Disconnecting...")
            #disconnect_future = client.disconnect()
            print("[SUBSCRIBER] Disconnected!")




