
PIP=pip
PIPENV=pipenv
PYTHON=python
PACKAGE=aamras

init: pipenv
	$(PIPENV) install

init-test: pipenv
	$(PIPENV) install --dev

pipenv:
ifeq (, $(shell PATH=$(PATH) which $(PIPENV) 2> /dev/null))
	@echo "$(PIPENV) not installed; installing"

	$(PYTHON) -m $(PIP) install --upgrade $(PIP)
	$(PIP) install pipenv
endif

run: pipenv
	$(PIPENV) run $(PYTHON) -m $(PACKAGE)

clean:
	find . -iname '*.pyc' -delete
	find . -iname '__pycache__' -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache

typecheck: pipenv
	$(PIPENV) run mypy --package $(PACKAGE)

lint: pipenv
	$(PIPENV) run flake8 . --select E9,F63,F7,F82
	$(PIPENV) run flake8 . --exit-zero

unittest: pipenv
	$(PIPENV) run pytest --cov $(PACKAGE)

test: pipenv typecheck lint unittest
