import json
import Config
from RepoGithub import scan_github_repo

# Load previous data
tools = json.loads(open('data-tools-old.json').read(), encoding='utf-8')
# print(tools)
# print(tools[1]['name'])


scan_github_repo(tools, Config.GitHubToken)
# Should scan BitBucket repo ...
# other repo ...


# Should perform some Machine Learning on Readme to get meta-data like themes, category ...


# Write the updated data
with open('data-tools-full.json', mode='w', encoding='utf-8') as f:
    json.dump(tools, f, indent=2)


def remove_useless_keys(tool):
    try:
        del tool['readme']
    except:
        pass
    return tool

tools = list(map(remove_useless_keys, tools))


# Write the updated data
with open('data-tools.json', mode='w', encoding='utf-8') as f:
    json.dump(tools, f, indent=2)
