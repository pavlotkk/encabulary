ENV = env

PYBIN_WINDOWS = $(ENV)/Scripts
PYBIN_LINUX = $(ENV)/bin
PYBIN = $(PYBIN_LINUX)

DEFAULT_PYTHON = python
PYTHON = $(PYBIN)/python

PIP = $(PYBIN)/pip
APPNAME = server
PYTEST = $(PYTHON) -m pytest
UNITTEST = $(PYTHON) -m unittest
PYFLAKE8 = $(PYTHON) -m flake8
TESTSDIR = $(APPNAME)/tests
FRONTEND = $(APPNAME)/frontend

DOCKER = docker
DOCKER_CONTAINER_NAME = encabulary

.PHONY: help
help:
	@echo "make install             # install project"
	@echo "make run                 # run server"
	@echo "make initdb              # drop db, create all tables and init dicts with data"
	@echo "make tests               # run tests"
	@echo "make flake8              # run flake8"
	@echo "make docker              # rebuild docker"
	@echo "make docker-build        # build docker container"
	@echo "make docker-stop         # stop docker container"
	@echo "make docker-remove       # remove docker container"
	@echo "make docker-remove-all   # remove all docker container"
	@echo "=========================#"
	@echo "make frontend-install    # install node modules"
	@echo "make frontend-dev        # run webpack dev server"
	@echo "make frontend-build      # build frontend"

.PHONY: install
install: requirements.txt requirements-dev.txt
	$(DEFAULT_PYTHON) -m virtualenv $(ENV)
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
	$(PYTEST) --junitxml tests_xml/TEST-pytest.results.xml $(TESTSDIR)/unit_tests -v

.PHONY: unittests
unittests:
	$(PYTHON) rununittests.py

.PHONY: tests
tests:
	$(MAKE) pytests
	$(MAKE) unittests

.PHONY: flake8
flake8:
	$(PYFLAKE8) $(APPNAME)

.PHONY: docker
docker:
	$(MAKE) docker-stop && $(MAKE) docker-build || $(MAKE) docker-build
	$(MAKE) docker-start || $(MAKE) docker-run

.PHONY: docker-stop
docker-stop:
	$(DOCKER) stop $(DOCKER_CONTAINER_NAME)

.PHONY: docker-remove
docker-remove:
	$(MAKE) docker-stop
	$(DOCKER) rm $(DOCKER_CONTAINER_NAME)
	$(DOCKER) rmi $(DOCKER_CONTAINER_NAME)

.PHONY: docker-remove-all
docker-remove-all:
	$(DOCKER) stop $$($(DOCKER) ps -a -q)
	$(DOCKER) rm $$($(DOCKER) ps -a -q)
	$(DOCKER) rmi $$($(DOCKER) images -a -q)

.PHONY: docker-build
docker-build:
	$(DOCKER) build -t $(DOCKER_CONTAINER_NAME) .

.PHONY: docker-run
docker-run:
	$(DOCKER) run --restart=always -p 80:80 -d --name $(DOCKER_CONTAINER_NAME) --net="host" -t $(DOCKER_CONTAINER_NAME)

.PHONY: docker-start
docker-start:
	$(DOCKER) start $(DOCKER_CONTAINER_NAME)

.PHONY: docker-attach
docker-attach:
	$(DOCKER) exec -it $(DOCKER_CONTAINER_NAME) bash

.PHONY: frontend-install
frontend-install:
	$(MAKE) -C $(FRONTEND) install

.PHONY: frontend-dev
frontend-dev:
	$(MAKE) -C $(FRONTEND) dev

.PHONY: frontend-build
frontend-build:
	$(MAKE) -C $(FRONTEND) build