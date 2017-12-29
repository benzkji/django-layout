from django.contrib import admin

from .models import My


class MyAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', )


admin.site.register(My, MyAdmin)
