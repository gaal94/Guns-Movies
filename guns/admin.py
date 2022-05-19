from django.contrib import admin
from .models import GunType, Gun

admin.site.register(GunType)
admin.site.register(Gun)