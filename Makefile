PIP ?= pip

DEVELOPMENT_ENV_DIRECTORY = $(shell pwd)/.virtualenvs/development


help :
	@echo "usage: make <target> where target is one of:"
	@echo
	@echo "  clean     Delete auto-generated files (.pyc, sdists, etc)"
	@echo "  env       Install local development environment"
	@echo "  lint      Run PEP8 linter on application code"
	@echo "  pristine  Delete local development environment"
	@echo "  test      Run tests if linter finds no style errors"
	@echo

$(DEVELOPMENT_ENV_DIRECTORY)/bin/python :
	$(PIP) install \
		--environment=$(DEVELOPMENT_ENV_DIRECTORY) \
		--editable=. \
		--requirement=requirements.txt

$(DEVELOPMENT_ENV_DIRECTORY)/takestock.db : \
		$(DEVELOPMENT_ENV_DIRECTORY)/bin/python
	bin/manage syncdb --noinput

bin/fab : $(DEVELOPMENT_ENV_DIRECTORY)/bin/python
	ln -s $(DEVELOPMENT_ENV_DIRECTORY)/bin/fab bin/fab

clean :
	git clean -fx

env : \
		$(DEVELOPMENT_ENV_DIRECTORY)/bin/python \
		$(DEVELOPMENT_ENV_DIRECTORY)/takestock.db \
		bin/fab

lint : env
	$(DEVELOPMENT_ENV_DIRECTORY)/bin/pep8 src
	@echo "SUCCESS! Linter reports no issues."

pristine : clean
	git clean -dfx

test : env lint
	bin/manage test
