from datetime import date, timedelta
from github import Github
from github.Repository import Repository
import json


# Load previous data
tools = json.loads(open('data-tools-old.json').read(), encoding='utf-8')
# print(tools)
# print(tools[1]['name'])

# Parse Github request to update the data
gh = Github(per_page=100)


def updateTool(r, res):
    res['description'] = r.description
    res['descriptionText'] = r.description
    res['url'] = r.homepage or r.html_url   # Nice syntax!
    res['url_src'] = r.html_url
    # we need other requests for the authors
    res['language'] = [r.language]
    res['last_update'] = r.updated_at[:-10]
    res['verified'] = date.today().isoformat()
    res['obsolete'] = timedelta(years=3) < date(r.updated_at) - date.today()


def parseBatchOfGithubResults(r, tools):
    # Is current result already in the tools?
    print('Parsing ' + r.name)
    matchesNumb = 0
    matches = filter(lambda x: r.name == x['name'], tools)
    for res in matches:
        print(res)
        print("Warning: Please check possible duplicates in previous data !")
        if res['url_src'] == r.html_url:
            matchesNumb += 1
            if matchesNumb > 1:
                print("Error: at least 2 projects have the same name and URL in previous data: "+ r.name +" !")
            updateTool(r, res)
    if matchesNumb == 0:
        print("(Warning: Please check duplicates !  May be on GitHub, but the source URL does not link to GitHub.) ")
        return False
    else:
        return True

i = 0
for r in gh.search_repositories("taskwarrior"):
    assert isinstance(r, Repository)
    i += 1
    print(i, "Name " + r.name)
    parseBatchOfGithubResults(r, tools)

# Write the updated data
with open('data-tools.json', mode='w', encoding='utf-8') as f:
    json.dump(tools, f, indent=2)


# http://pygithub.github.io/PyGithub/v1/index.html
# Maybe gh.load( file ) could allow to load an existing search into the Github object?
