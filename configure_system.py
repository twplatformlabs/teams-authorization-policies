import sys
import os
import json
from typing import Dict

import requests

TOKEN_NOT_SET = "TOKEN_NOT_SET"
STYRA_TOKEN = os.environ.get("STYRA_API_TOKEN", TOKEN_NOT_SET)
GITHUB_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", TOKEN_NOT_SET)
STYRA_BASE_URL = "https://thoughtworks.styra.com/v1/"
COMMON_HEADERS = {
        "Authorization": f"Bearer {STYRA_TOKEN}",
        "Content-Type": "application/json"
        }

def build_request(name: str, environment: str, branch: str):
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


if len(sys.argv) != 3:
    print("Usage: python configure_system.py <environment> <branch to track>")
    sys.exit(1)

ENVIRONMENT = sys.argv[1]
BRANCH = sys.argv[2]
SYSTEM_NAME = f"lab_teams_{ENVIRONMENT}"

if STYRA_TOKEN == TOKEN_NOT_SET:
    print("Environment variable STYRA_API_TOKEN must be set")
    sys.exit(1)

if GITHUB_TOKEN == TOKEN_NOT_SET:
    print("Environment variable GITHUB_ACCESS_TOKEN must be set")
    sys.exit(1)


def create_new_system():
    headers = COMMON_HEADERS
    headers['IF-None-Match'] = "*"
    r = requests.put(STYRA_BASE_URL + f"systems/{SYSTEM_NAME}",
        timeout=5,
        data=build_request(SYSTEM_NAME, ENVIRONMENT, BRANCH),
        headers=headers)
    if r.status_code != 200:
        print("Error creating a new system")
        r.raise_for_status()
    print("Successfully created new system")


def update_existing_system():
    headers = COMMON_HEADERS
    headers['Host'] = "thoughtworks.styra.com"
    r: requests.Response = requests.put(STYRA_BASE_URL + f"systems/{SYSTEM_NAME}",
        timeout=5,
        data=build_request(SYSTEM_NAME, ENVIRONMENT, BRANCH),
        headers=headers)
    if r.status_code != 200:
        print("Error updating system")
        r.raise_for_status()
    print("Successfully updated system")

secret_payload = {"name": "twdpsio", "secret": GITHUB_TOKEN}
secret_request = requests.put(STYRA_BASE_URL + 'secrets/git/teams-policy-repo-access',
        timeout=5,
        data=secret_payload,
        headers=COMMON_HEADERS)

if secret_request.status_code != 200:
    print(f"Error creating secret with status code {secret_request.status_code}")
    secret_request.raise_for_status()
else:
    print("Successfully created secret for git credentials")

current_system_request = requests.get(STYRA_BASE_URL + f"systems/{SYSTEM_NAME}",
        timeout=5,
        headers=COMMON_HEADERS)

if current_system_request.status_code == 200:
    update_existing_system()
else:
    create_new_system()
