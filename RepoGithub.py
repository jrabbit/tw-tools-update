import json
from datetime import date
import logging
import re

from github import Github
from github.Repository import Repository

import Tool
from SkipTheseTools import skip_these_tool
from Tool import is_obsolete, best_effort_theme


logger = logging.getLogger(__name__)

#
# http://pygithub.github.io/PyGithub/v1/index.html
# Maybe gh.load( file ) could allow to load an existing search into the Github object?

# Looks like GitHub provides License information: https://developer.github.com/v3/licenses/#get-a-repositorys-license
# But the Python library is not able to get it. Wait and see ...


def update_tool(new_tool, old_tool):
    """
    Parse Github request to update the data
    :param new_tool: from the GitHub repository
    :param old_tool:
    """
    old_tool['description'] = new_tool.description
    old_tool['descriptionText'] = new_tool.description
    old_tool['url'] = new_tool.homepage or new_tool.html_url   # Nice syntax!
    old_tool['url_src'] = new_tool.html_url
    old_tool['author'] = []
    for contributor in new_tool.get_contributors():
        if contributor.name:
            old_tool['author'].append(contributor.name + ' (' + contributor.login + ')')
        else:
            old_tool['author'].append(contributor.login)
    # Get the readme for future use ...
    rx = re.compile('\W+')
    try:
        old_tool['readme'] = rx.sub(' ', new_tool.get_readme().decoded_content.decode('utf-8')).strip()
    except:
        print('Could not get Readme.')
    old_tool['language'] = [new_tool.language] if new_tool.language is not None else []
    # Get a list of people who have bookmarked the repo.
    # Since you'll get a lazy iterator back, you have to traverse
    # it if you want to get the total number of stargazers.
    stargazers = [s for s in new_tool.get_stargazers()]
    old_tool['stars'] = len(stargazers)
    # LastUpdate would be an update on GitHub repo
    old_tool['last_update'] = new_tool.updated_at.date().isoformat()
    old_tool['verified'] = date.today().isoformat()
    old_tool['obsolete'] = is_obsolete(new_tool.updated_at)
    best_effort_theme(old_tool)


def is_tool_update(new_tool, old_tools):
    """
    Is current result already in the tools?
    :param new_tool: tool from the repository
    :param old_tools: old tool list
    :return:
    :rtype: bool
    """
    potential_matches = 0
    good_matches = 0
    existing_matches = filter(lambda x: new_tool.name == x['name'], old_tools)
    for existing_tool in existing_matches:
        print(existing_tool)
        potential_matches += 1
        if (existing_tool['url_src'] == new_tool.html_url) or (existing_tool['url'] == new_tool.html_url):
            good_matches += 1
            if good_matches > 1:
                print("Error: at least 2 projects have the same name and URL in previous data: " + new_tool.name + " !")
            update_tool(new_tool, existing_tool)
            print('  Updated')
    if good_matches == 0:
        if potential_matches > 0:
            print("(Warning: Please check duplicates !  May be on GitHub, but the source URL does not link to GitHub.) ")
        return False
    else:
        if potential_matches > 1:
            print("Warning: Please check possible duplicates in previous data !")
        return True


def add_tool(new_tool, old_tools):
    """

    :param new_tool: tool from the repository
    :param old_tools: old tool list
    """
    t = Tool.new_tool(new_tool.name)
    update_tool(new_tool, t)
    old_tools.append(t)
    print(json.dumps(t, indent=2))


def scan_github_repo(tools, github_token):
    """
    Main program loop
    :param tools: old tool list
    :param github_token: See GitHub doc.
    """
    i = 0
    gh = Github(login_or_token=github_token, per_page=100)
    for r in gh.search_repositories("taskwarrior"):
        assert isinstance(r, Repository)
        i += 1
        print(i, "Name " + r.name + " " + r.html_url)
        if not skip_these_tool(r.html_url) and not is_tool_update(r, tools):
            add_tool(r, tools)
            print("  Added")