import requests


class GithubUserRetriever:
    def user(self, username: str) -> dict[str, str]:
        response = requests.get("https://api.github.com/users/USERNAME/orgs")
        return response.json()
