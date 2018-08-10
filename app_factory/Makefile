#!/usr/bin/make -f
########################################
# Includes make commands to setup and  #
# clean environment for app factory.   #
########################################
REQUIREMENTS_FILE=requirements.txt
ENV_PATH=~/.virtualenvs/app_factory
ENV=$(ENV_PATH)/bin/activate

help:
	@echo "setup - Setup, activate virtualenv and install requirements"
	@echo "clean - De-activate and deletes virtualenv"

setup:
	virtualenv -p python3.6 $(ENV_PATH); \
	source $(ENV); \
	pip install -r requirements.txt; \

clean:
	sudo deactivate; \
	rm -rf $(ENV_PATH)
	find . -name "*.pyc" -exec rm -f {} \;
