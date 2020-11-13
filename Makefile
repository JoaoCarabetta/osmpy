REPO=$(shell basename $(CURDIR))

create-env:
	python3 -m venv .$(REPO);
	source .$(REPO)/bin/activate; \
			pip3 install --upgrade -r requirements_dev.txt; \
			python -m ipykernel install --user --name=$(REPO);