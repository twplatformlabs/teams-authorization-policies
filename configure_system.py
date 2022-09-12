import sys
from lib import StyraClient

if len(sys.argv) != 3:
    print("Usage: python configure_system.py <environment> <branch to track>")
    sys.exit(1)

ENVIRONMENT = sys.argv[1]
BRANCH = sys.argv[2]
SYSTEM_NAME = f"lab_teams_{ENVIRONMENT}"

client = StyraClient(ENVIRONMENT)

client.ensure_git_secret_exists()

client.create_or_update_system(SYSTEM_NAME, BRANCH)
