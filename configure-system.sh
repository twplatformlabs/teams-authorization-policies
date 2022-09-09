#! /bin/bash

ENVIRONMENT=$1
NAME="lab_teams_${ENVIRONMENT}"

cat <<EOF > body.json
{
  "type": "template.istio:1.0",
  "name": "${NAME}",
  "description": "authorization system for the Teams API for Environment: ${ENVIRONMENT}"
}

EOF

curl -X PUT \
  -H "Authorization: Bearer ${STYRA_API_TOKEN}" \
  -H "If-None-Match: *" \
  -H "Content-Type: application/json" \
  -d "@body.json" \
  https://thoughtworks.styra.com/v1/systems/${NAME}
