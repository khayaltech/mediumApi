from .base import *  # noqa
from .base import env  # noqa

DEBUG = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="VoQE5G62Qu1Sk8cmBMa8V8D4nYhWazjaEoH9p9wWGPF4Pv23A3M68Wtme2BpHSwt",
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]


# SECRET_KEY = 'django-insecure-uz(cebeajnd7jekvt(hh*s-xbs9=a0mds))r+0)5g@!4*7(7i@'
CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]



EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_USE_TLS = True
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = "khayalfarajov@gmail.com"
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DOMAIN = env("DOMAIN")
SITE_NAME = "Medium Api"
DEFAULT_FROM_EMAIL = "khayalfarajov@gmail.com"
