import json

# LastUpdate would be an update on GitHub repo
from RepoGithub import scanGithubRepo

# Load previous data
tools = json.loads(open('data-tools-old.json').read(), encoding='utf-8')
# print(tools)
# print(tools[1]['name'])


scanGithubRepo(tools)# Write the updated data

with open('data-tools.json', mode='w', encoding='utf-8') as f:
    json.dump(tools, f, indent=2)


