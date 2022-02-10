from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Application definition

INSTALLED_APPS = [
    'log.apps.LogConfig',
    'secure.apps.SecureConfig',
    'config.apps.ConfigConfig',
    'user.apps.UserConfig',
    'doc.apps.DocConfig',
    'error500.apps.Error500Config',
    'faq.apps.FaqConfig',
    'language.apps.LanguageConfig',
    'country.apps.CountryConfig',
    'nationality.apps.NationalityConfig',
    'visa.visa.apps.VisaConfig',
    'visa.field.apps.FieldConfig',
    'visa.document.apps.DocumentConfig',
    'visa.kind.apps.KindConfig',
    'visa.person_number.apps.PersonNumberConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'main.wsgi.application'

AUTH_USER_MODEL = 'user.User'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ulaanbaatar'

USE_I18N = True

USE_L10N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'static'

SESSION_COOKIE_NAME = 'evisa-intl'
CSRF_FAILURE_VIEW = 'secure.views.csrf_failure'


GENERATE_VISA_PERSON_NUMBER_TIMEOUT = 6
GENERATE_VISA_PERSON_NUMBER_BATCH_SIZE = 900


DATA_UPLOAD_MAX_MEMORY_SIZE = 50000000
PORTRAIT_MAX_UPLOAD_SIZE = 250000
DOCUMENT_MAX_UPLOAD_SIZE = 1600000


MEDIA_URL = '/uploads/'
MEDIA_ROOT = BASE_DIR.parent / 'uploads'
