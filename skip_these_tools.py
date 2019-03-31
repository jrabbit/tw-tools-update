#
# List of tools urls to skip, as if they where not in GitHub or other repo.
#

exclude_url_list = [
    "https://github.com/BrunoVernay/tw-tools-update",
    "https://github.com/BrunoVernay/taskwarrior-site-test",
    "https://github.com/BrunoVernay/tw-html-parse",
    "https://github.com/pld-linux/bugwarrior",
]


def skip_these_tool(url: str) -> bool:
    """
    Some projects that are not relevant to the tool list
    :param url: would be html_url for GitHub, to uniquely distinguish projects
    :return: boolean True if this tool should be ignored
    """
    if any(url == s for s in exclude_url_list):
        return True
    return False
