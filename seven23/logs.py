from . import settings

def print_settings_report():
    print('################################')
    print('#####    Seven23_server     ####')
    print('################################')

    if settings.DEBUG:
        print('✅ 🔎 🐛 Debug is enabled')

    print(f'Version: {settings.VERSION[0]}.{settings.VERSION[1]}.{settings.VERSION[2]}')

    if 'SECRET_KEY' in settings.errors:
        print('⚠️ Secret key generated. Please set the environment variable SECRET_KEY to avoid this message.')

    if 'ALLOW_ACCOUNT_CREATION' in settings.errors:
        print('❌ 🙅‍♂️ Registration is disabled')
    else:
        print('✅ 🙋‍♂️ Registration is enabled')

    if 'EMAIL_BACKEND' in settings.errors:
        print('❌ ✉️  Emails are displayed in console')