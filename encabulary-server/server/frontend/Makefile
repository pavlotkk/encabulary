NPM = npm


environ: package.json
	$(MAKE) build

.PHONY: help
help:
	@echo "make install     # install npm dependencies"
	@echo "make dev         # run webpack dev server"
	@echo "make build       # build"

.PHONY: install
install: package.json
	$(NPM) install

.PHONY: dev
dev: package.json
	$(NPM) run dev

.PHONY: build
build: package.json
	$(NPM) run build