clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +


clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

publish:
	@rm -rf dist
	@rm -rf osm_road_length.egg-info
	@python setup.py sdist
	@twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	ls -l dist

release: dist ## package and upload a release
	twine upload dist/*

start-env:
	python3 -m venv .env
	. .env/bin/activate; pip install -r requirements_dev.txt; \
		python -m ipykernel install --user --name=osm-road-length