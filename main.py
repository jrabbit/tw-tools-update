import json
import argparse
import logging
from typing import Dict, Any
import toml

from repo_github import scan_github_repo

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()
parser.add_argument("--debug-all", action="store_true", help="log all possible messages")
parser.add_argument("--debug-some", action="store_true")
parser.add_argument("--small-run", action="store_true")
args = parser.parse_args()

if args.debug_all:
    logging.basicConfig(level="DEBUG")

logging.basicConfig(level=logging.INFO)
# Load previous data
with open("data-tools-old.json") as f:
    tools = json.load(f)


config = toml.load("config.toml")

gh_token = config["github"]["token"]

revised_tools = scan_github_repo(tools, gh_token, args.small_run)
# Should scan BitBucket repo ...
# other repo ...


# Should perform some Machine Learning on Readme to get meta-data like themes, category ...


# Write the updated data
with open("data-tools-full.json", mode="w", encoding="utf-8") as f:
    json.dump(revised_tools, f, indent=2)


def remove_useless_keys(tool: Dict[str, Any]) -> Dict[str, Any]:
    try:
        del tool["readme"]
    except (KeyError, TypeError):
        # supress
        pass
    except Exception as e:
        logger.exception(e)
    return tool


slim_tools = list(map(remove_useless_keys, revised_tools))


# Write the updated data
with open("data-tools.json", mode="w", encoding="utf-8") as f:
    json.dump(slim_tools, f, indent=2)
logger.info("wrote data-tools.json successfully")
