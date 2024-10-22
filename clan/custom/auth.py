import os

SESSION_COOKIE_NAME = 'session_key'
SESSION_COOKIE_AGE = 3600
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
]

GUARDIAN_GET_CONTENT_TYPE = 'polymorphic.contrib.guardian.get_polymorphic_base_content_type'

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

EMAIL_HOST=os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER=os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL=os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_USE_TLS=True
EMAIL_PORT = os.environ.get('EMAIL_PORT')
