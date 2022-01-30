from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

api = client.AppsV1Api()

response = api.read_namespaced_deployment_status("sample-app", "devex-staging")
print (response.spec.replicas)