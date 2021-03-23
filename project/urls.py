from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.urls import path
from django.contrib import admin


# maybe use i18npatterns?!
urlpatterns = [
    # path('robots.txt', RobotsView.as_view())
    # path('', include('{{ project_name }}.urls')),
    # path('admin/doc/', include('django.contrib.admindocs.urls')),
]


urlpatterns = urlpatterns + i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('cms.urls')),
)


if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
