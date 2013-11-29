"""
Django settings for bulkymonkey project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""


from configurations import Configuration, values


class Common(Configuration):
    DEBUG = True

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'b0%6y28ci*948t=bwz5)rxx1p6duc0_k8+rv!%e5m!_49uzt4w'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    TEMPLATE_DEBUG = True

    ALLOWED_HOSTS = []

    # Application definition
    BASE_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )

    # Third party apps
    THIRD_PARTY_APPS = (
        'django_extensions',
        'djrill',
        'floppyforms',
        'crispy_forms',
        'south',
        'djcelery',
    )

    # Local apps
    LOCAL_APPS = (
        'emailer',
    )

    INSTALLED_APPS = BASE_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'bulkymonkey.urls'

    WSGI_APPLICATION = 'bulkymonkey.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases
    # http://django-configurations.readthedocs.org/en/latest/values/#configurations.values.DatabaseURLValue
    DATABASES = values.DatabaseURLValue(environ=True, environ_name='DJANGO_DATABASE_URL')

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/

    LANGUAGE_CODE = 'es-es'

    TIME_ZONE = 'Europe/Madrid'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale'),
    )

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = '/static/'

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

    # Djrill configuration
    # MANDRILL_API_KEY = values.Value('', environ=True)
    # EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

    # Local SMTP configuration
    EMAIL_BACKEND = "emailer.backends.BulkyMonkeyEmailBackend"
    EMAIL_HOST = values.Value('', environ=True)
    EMAIL_HOST_USER = values.Value('', environ=True)
    EMAIL_HOST_PASSWORD = values.Value('', environ=True)

    INTERNAL_IPS = ('127.0.0.1',)

    CRISPY_TEMPLATE_PACK = 'bootstrap3'

    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
        "django.contrib.messages.context_processors.messages",
        "emailer.context_processors.display_version"
    )

    LOGIN_REDIRECT_URL = '/'
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

    SOUTH_DATABASE_ADAPTERS = {'default': 'south.db.postgresql_psycopg2'}


class Dev(Common):
    """
    The in-development settings and the default configuration.
    """

    THIRD_PARTY_APPS = Common.THIRD_PARTY_APPS + (
        'debug_toolbar',
    )

    INSTALLED_APPS = Common.BASE_APPS + THIRD_PARTY_APPS + Common.LOCAL_APPS

    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )


class Prod(Common):
    """
    The in-production settings.
    """
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    ALLOWED_HOSTS = ['*']
    SECRET_KEY = values.SecretValue()

