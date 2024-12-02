import os
import nox

os.environ.update({"PDM_IGNORE_SAVED_PYTHON": "1"})

@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"])
def tests(session):
    session.install("pytest")
    session.run_always('pdm', 'install', external=True)
    session.run('pytest')