import json
from datetime import date
from github import Github
from github.NamedUser import NamedUser
from github.Repository import Repository

from Tool import isObsolete

#
# http://pygithub.github.io/PyGithub/v1/index.html
# Maybe gh.load( file ) could allow to load an existing search into the Github object?

# Had to use a function just to get the right type. Otherwise, no auto-completion.
def getUserName(r: Repository) -> NamedUser:
    return r.owner

# Parse Github request to update the data
def updateTool(r: Repository, res):
    res['description'] = r.description
    res['descriptionText'] = r.description
    res['url'] = r.homepage or r.html_url   # Nice syntax!
    res['url_src'] = r.html_url
    res['author'] = [getUserName(r).name + ' (' + r.owner + ')']
    # we need other requests for the authors
    res['language'] = [r.language]
    res['last_update'] = r.updated_at.isoformat()
    res['verified'] = date.today().isoformat()
    res['obsolete'] = isObsolete(r.updated_at)


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
    newTool = {'name': r.name, 'category': "Unknown"}
    updateTool(r, newTool)
    tools.append(newTool)
    print(json.dumps(newTool, indent=2))
    pass




# Main program loop
# You really have to provide your token here, because 60 requests per hours won't cut it
#  Use https://github.com/settings/tokens
def scanGithubRepo(tools: list):
    i = 0
    gh = Github(login_or_token='ed372a1f41d3f1e7654dae3a21555e710c04455c', per_page=100)
    for r in gh.search_repositories("taskwarrior"):
        assert isinstance(r, Repository)
        i += 1
        print(i, "Name " + r.name)
        if not isToolUpdate(r, tools):
            addTools(r, tools)
            print("  Added")