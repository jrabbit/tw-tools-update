from datetime import date
import logging
import re
from typing import List, Dict, Any

from github import Github
from github.Repository import Repository

import tool
from skip_these_tools import skip_these_tool
from tool import is_obsolete, best_effort_theme

logger = logging.getLogger(__name__)

# Looks like GitHub provides License information: https://developer.github.com/v3/licenses/#get-a-repositorys-license
# But the Python library is not able to get it. Wait and see ...


def update_tool(new_tool: Repository, old_tool: Dict[str, Any]) -> None:
    """
    Parse Github request to update the data
    :param new_tool: from the GitHub repository
    :param old_tool:
    """
    old_tool["description"] = new_tool.description
    old_tool["descriptionText"] = new_tool.description
    old_tool["url"] = new_tool.homepage or new_tool.html_url  # Nice syntax!
    old_tool["url_src"] = new_tool.html_url
    old_tool["author"] = []
    for contributor in new_tool.get_contributors():
        if contributor.name:
            old_tool["author"].append(contributor.name + " (" + contributor.login + ")")
        else:
            old_tool["author"].append(contributor.login)
    # Get the readme for future use ...
    rx = re.compile(r"\W+")
    try:
        old_tool["readme"] = rx.sub(
            " ", new_tool.get_readme().decoded_content.decode("utf-8")
        ).strip()
    except:
        logger.debug("Could not get Readme.")
    old_tool["language"] = [new_tool.language] if new_tool.language is not None else []
    old_tool["stars"] = new_tool.stargazers_count
    # LastUpdate would be an update on GitHub repo
    old_tool["last_update"] = new_tool.updated_at.date().isoformat()
    old_tool["verified"] = date.today().isoformat()
    old_tool["obsolete"] = is_obsolete(new_tool.updated_at)
    best_effort_theme(old_tool)


def is_tool_update(new_tool: Repository, old_tools: List[Dict[str, Any]]) -> bool:
    """
    Is current result already in the tools?
    :param new_tool: tool from the repository
    :param old_tools: old tool list
    :return:
    :rtype: bool
    """
    potential_matches = 0
    good_matches = 0
    existing_matches = filter(lambda x: new_tool.name == x["name"], old_tools)
    for existing_tool in existing_matches:
        logger.debug(existing_tool)
        potential_matches += 1
        if (existing_tool["url_src"] == new_tool.html_url) or (
            existing_tool["url"] == new_tool.html_url
        ):
            good_matches += 1
            if good_matches > 1:
                logger.warning(
                    "Error: at least 2 projects have the same name and URL in previous data: "
                    + new_tool.name
                    + " !"
                )
            update_tool(new_tool, existing_tool)
            logger.debug("  Updated")
    if good_matches == 0:
        if potential_matches > 0:
            logger.warning(
                "(Warning: Please check duplicates !  May be on GitHub, but the source URL does not link to GitHub.) "
            )
        return False
    else:
        if potential_matches > 1:
            logger.warning(
                "Warning: Please check possible duplicates in previous data !"
            )
        return True


def scan_github_repo(tools: List[Dict[str, Any]], github_token: str, small_run: bool) -> List[Dict[str, Any]]:
    """
    Main program loop
    :param tools: old tool list
    :param github_token: See GitHub doc.
    """
    gh = Github(login_or_token=github_token, per_page=100)
    revised_tools = list()
    r: Repository #declare type 
    for i, r in enumerate(gh.search_repositories("taskwarrior"), 1):
        if i > 5 and small_run:
            break
        # assert isinstance(r, Repository)
        logger.info("#%d, Name: %s %s", i, r.name, r.html_url)
        if not skip_these_tool(r.html_url) and not is_tool_update(r, tools):
            t = tool.new_tool(r.name)
            update_tool(r, t)
            revised_tools.append(t)
            logger.debug("new tool %r", t)
            logger.info("%s  Added", r.name)

        # this isn't a free lookup or cached.
        # elif is_tool_update(r, tools):
        # todo: handle this case
        # pass
    return revised_tools
