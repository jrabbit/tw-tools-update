#
# List of tools urls to skip, as if they where not in GitHub or other repo.
#


def skip_these_tools(url):
    if url == "https://github.com/BrunoVernay/tw-tools-update":
        return True
    return False
