# tw-tools-update

## Description

Use the GitHub-API to update the list of tools and extensions related to TaskWarrior. 
It will be displayed on the web site: http://taskwarrior.org/tools/

This is linked to the project of future Tool page: http://brunovernay.github.io/taskwarrior-site-test/

The idea is to use the GitHub-API to search project related to TaskWarrior and update the list of tools displayed on TaskWarrior site from this list.

The project started in Java, but I created a Python branch, as it is more idiomatic to the TaskWarrior community.

I use https://github.com/PyGithub/PyGithub , there are [many Python projects addressing GitHub](https://developer.github.com/libraries/#python), even a book [Mining the Social Web](https://www.safaribooksonline.com/library/view/mining-the-social/9781449368180/) .

## Status

- It works
- We still have to set the category manually
- There is no API yet to get the license (GitHub is working on it)
- You have to enter your GitHub token given the number of required requests. (https://github.com/settings/tokens)
- It only covers GitHub projects currently (BitBucket maybe one day ...)
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


## Automatic classification

I get all the "Readme" in order to perform some Machine Learning. The first idea would be to classify by category. The Python library seems to be SciKit. There is a more active [NLTK](http://www.nltk.org/) library, but since I only need simple text feature extraction and no complex Natural Language processing, I will stick to SciKit. 
Some ref:
 - http://scikit-learn.org/stable/modules/feature_extraction.html
 - http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
 - http://scikit-learn.org/stable/auto_examples/model_selection/grid_search_text_feature_extraction.html
 - 
 
