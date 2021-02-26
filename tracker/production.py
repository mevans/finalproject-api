from .settings import *

DEBUG = False

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MIDDLEWARE = MIDDLEWARE + [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

print('here')
