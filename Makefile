serve:
	python manage.py runserver 0.0.0.0:8000

start:
	brew services start postgresql

stop:
	brew services stop postgresql

build:
	python manage.py test --settings seven23.settings_tests
	python manage.py migrate
	python manage.py collectstatic --no-input
	python manage.py loaddata seven23/models/currency/fixtures/initial_data.json

test:
	python manage.py test --settings seven23.settings_tests

docs:
	sphinx-autobuild docs/ docs/_build/html

clean:
	find . -name '*.pyc' -delete
	find . -name '*~' -delete

docker-build:
	docker build --pull -t seven23_server .

docker-run:
	docker-compose -f docker-compose.yml up -d

docker-shell:
	docker exec -ti seven23_server_app_1 /bin/sh

docker-stop:
	docker-compose stop

.PHONY: start stop shell test docs clean build serve
