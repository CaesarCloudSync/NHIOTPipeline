import os
from dotenv import load_dotenv
load_dotenv("./NHIOTSub/.env")
class NHIOTSubEnvs:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    OWNER = os.getenv("OWNER")
    REPO = os.getenv("REPO")
    WORKFLOW_ID = os.getenv("WORKFLOW_ID")
    BRANCH = os.getenv("BRANCH")
    POLL_INTERVAL=os.getenv("POLL_INTERVAL")
