import requests
import time

# --- Configuration ---
GITHUB_TOKEN = "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"
OWNER = "CaesarCloudSync"
REPO = "NHIOTPipeline"
WORKFLOW_ID = "main.yml"  # workflow file name or workflow ID
BRANCH = "main"
POLL_INTERVAL = 10  # seconds

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_latest_workflow_run():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_ID}/runs"
    params = {"branch": BRANCH, "per_page": 1}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    runs = response.json()["workflow_runs"]
    if runs:
        return runs[0]
    return None

def monitor_workflow():
    print("Monitoring workflow...")
    while True:
        run = get_latest_workflow_run()
        if not run:
            print("No workflow run found. Waiting...")
        else:
            status = run["status"]  # 'queued', 'in_progress', 'completed'
            conclusion = run.get("conclusion")  # 'success', 'failure', etc.
            print(f"Workflow status: {status}, conclusion: {conclusion}")
            if status == "completed":
                print(f"Workflow finished with conclusion: {conclusion}")
                return conclusion
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    monitor_workflow()
