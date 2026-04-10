"""
Django Production Settings for Smart Locker System
Import base settings and override for production
"""

from .settings import *
import environ
import os

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Database (from environment)
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

# Redis Cache (Production)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://127.0.0.1:6380/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'PASSWORD': env('REDIS_PASSWORD', default=None),
        },
        'TIMEOUT': 60,
    }
}

# Elastic APM - Production Configuration
ELASTIC_APM = {
    'SERVICE_NAME': env('ELASTIC_APM_SERVICE_NAME', default='smart-locker-system'),
    'SERVER_URL': env('ELASTIC_APM_SERVER_URL', default='http://localhost:8200'),
    'SECRET_TOKEN': env('ELASTIC_APM_SECRET_TOKEN', default=''),
    'ENVIRONMENT': env('ELASTIC_APM_ENVIRONMENT', default='production'),
    'DEBUG': False,  # Always False in production
    
    # Performance settings
    'TRANSACTION_SAMPLE_RATE': 0.5,  # Sample 50% of transactions
    'CAPTURE_BODY': 'errors',  # Only capture body on errors
    'CAPTURE_HEADERS': False,  # Don't capture headers for privacy
    
    # Security
    'SERVER_TIMEOUT': 10,  # 10 second timeout
    
    # Logging integration
    'LOG_LEVEL': env('LOG_LEVEL', default='WARNING'),
    'AUTO_LOG_STACKS': True,
}

# Security Settings (Production)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging - Production (JSON format for ELK)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'fmt': '%(asctime)s %(levelname)s %(name)s %(module)s %(message)s %(pathname)s %(lineno)d',
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'json',  # JSON for production
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': env('LOG_DIR', default='/var/log/locker-system') + '/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'json',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': env('LOG_DIR', default='/var/log/locker-system') + '/error.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10,
            'formatter': 'json',
        },
        'elastic_apm': {
            'level': 'ERROR',
            'class': 'elasticapm.handlers.logbook.LoggingHandler',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'accounts': {
            'handlers': ['console', 'file', 'error_file', 'elastic_apm'],
            'level': 'INFO',
            'propagate': False,
        },
        'lockers': {
            'handlers': ['console', 'file', 'error_file', 'elastic_apm'],
            'level': 'INFO',
            'propagate': False,
        },
        'reservations': {
            'handlers': ['console', 'file', 'error_file', 'elastic_apm'],
            'level': 'INFO',
            'propagate': False,
        },
        'elasticapm': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Static Files (Production)
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Media Files (Use S3 or similar in production)
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Email Configuration (Production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')

# Performance
CONN_MAX_AGE = 60  # Database connection persistence
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Rate Limiting (Optional - install django-ratelimit)
# Install: pip install django-ratelimit
# Add 'ratelimit' to INSTALLED_APPS
