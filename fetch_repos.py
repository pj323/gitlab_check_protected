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
