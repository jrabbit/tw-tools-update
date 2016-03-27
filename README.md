# tw-tools-update
Use the GitHub-API to update the list of tools and extensions related to TaskWarrior. 
It will be displayed on the web site: http://taskwarrior.org/tools/

This is linked to the project of future Tool page: http://brunovernay.github.io/taskwarrior-site-test/

It is a work in progress. The idea is to use the GitHub-API to search project related to TaskWarrior and update the list of tools display on TaskWarrior site from this list.

Project currently in Java, but I may create a Python branch, as it is more idiomatic to this community.
(https://github.com/sigmavirus24/github3.py might be a good start, there are [many Python projects addressing GitHub](https://developer.github.com/libraries/#python) )

- We still have to set the category manually
- It only covers GitHub projects currently
- We might apply a diff after the update, to keep manual changes
- We might apply a filter before, to exclude this very project for example :-)


Note:
- the text description is pure text, no HTML.
- There are duplicated names, I use the url_src as a unique identifier. But some project changed URL, for example xtw changed its login name, so the url is different. I output a warning and create a duplicate

The mapping:
- category: *manual*
- name name
- description description
- url homepage
- url_src html_url
- license ???
- language language (will get only the primary language, have to request languages_url to know more)
- author owner/login (+ collaborators, contributors, teams ...) We have to make multiple request to get the real name instead of the Login.
- theme *best guess from description*
- verified *today*
- last_update updated_at (pushed_at would be more conservative, but would miss commits in non-master branches)
