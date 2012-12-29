DEVELOPMENT_ENV_DIRECTORY = .virtualenvs/development


help :
	@echo "usage: make <target> where target is one of:"
	@echo
	@echo "  env  Install local development environment"
	@echo

$(DEVELOPMENT_ENV_DIRECTORY)/bin/python :
	pip install \
		--environment=$(DEVELOPMENT_ENV_DIRECTORY) \
		--editable . \
		--requirement requirements.txt

env : $(DEVELOPMENT_ENV_DIRECTORY)/bin/python