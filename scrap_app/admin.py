from django.contrib import admin
from .models import City, Language, Vacantion, Error

admin.site.register(City)
admin.site.register(Language)
admin.site.register(Vacantion)
admin.site.register(Error)
