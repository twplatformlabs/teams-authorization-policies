#! /bin/bash

ENVIRONMENT=$1
BRANCH=$2
NAME="lab_teams_${ENVIRONMENT}"

if [ ! ${ENVIRONMENT} ]; then
  echo "Usage: ./configure-system.sh <environment> <branch>"
  exit 1
fi

if [ ! ${BRANCH} ]; then
  echo "Usage: ./configure-system.sh <environment> <branch>"
  exit 1
fi

cat <<EOF > secret.json
{
  "name": "twdpsio",
  "secret": "${GITHUB_ACCESS_TOKEN}"
}
EOF

cat <<EOF > body.json
{
  "type": "template.istio:1.0",
  "name": "${NAME}",
  "description": "authorization system for the Teams API for Environment: ${ENVIRONMENT}",
  "read_only": true,
  "source_control": {
    "origin": {
      "url": "https://github.com/ThoughtWorks-DPS/teams-authorization-policies",
      "reference": "refs/heads/${BRANCH}",
      "credentials": "git/teams-policy-repo-access"
    }
  }
}

EOF

echo "Ensuring repo access secrets are created"

curl -X PUT \
  -H "Authorization: Bearer ${STYRA_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "@secret.json" \
  https://thoughtworks.styra.com/v1/secrets/git/teams-policy-repo-access

echo "Ensured secret exists, pausing for eventual consistency"
sleep 5

echo "Creating/Updating system for ${NAME}"

curl -X PUT \
  -H "Authorization: Bearer ${STYRA_API_TOKEN}" \
  -H "If-None-Match: *" \
  -H "Content-Type: application/json" \
  -d "@body.json" \
  https://thoughtworks.styra.com/v1/systems/${NAME}
