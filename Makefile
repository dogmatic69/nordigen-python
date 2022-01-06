.PHONY: build
build: venv
	python setup.py sdist

.PHONY: isort
isort:
	isort ./nordigen ./tests ./examples --check-only

.PHONY: black
black:
	black --check ./nordigen ./tests ./examples

.PHONY: flake8
flake8:
	flake8 ./nordigen ./tests ./examples

.PHONY: test
test:
	pytest --ignore=examples/

.PHONY: ci
ci: venv isort black flake8 test

.PHONY: ci-fix
ci-fix: venv
	isort ./nordigen ./tests ./examples
	black ./nordigen ./tests ./examples

.PHONY: dev
dev:
	$(MAKE) ci-fix
	$(MAKE) ci

.PHONY: install-pip
install-pip: venv
	python -m pip install --upgrade pip

.PHONY: install-dev
install-dev: install-pip
	pip install -e ".[dev]"

.PHONY: install-deploy
install-deploy: install-pip
	pip install -e ".[deploy]"

.PHONY: deploy
deploy: build
	twine upload --verbose dist/*

.PHONY: venv
venv:
	$(shell [ ! -d .python ] && python -m venv .python)
	. .python/bin/activate