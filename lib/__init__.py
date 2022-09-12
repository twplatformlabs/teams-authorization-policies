import os
import json
from typing import Dict, Union

import requests

TOKEN_NOT_SET = "TOKEN_NOT_SET"
STYRA_TOKEN = os.environ.get("STYRA_API_TOKEN", TOKEN_NOT_SET)
GITHUB_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", TOKEN_NOT_SET)
COMMON_HEADERS = {
        "Authorization": f"Bearer {STYRA_TOKEN}",
        "Content-Type": "application/json"
        }

class StyraClient:
    def __init__(self, environment: str, host: str='thoughtworks.styra.com') -> None:
        self.prefix = f"https://{host}/v1/"
        self.env = environment
        self.headers = COMMON_HEADERS.copy()
        self.headers['Host'] = host
        if STYRA_TOKEN == TOKEN_NOT_SET:
            raise Exception("STYRA_API_TOKEN env variable not set")
        if GITHUB_TOKEN == TOKEN_NOT_SET:
            raise Exception("GITHUB_ACCESS_TOKEN env variable is not set")

    def create_or_update_system(self, name: str, branch: str):
        if self.get_system(name) is None:
            self._create_system(name, branch)
        else:
            self._update_system(name, branch)

    def get_system(self, name: str) -> Union[Dict, None]:
        request = requests.get(self.prefix + f"systems/{name}",
                timeout=5, headers=self.headers)
        if request.status_code == 404:
            return None
        return request.json()

    def ensure_git_secret_exists(self):
        secret_payload = {"name": "twdpsio", "secret": GITHUB_TOKEN}
        secret_request = requests.put(self.prefix + 'secrets/git/teams-policy-repo-access',
                timeout=5,
                data=secret_payload,
                headers=self.headers)

        if secret_request.status_code != 200:
            print(f"Error creating secret with status code {secret_request.status_code}")
            secret_request.raise_for_status()
        else:
            print("Successfully created secret for git credentials")

    def get_envoy_filter(self, system_name: str):
        request = requests.get(self.prefix + f"systems/{system_name}/assets/envoyfilter.yaml",
                timeout=5, headers=self.headers)
        request.raise_for_status()
        return request.text


    def get_opa_config(self, system_name: str):
        request = requests.get(self.prefix + f"systems/{system_name}/assets/opaconfig.yaml",
                timeout=5, headers=self.headers)
        request.raise_for_status()
        return request.text


    def get_slp_deployment(self, system_name: str):
        request = requests.get(self.prefix + f"systems/{system_name}/assets/slp.yaml",
                timeout=5, headers=self.headers)
        request.raise_for_status()
        return request.text


    def _create_system(self, name: str,  branch: str):
        headers = self.headers.copy()
        headers['IF-None-Match'] = "*"
        request = requests.put(self.prefix + f"systems/{name}",
            timeout=5,
            data=self._build_system_request(name, self.env, branch),
            headers=headers)
        if request.status_code != 200:
            print("Error creating a new system")
            request.raise_for_status()
        print("Successfully created new system")


    def _update_system(self, name: str, branch: str):
        request = requests.put(self.prefix + f"systems/{name}",
            timeout=5,
            data=self._build_system_request(name, self.env, branch),
            headers=self.headers)
        if request.status_code != 200:
            print("Error updating system")
            request.raise_for_status()
        print("Successfully updated system")


    def _build_system_request(self, name: str, environment: str, branch: str):
        return json.dumps({
          "type": "template.istio:1.0",
          "name": name,
          "description": f"authorization system for the Teams API for Environment: {environment}",
          "read_only": True,
          "source_control": {
            "origin": {
              "url": "https://github.com/ThoughtWorks-DPS/teams-authorization-policies",
              "reference": f"refs/heads/{branch}",
              "credentials": "git/teams-policy-repo-access"
            }
          }
        })


