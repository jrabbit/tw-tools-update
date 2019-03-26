import json
import logging

import toml

from RepoGithub import scan_github_repo

logger = logging.getLogger(__name__)

# Load previous data
with open('data-tools-old.json') as f:
    tools = json.load(f)


config = toml.load("config.toml")

gh_token = config["github"]["token"]

scan_github_repo(tools, gh_token)
# Should scan BitBucket repo ...
# other repo ...


# Should perform some Machine Learning on Readme to get meta-data like themes, category ...


# Write the updated data
with open('data-tools-full.json', mode='w', encoding='utf-8') as f:
    json.dump(tools, f, indent=2)


def remove_useless_keys(tool):
    try:
        del tool['readme']
    except Exception as e:
        logger.exception(e)
    return tool

tools = list(map(remove_useless_keys, tools))


# Write the updated data
with open('data-tools.json', mode='w', encoding='utf-8') as f:
    json.dump(tools, f, indent=2)
