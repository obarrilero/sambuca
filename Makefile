SHELL=/bin/sh

.PHONY: clean
.IGNORE: clean
clean:
	rm -rf build/ htmlcov/
	find ./src/ -name "__pycache__" -exec rm -rf {} \;
	find ./src/ -name "*.pyc" -exec rm -rf {} \;
