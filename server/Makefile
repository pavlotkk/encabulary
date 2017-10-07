ENV = env
PYBIN = $(ENV)/scripts
PYTHON = $(PYBIN)/python
PIP = $(PYBIN)/pip
APPNAME = server
PYTEST = $(PYTHON) -m pytest
UNITTEST = $(PYTHON) -m unittest
PYFLAKE8 = $(PYTHON) -m flake8
TESTSDIR = $(APPNAME)/tests

environ: requirements.txt requirements-dev.txt
	virtualenv $(ENV)
	$(PIP) install -r requirements-dev.txt

.PHONY: help
help:
	@echo "make run     # run server"
	@echo "make initdb  # drop db, create all tables and init dicts with data"
	@echo "make tests   # run tests"
	@echo "make flake8  # run flake8"

.PHONY: run
run:
	$(PYTHON) runserver.py

.PHONY: initdb
initdb:
	$(PYTHON) initdb.py

.PHONY: pytests
pytests:
	$(PYTEST) --junitxml TEST-pytest.results.xml $(TESTSDIR)/unit_tests -v

.PHONY: unittests
unittests:
	$(PYTHON) -m xmlrunner discover -v -s $(TESTSDIR)/functional_tests

.PHONY: tests
tests:
	$(MAKE) pytests
	$(MAKE) unittests

.PHONY: flake8
flake8:
	$(PYFLAKE8) $(APPNAME)