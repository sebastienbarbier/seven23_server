serve:
	python manage.py runserver 0.0.0.0:8000

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
	docker build --pull -t seven23 .

docker-run:
	docker run -p 8000:8000 --name seven23 -ti seven23

docker-shell:
	docker exec -ti seven23 /bin/sh

docker-stop:
	docker stop seven23

.PHONY: start stop shell test docs clean build serve docker-build docker-run docker-shell docker-stop