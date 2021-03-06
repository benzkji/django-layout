from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings

from django.contrib import admin


# maybe use i18npatterns?!
urlpatterns = [
    # path('robots.txt', RobotsView.as_view())
    # url(r'', include('{{ project_name }}.urls')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]


urlpatterns = urlpatterns + i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^', include('cms.urls')),
)


if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
