"""
Base settings to build other settings files upon.
"""

import logging
import os
import environ
from language_acts.twitterhut.settings import *  # noqa

LOGIN_URL = '/wagtail/login/'


ROOT_DIR = (
    environ.Path(__file__) - 3
)  # (language_acts/config/settings/base.py - 3 = language_acts/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
COMPOSE_DIR = os.path.join(BASE_DIR, "compose")

APPS_DIR = ROOT_DIR.path("language_acts")

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-gb"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [ROOT_DIR.path("locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'modelcluster',
    'rest_framework',
    'sekizai',
    'taggit',
    'wagtail.core',
    'wagtail.admin',
    'wagtail.documents',
    'wagtail.snippets',
    'wagtail.users',
    'wagtail.images',
    'wagtail.embeds',
    'wagtail.search',
    'wagtail.contrib.redirects',
    'wagtail.contrib.forms',
    'wagtail.sites',
    'wagtail.api',
    'wagtail.contrib.routable_page',
    'wagtail.contrib.table_block',
    'django_elasticsearch_dsl'
]

LOCAL_APPS = [
    # "language_acts.users.apps.UsersConfig",
    "language_acts.cms.apps.CmsConfig",
    # 'kdl_ldap',
    'language_acts.twitterhut.apps.TwitterhutConfig',
    # 'activecollab_digger',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
# MIGRATION_MODULES = {"sites": "language_acts.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
# AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
# LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = '/wagtail/login/'

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using
    # -argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
                ".UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation"
                ".CommonPasswordValidator"},
    {
        "NAME": "django.contrib.auth.password_validation"
                ".NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATICFILES_STORAGE = \
    "language_acts.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = str(ROOT_DIR("staticfiles"))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting
# -STATICFILES_DIRS
# os.path.join(ROOT_DIR, 'node_modules')
STATICFILES_DIRS = [
    str(APPS_DIR.path("static")),
    str(ROOT_DIR.path("node_modules")),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles
# -finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR("media"))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting
        # -TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template
            # -loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api
            # /#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template
            # -context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "sekizai.context_processors.sekizai",
                "django.contrib.messages.context_processors.messages",
                "language_acts.utils.context_processors.settings_context",
            ],
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
# FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template
# -packs
# CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = env(
#     "DJANGO_EMAIL_BACKEND",
#     default="django.core.mail.backends.smtp.EmailBackend"
# )
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-timeout
# EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""King's Digital Lab""", "kdl-info@kcl.ac.uk")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING

LOGGING_LEVEL = logging.WARN

# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    # 'loggers': {
    #     'django': {
    #         'handlers': ['file'],
    #         'level': LOGGING_LEVEL,
    #         'propagate': True
    #     },
    #     'elasticsearch': {
    #         'handlers': ['file'],
    #         'level': LOGGING_LEVEL,
    #         'propagate': True
    #     },
    # },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]
# -----------------------------------------------------------------------------
# Django Compressor
# http://django-compressor.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

COMPRESS_CSS_FILTERS = [
    # CSS minimizer
    'compressor.filters.cssmin.CSSMinFilter'
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# Wagtail
# ------------------------------------------------------------------------------
# https://docs.wagtail.io/en/v2.7.1/getting_started/integrating_into_django
# .html
WAGTAIL_SITE_NAME = "Language Acts and Worldmaking"
ITEMS_PER_PAGE = 10

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.elasticsearch7',
        'URLS': ["http://elasticsearch:9200"],
        'INDEX': 'owri_wagtail',
    }
}

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
    },
    'carousel': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': ['bold', 'italic', 'colour', 'reference']
        }
    },
    'bibliography': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': ['bold', 'italic', 'colour', 'link']
        }
    }
}

WAGTAIL_FRONTEND_LOGIN_TEMPLATE = 'language_acts/cms/login.html'
WAGTAILSEARCH_RESULTS_TEMPLATE = 'cms/search_results_page.html'

# Your stuff...
# ------------------------------------------------------------------------------

# Elasticsearch
# ------------------------------------------------------------------------------
# https://github.com/django-es/django-elasticsearch-dsl
ELASTICSEARCH_DSL = {"default": {"hosts": "elasticsearch:9200"}}


# -----------------------------------------------------------------------------
# Twitter
# -----------------------------------------------------------------------------

TWITTER_SCREEN_NAME = 'languageacts'

""" Put api keys or other protected settings in local_protected.py
    They will be imported if present"""
try:
    from .local_protected import (
        TWITTERHUT_TWITTER_API_KEY, TWITTERHUT_TWITTER_API_SECRET,
        TWITTERHUT_TWITTER_ACCESS_TOKEN,
        TWITTERHUT_TWITTER_ACCESS_TOKEN_SECRET, PRODUCTION_GA_ID
    )
    TWITTER_API_KEY = TWITTERHUT_TWITTER_API_KEY
    TWITTER_API_SECRET = TWITTERHUT_TWITTER_API_SECRET
    TWITTER_ACCESS_TOKEN = TWITTERHUT_TWITTER_ACCESS_TOKEN
    TWITTER_ACCESS_TOKEN_SECRET = TWITTERHUT_TWITTER_ACCESS_TOKEN_SECRET
    GA_ID = PRODUCTION_GA_ID
except ImportError:
    TWITTER_API_KEY = ''
    TWITTER_API_SECRET = ''
    TWITTER_ACCESS_TOKEN = ''
    TWITTER_ACCESS_TOKEN_SECRET = ''
    GA_ID = ''

# Run data migrations
# False by default so that clean builds and tests won't fail
RUN_DATA_MIGRATIONS = False

# -----------------------------------------------------------------------------
# Bibliographic References
# -----------------------------------------------------------------------------

# Add with the key "app, model" for each reference model snippet
# The value is the bibliography page model: "app, model"
# the page link will be derived from the page linked to the selected snippet
REFERENCE_MODEL = {
    "cms, BibliographyEntry": "cms.BibliographyPage",
    "cms, GlossaryTerm": "cms.GlossaryPage"
}
