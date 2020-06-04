from django.conf import settings


def general_contextor(request):
    context = {}
    if getattr(settings, 'GOOGLE_ANALYTICS_UA', None):
        context['analytics_ua'] = settings.GOOGLE_ANALYTICS_UA
    return context
