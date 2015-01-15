SHELL=/bin/sh

.SILENT:
.IGNORE:

.PHONY: test
test:
	py.test

.PHONY: clean
clean:
	rm -rf build/ htmlcov/
	find ./src/ -name "__pycache__" -exec rm -rf {} \;
	find ./src/ -name "*.pyc" -exec rm -rf {} \;

.PHONY: install-deps
install-deps:
	pip install --upgrade -e.[dev,test]

develop: install-deps
	python setup.py develop

.PHONY: lint
lint:
	pylint ./src/sambuca/

.PHONY: sdist
sdist:
	python setup.py sdist

.PHONY: bdist_wheel
bdist_wheel:
	python setup.py bdist_wheel

.PHONY: docs
docs:
	sphinx-build -b html docs build/docs
