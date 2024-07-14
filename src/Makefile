.PHONY: essential-folders init start migrate

essential-folders:
	@if [ ! -d ".csepf" ]; then mkdir .csepf; fi
	@if [ ! -d ".csepf/creds" ]; then mkdir .csepf/creds; fi


init: essential-folders
	pip install -r requirements.txt


start: essential-folders
	@echo "Initializing server now ..."
	python manage.py runserver

migrate:
	@echo "Running migrations ..."
	python manage.py makemigrations
	python manage.py migrate
