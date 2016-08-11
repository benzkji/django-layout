from django.contrib import admin


from .models import My


class MyAdmin(admin.ModelAdmin):
    pass

admin.site.register(My, MyAdmin)