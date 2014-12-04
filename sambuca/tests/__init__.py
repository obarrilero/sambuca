# pytest does not recommend putting __init__.py into the tests directory for
# inlined tests, however not having it present makes the coverage report fail
# when the tests are run via tox :(
