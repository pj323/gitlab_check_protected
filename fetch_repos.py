import requests
import os
import json

# Set environment variables
access_token = os.getenv('ACCESS_TOKEN')
group_id = "your_group_id"  # Replace with your specific GitLab group ID
output_file = "repo_details.txt"

# API URLs
group_projects_url = f"https://gitlab.com/api/v4/groups/{group_id}/projects?include_subgroups=true"

# Fetch all projects in the specified group
response = requests.get(group_projects_url, headers={"PRIVATE-TOKEN": access_token})
projects = response.json()

with open(output_file, "w") as file:
    for project in projects:
        project_id = project['id']
        project_name = project['name']
        branches_url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/branches"
        
        # Fetch branches of the project
        branches_response = requests.get(branches_url, headers={"PRIVATE-TOKEN": access_token})
        branches = branches_response.json()

        # Check if 'master' or 'main' is protected
        for branch in branches:
            branch_name = branch['name']
            is_protected = branch['protected']
            if branch_name in ["master", "main"]:
                file.write(f"Repository: {project_name}, Branch: {branch_name}, Protected: {is_protected}\n")

