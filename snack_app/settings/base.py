import json

from django.core.exceptions import ImproperlyConfigured
from unipath import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).ancestor(3)

with open("secret.json") as f:
    secret = json.loads(f.read())


def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "la variable %s no existe" % secret_name
        raise ImproperlyConfigured(msg)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
)

LOCAL_APPS = (
    'applications.users',
    'applications.home',
    'applications.events',
    'applications.orders',
    'applications.products',
    'applications.payments'
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'ckeditor',
    'ckeditor_uploader',
    'knox',
    'corsheaders',
    'mercadopago',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'knox.auth.TokenAuthentication',
    ]
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'social_django.middleware.SocialAuthExceptionMiddleware',  # <-- Here
]


#ALLOWED_HOSTS = ['*']
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8080',
    'http://127.0.0.1:8000'
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'snack_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'social_django.context_processors.backends',  # <-- Here
                # 'social_django.context_processors.login_redirect',  # <-- Here
            ],
        },
    },
]

WSGI_APPLICATION = 'snack_app.wsgi.application'


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

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.facebook.FacebookOAuth2',
    # 'social_core.backends.twitter.TwitterOAuth',
    # 'social_core.backends.github.GithubOAuth2',
    # 'social_core.backends.open_id.OpenIdAuth',
    # 'social_core.backends.google.GoogleOpenId',
    # 'social_core.backends.google.GoogleOAuth2',
    # 'social_core.backends.google.GoogleOAuth',
    # 'social_core.backends.twitter.TwitterOAuth',
    # 'social_core.backends.yahoo.YahooOpenId',
    # 'social_core.backends.apple.AppleIdAuth',
    # 'users.backends.AppleIdAppAuth',
    # 'users.backends.AppleIdWebAuth',

    'django.contrib.auth.backends.ModelBackend',

)


# SOCIAL_AUTH_FACEBOOK_KEY = '209813464447923'  # App ID
# SOCIAL_AUTH_FACEBOOK_SECRET = '90664640d2a5c6f282d73ea3e7d3cbf1'  # App Secret
#SOCIAL_AUTH_POSTGRES_JSONFIELD = True
