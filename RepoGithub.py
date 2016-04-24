import json
from datetime import date
from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile
import re

import Tool
from Tool import isObsolete, bestEffortTheme


#
# http://pygithub.github.io/PyGithub/v1/index.html
# Maybe gh.load( file ) could allow to load an existing search into the Github object?

# Looks like GitHub provides License information: https://developer.github.com/v3/licenses/#get-a-repositorys-license
# But the Python library is not able to get it. Wait and see ...


# Parse Github request to update the data
def updateTool(r: Repository, res):
    res['description'] = r.description
    res['descriptionText'] = r.description
    res['url'] = r.homepage or r.html_url   # Nice syntax!
    res['url_src'] = r.html_url
    res['author'] = []
    for contributor in r.get_contributors():
        if contributor.name:
            res['author'].append(contributor.name + ' (' + contributor.login + ')')
        else:
            res['author'].append(contributor.login)
    # Get the readme for future use ...
    rx = re.compile('\W+')
    try:
        res['readme'] = rx.sub(' ',  r.get_readme().decoded_content.decode('utf-8')).strip()
    except:
        print('Could not get Readme.')
    res['language'] = [r.language] if r.language is not None else []
    # LastUpdate would be an update on GitHub repo
    res['last_update'] = r.updated_at.date().isoformat()
    res['verified'] = date.today().isoformat()
    res['obsolete'] = isObsolete(r.updated_at)
    bestEffortTheme(res)


def isToolUpdate(r: Repository, tools: list) -> bool:
    # Is current result already in the tools?
    potential_matches = 0
    good_matches = 0
    matches = filter(lambda x: r.name == x['name'], tools)
    for res in matches:
        print(res)
        potential_matches += 1
        if res['url_src'] or res['url'] == r.html_url:
            good_matches += 1
            if good_matches > 1:
                print("Error: at least 2 projects have the same name and URL in previous data: "+ r.name +" !")
            updateTool(r, res)
            print('  Updated')
    if good_matches == 0:
        if potential_matches > 0:
            print("(Warning: Please check duplicates !  May be on GitHub, but the source URL does not link to GitHub.) ")
        return False
    else:
        if potential_matches > 1:
            print("Warning: Please check possible duplicates in previous data !")
        return True


def addTools(r: Repository, tools):
    newTool = Tool.newTool(r.name)
    updateTool(r, newTool)
    tools.append(newTool)
    print(json.dumps(newTool, indent=2))
    pass




# Main program loop
def scanGithubRepo(tools: list, github_token: str):
    i = 0
    gh = Github(login_or_token=github_token, per_page=100)
    for r in gh.search_repositories("taskwarrior"):
        assert isinstance(r, Repository)
        i += 1
        print(i, "Name " + r.name)
        if not isToolUpdate(r, tools):
            addTools(r, tools)
            print("  Added")