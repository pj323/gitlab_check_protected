import json
from urllib import request, error
import os

def fetch_and_check_repos(group_id, access_token):
    # Set the base URL for GitLab API
    base_url = "https://gitlab.com/api/v4"
    
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

    # Fetch all projects in the specified group
    projects_url = f"{base_url}/groups/{group_id}/projects?include_subgroups=true&per_page=100"
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
    ACCESS_TOKEN = os.getenv('GITLAB_TOKEN')
    GROUP_ID = os.getenv('GITLAB_GROUP_ID')

    fetch_and_check_repos(GROUP_ID, ACCESS_TOKEN)
