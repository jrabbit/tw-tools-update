from invoke import task


@task
def lint(c, mypy=False):
    c.run("flake8 --count", warn=True)
    if mypy:
        c.run("mypy --strict .", warn=True)
