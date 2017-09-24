all:
	python manage.py runserver 0.0.0.0:8000

start:
	brew services start postgresql

stop:
	brew services stop postgresql

test:
	python manage.py test

docs:
	sphinx-autobuild docs/ docs/_build/html

clean:
	find . -name '*.pyc' -delete
	find . -name '*~' -delete
