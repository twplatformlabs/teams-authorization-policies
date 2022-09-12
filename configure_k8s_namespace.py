import sys
from lib import StyraClient

if len(sys.argv) != 2:
    print("Usage: python configure_k8s_namespace.py <environment>")
    sys.exit(1)

ENVIRONMENT = sys.argv[1]
SYSTEM_NAME = f"lab_teams_{ENVIRONMENT}"

client = StyraClient(ENVIRONMENT)

print("Getting Envoyfilter")
with open('envoyfilter.yaml', 'w') as f:
    f.write(client.get_envoy_filter(SYSTEM_NAME))
    print("Writing envoyfilter.yaml")

print("Getting OPA Config")
with open('opaconfig.yaml', 'w') as f:
    f.write(client.get_opa_config(SYSTEM_NAME))
    print("Writing opaconfig.yaml")

print("Getting SLP Deployment")
with open('slp.yaml', 'w') as f:
    f.write(client.get_slp_deployment(SYSTEM_NAME))
    print("Writing slp.yaml")
