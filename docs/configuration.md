# Configuration

The configuration is done through environment variables within the `seven23/settings.py` file. This allows to have a single source of truth for the configuration, and to easily change it depending on the environment.

Variables can be define in a `.env` file.

## Secret Key

Used to define the secret key used to sign the session cookie.

```shell
SECRET_KEY=<cat walk>
```

## Database url

Used to define access to the database.

```shell
DATABASE_URL=postgresql://username:password@url:port/db
```

## Debug mode

Toggle debug mode.

```shell
DEBUG=1
```

## Allow account creation

Disable the creation of new user throught the application.

```shell
ALLOW_ACCOUNT_CREATION=0
```