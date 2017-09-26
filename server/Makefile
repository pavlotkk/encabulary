PYTHON = python
APPNAME = server
PYTEST = $(PYTHON) -m pytest
UNITTEST = $(PYTHON) -m unittest
PYFLAKE8 = $(PYTHON) -m flake8
TESTSDIR = $(APPNAME)/tests

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

.PHONY: tests
tests:
	$(PYTEST) $(TESTSDIR)/unit_tests -v
	$(UNITTEST) discover -v -s $(TESTSDIR)/functional_tests

.PHONY: flake8
flake8:
	$(PYFLAKE8) $(APPNAME)