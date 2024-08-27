import json
from urllib import request, error
import os

def fetch_and_check_repos(group_path, access_token):
    # Set the base URL for your GitLab instance's API
    base_url = "https://sfgitlab.opr.statefarm.org/api/v4"
    
    # Prepare the header for authorization
    headers = {
        'Private-Token': access_token
    }

    # Function to make HTTP GET requests
    def make_request(url):
        req = request.Request(url, headers=headers)
        try:
            with request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except error.URLError as e:
            print(f"Failed to fetch data: {e.reason}")
            return None

    # Use the full path to specify the group, e.g., "groups/Turing"
    projects_url = f"{base_url}/groups/{group_path}/projects?include_subgroups=true&per_page=100"
    projects = make_request(projects_url)

    if projects is None:
        return

    # Iterate over each project
    for project in projects:
        project_id = project['id']
        project_name = project['name']
        branches_url = f"{base_url}/projects/{project_id}/repository/branches"
        
        # Fetch branches
        branches = make_request(branches_url)

        if branches is None:
            continue

        # Check if 'master' or 'main' is protected
        for branch in branches:
            if branch['name'] in ['master', 'main']:
                print(f"Repository: {project_name}, Branch: {branch['name']}, Protected: {branch['protected']}")

if __name__ == "__main__":
    # Environment variables
    ACCESS_TOKEN = os.getenv('GITLAB_ACCESS_TOKEN')
    GROUP_PATH = os.getenv('GITLAB_GROUP_PATH')  # Use the group's path instead of ID for clarity

    fetch_and_check_repos(GROUP_PATH, ACCESS_TOKEN)








1. Instance Identification
Input: The pipeline should accept the instance name as an input parameter.
Search Mechanism: Implement a search mechanism that queries all namespaces across both clusters (EDCO and EDCR) to locate the instance. This can be done using kubectl commands like kubectl get pods --all-namespaces -o wide | grep <instance-name>.
2. Retrieve Instance Details
Namespace & Cluster: Identify and output the namespace and cluster where the instance is located.
Pod Details: Fetch detailed information about the pod, including:
Resource Limits (CPU, Memory)
Environment Variables
Volume Mounts
Container Status (image, restart count)
Annotations and Labels
StatefulSet (STS) Information: If the instance is part of a StatefulSet:
Fetch the StatefulSet manifest details (replicas, update strategy, resource requests/limits, etc.)
Check for any failed or pending updates.
Service & Ingress: Fetch associated Services, Ingresses, and ConfigMaps linked to the instance for network and configuration context.
Logs: Pull the latest logs from the pod to check for any immediate errors or warnings.
Events: Retrieve events from the namespace for any warnings or errors related to the pod or associated resources using kubectl get events --namespace <namespace> | grep <instance-name>.
3. Instance Health Check
Ping & Probe: Implement a simple health check by pinging the instance and checking the liveness and readiness probes. You can use kubectl exec to ping or curl the service endpoint internally within the cluster.
Resource Utilization: Monitor current resource utilization of the pod (CPU, Memory) using kubectl top pod <pod-name> --namespace <namespace>.
4. Output Reporting
Detailed Report: Generate a detailed report summarizing all the information gathered:
Instance location (Namespace, Cluster)
Pod details (Resources, Status, Logs)
StatefulSet details (if applicable)
Service, Ingress, ConfigMaps
Health Check Results
Events and Logs
Alerting: If any issues are detected (e.g., failing probes, resource limits exceeded, or errors in logs), trigger an alerting mechanism (e.g., sending notifications to Slack, email, etc.).
5. Automation & CI/CD Integration
GitLab CI/CD Pipeline: Define the pipeline stages in your gitlab-ci.yml:
Search & Locate Stage: Run a script that searches and identifies the instance location.
Details Fetching Stage: Execute a script to gather all the details and run health checks.
Reporting Stage: Collate all information and create a detailed report, pushing the results to a central location (e.g., an S3 bucket, GitLab artifact).
Parallelization: If applicable, parallelize certain stages (e.g., fetching details from multiple namespaces) to speed up the process.
