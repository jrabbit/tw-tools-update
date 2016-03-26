# tw-tools-update
Use the GitHub-API to update the list of tools and extensions related to TaskWarrior. 
It will be displayed on the web site: http://taskwarrior.org/tools/

This is linked to the project of future Tool page: http://brunovernay.github.io/taskwarrior-site-test/

It is a work in progress. The idea is to use the GitHub-API to search project related to TaskWarrior and update the list of tools display on TaskWarrior site from this list.

- We still have to set the category manually
- It only covers GitHub projects currently
- We might apply a diff after the update, to keep manual changes
- We might apply a filter before, to exclude this very project for example :-)


Note:
- the text description is pure text, no HTML.
- There are duplicated names, we may have to use the author also?

The mapping:
- category: *manual*
- name name
- description description
- url homepage
- url_src html_url
- license ???
- language languages_url...
- author owner/login (+ collaborators, contributors, teams ...)
- theme *best guess from description*
