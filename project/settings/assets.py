# all things concerning paths/assets/discovery

import os
from .base import PROJECT_PATH


COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "public", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "public", "static")

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# COMPRESS_CSS_FILTERS = [
#    'compressor.filters.css_default.CssAbsoluteFilter',  # default
#    'compressor.filters.cssmin.CSSMinFilter',  # pip install cssmin
# ]

FILER_PAGINATE_BY = 200
FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = True

FILER_STORAGES = {
    "public": {
        "main": {
            "UPLOAD_TO": (
                "filer_addons.filer_utils.generate_folder_and_filename.very_short_uuid4"
            ),
            "UPLOAD_TO_PREFIX": "files",
        },
        "thumbnails": {
            "THUMBNAIL_OPTIONS": {"base_dir": "thumbs"},
        },
    },
    "private": {
        "main": {
            "UPLOAD_TO": (
                "filer_addons.filer_utils.generate_folder_and_filename.very_short_uuid4"
            ),
        }
    },
}

THUMBNAIL_CACHE_DIMENSIONS = True
THUMBNAIL_EXTENSION = "webp"
THUMBNAIL_TRANSPARENCY_EXTENSION = "webp"
THUMBNAIL_PRESERVE_EXTENSIONS = ("svg",)
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    # 'easy_thumbnails.processors.scale_and_crop',
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

THUMBNAIL_OPTIMIZE_COMMAND = {
    "png": "/usr/bin/optipng {filename}",
    "gif": "/usr/bin/optipng {filename}",
    "jpeg": "/usr/bin/jpegoptim {filename}",
}
