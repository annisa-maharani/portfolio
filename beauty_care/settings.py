from decouple import config
from os.path import join, abspath, dirname

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = dirname(dirname(abspath(__file__)))
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"

SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
""" set debug to false in .env file """
# DEBUG = bool(int(config('DEBUG')))
DEBUG = True

ALLOWED_HOSTS = ['*']
X_FRAME_OPTIONS = 'SAMEORIGIN'

""" uncomment this section when you want to make it online """
CORS_REPLACE_HTTPS_REFERER = False
HOST_SCHEME = "http://"
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = None
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_FRAME_DENY = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False
SESSION_COOKIE_HTTPONLY = False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    'beauty',
    'backend',
    'api',
    'ckeditor',
    'crispy_forms',
    'robots',
    'rest_framework',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

ROBOTS_USE_SCHEME_IN_HOST = True
ROBOTS_USE_SITEMAP = True
ROBOTS_SITEMAP_URLS = {
    '/sitemap.xml'
}
ROBOTS_SITEMAP_VIEW_NAME = 'sitemap'
ROBOTS_CACHE_TIMEOUT = 60 * 60 * 24

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = int(config('SITE_ID'))

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'beauty_care.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(BASE_DIR, 'templates'), join(BASE_DIR, 'templates', 'allauth')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = config('WSGI_APPLICATION')

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, 'db.sqlite3')
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [join(BASE_DIR, 'static')]
STATIC_ROOT = join(BASE_DIR, 'static/root')

MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/wpcp-admin/'
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login"
ACCOUNT_SIGNUP_REDIRECT_URL = '/accounts/login/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 60 * 12

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': '100%',
    },
    'special': {
        'width': 'fit-content',
        'toolbar': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'AlignLeft', 'Subscript', 'Superscript', ],
            ['Source']
        ],
    },
    'comment': {
        'width': 'fit-content',
        'toolbar': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'AlignLeft', ],
            # ['NumberedList', 'BulletedList', ],
            # ['Indent', 'Outdent', 'Blockquote', ],
            # ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', 'BidiLtr', 'BidiRtl', ],
            ['Font', 'FontSize'],
            ['Source']
        ],
        # 'toolbar': 'basic'
    },
}
