# Deployment

Self-hosted instance are a big part of this project, and we want to make it as easy as possible to deploy your own instance.

To so do, we recommand using docker-compose, but you can also use the provided Dockerfile to build your own image.

(docker_deployment)=

## Using Docker

A docker image is available within hub.docker.com on the [sebastienbarbier/seven23](https://hub.docker.com/r/sebastienbarbier/seven23) repository.

Pull the image using
```shell
docker run -p 8000:8000 -ti sebastienbarbier/seven23
```

It will use by default a locally stored sqlite instance. and exposing directly to port 8000. To customize those settings, it is recommand to use a docker-compose.yml file and override env vars as describe in the following configurations section.

## Command tools

If for any reason you do not want to use our docker instance, code can run directly on any servuer and initialised using command tools direclty. A one command build is available as a Makefile.

```shell
make build
```

This is a set of instruction which can be runned manually:

```shell
python manage.py test --settings seven23.settings_tests
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py loaddata seven23/models/currency/fixtures/initial_data.json
```

## Configuration

Deployed instance will access environment variables to configure itself. Should be done before any deployment.

```shell
DATABASE_URL            = postgresql://username:password@url:port/db
SECRET_KEY              = YOUR_SECRET_KEY
ALLOW_ACCOUNT_CREATION  = false
AWS_ACCESS_KEY_ID       = YOUR_AWS_ACCESS_KEY_ID
AWS_S3_CUSTOM_DOMAIN    = YOUR_AWS_S3_CUSTOM_DOMAIN
AWS_SECRET_ACCESS_KEY   = YOUR_AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = YOUR_AWS_STORAGE_BUCKET_NAME
CONTACT_EMAIL           = admin@seven23.io
EMAIL_HOST              = YOUR_EMAIL_HOST
EMAIL_HOST_USER         = YOUR_EMAIL_USER
EMAIL_HOST_PASSWORD     = YOUR_EMAIL_PASSWORD
MAIL_USE_TLS            = false
EMAIL_PORT              = 25
DEBUG                   = false
```