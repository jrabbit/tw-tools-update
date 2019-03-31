from invoke import task


@task
def lint(c):
    c.run("flake8 --count")
