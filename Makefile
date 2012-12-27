help :
	@echo "usage: make <target> where target is one of:"
	@echo
	@echo "  env  Install local development environment"
	@echo

.virtualenvs/development/bin/python :
	pip install \
		--environment=.virtualenvs/development \
		--editable . \
		--requirement requirements.txt

env : .virtualenvs/development/bin/python
