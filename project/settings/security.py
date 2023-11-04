# AXES: https://django-axes.readthedocs.io/en/latest/4_configuration.html
AXES_FAILURE_LIMIT = 20  # high value, still protects
AXES_LOCKOUT_PARAMETERS = [
    ["username", "ip_address"],
]  # ip AND username
AXES_COOLOFF_TIME = 12  # COOL down after 12 hours
AXES_RESET_ON_SUCCESS = True
AXES_IPWARE_META_PRECEDENCE_ORDER = [
    "HTTP_X_FORWARDED_FOR",
    "REMOTE_ADDR",
]

AUTHENTICATION_BACKENDS = [
    # AxesBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    "axes.backends.AxesBackend",
    # Django ModelBackend is the default authentication backend.
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# strict transport security, only sent when https
# > no going back, know what you do!
# SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_CONTENT_TYPE_NOSNIFF = True

# some basic cookie security
if not DEBUG:  # noqa
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
CRSF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "SAMEORIGIN"
