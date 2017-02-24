all:
	python manage.py runserver 0.0.0.0:8000

start:
	launchctl load /usr/local/opt/postgresql/homebrew.mxcl.postgresql.plist

stop:
	launchctl unload /usr/local/opt/postgresql/homebrew.mxcl.postgresql.plist

test:
	python manage.py test

docs:
	sphinx-autobuild docs/ docs/_build/html

clean:
	find . -name '*.pyc' -delete
	find . -name '*~' -delete
