from django.conf import settings


def general_contextor(request):
    context = {}
    context["webpack_static"] = "{{ project_name }}/dist/"
    if settings.DEBUG:
        context["webpack_static"] = "{{ project_name }}/dev/"
    if getattr(settings, "GOOGLE_ANALYTICS_UA", None):
        context["analytics_ua"] = settings.GOOGLE_ANALYTICS_UA
    return context
