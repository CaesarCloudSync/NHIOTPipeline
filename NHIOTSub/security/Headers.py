from NHIOTSub.config import NHIOTSubEnvs


class Headers:
    github_headers = {
        "Authorization": f"token {NHIOTSubEnvs.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }