ENV = env
PYBIN = $(ENV)/scripts
PYTHON = $(PYBIN)/python
PIP = $(PYBIN)/pip
APPNAME = server
PYTEST = $(PYTHON) -m pytest
UNITTEST = $(PYTHON) -m unittest
PYFLAKE8 = $(PYTHON) -m flake8
TESTSDIR = $(APPNAME)/tests
FRONTEND = $(APPNAME)/frontend

.PHONY: help
help:
	@echo "make install             # install project"
	@echo "make run                 # run server"
	@echo "make initdb              # drop db, create all tables and init dicts with data"
	@echo "make tests               # run tests"
	@echo "make flake8              # run flake8"
	@echo "=========================#"
	@echo "make frontend-install    # install node modules"
	@echo "make frontend-dev        # run webpack dev server"
	@echo "make frontend-build      # build frontend"

.PHONY: install
install: requirements.txt requirements-dev.txt
	virtualenv $(ENV)
	$(PIP) install -r requirements-dev.txt
	$(MAKE) frontend-install
	$(MAKE) frontend-build

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

.PHONY: frontend-install
frontend-install:
	$(MAKE) -C $(FRONTEND) install

.PHONY: frontend-dev
frontend-dev:
	$(MAKE) -C $(FRONTEND) dev

.PHONY: frontend-build
frontend-build:
	$(MAKE) -C $(FRONTEND) build