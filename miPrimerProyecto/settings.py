from pathlib import Path

# Construir rutas dentro del proyecto como BASE_DIR / 'subcarpeta'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración rápida para desarrollo: no apta para producción
SECRET_KEY = 'django-insecure-faq=fx0cu+4wlhb4l(7_)uldljxi&yx3h-d-%a3*^sei8nmop8'
DEBUG = True
ALLOWED_HOSTS = []

# Definición de aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'anuncios',
    'django.contrib.sites',  # Necesario para django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'channels',
    'corsheaders',  # Añadido para gestionar CORS
]

SITE_ID = 1  # Configuración para django.contrib.sites

MIDDLEWARE = [
    # Middleware de CORS (debe estar al inicio)
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'miPrimerProyecto.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Carpeta para plantillas HTML
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Necesario para django-allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'miPrimerProyecto.wsgi.application'
ASGI_APPLICATION = 'miPrimerProyecto.asgi.application'

# Configuración de base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validación de contraseñas
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

# Configuración de internacionalización
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos estáticos y multimedia
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración para OAuth2 con Google y Facebook
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['email', 'profile'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email'],
        'FIELDS': ['email', 'name'],
        'VERIFIED_EMAIL': False,
    },
}

# Claves para autenticación social
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '293982673470-iaocmec1g2v64ml9k6iulqm2vgnuejh5.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

SOCIAL_AUTH_FACEBOOK_KEY = 'TU_FACEBOOK_APP_ID'
SOCIAL_AUTH_FACEBOOK_SECRET = 'TU_FACEBOOK_SECRET'

# Configuración del correo para desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Redirección después del inicio y cierre de sesión
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# Configuración de CORS para React
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Dirección del servidor React
]
CORS_ALLOW_CREDENTIALS = True

# Configuración de Django Channels con Redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("172.17.0.2", 6379)],
            "capacity": 15000,  # Aumenta la capacidad de mensajes pendientes
            "expiry": 120,  # Incrementa el tiempo de espera antes de cerrar conexiones inactivas
        },
    },
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "channels": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
