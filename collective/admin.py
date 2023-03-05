from django.contrib import admin
from . import models

admin.site.register(models.Collective)
admin.site.register(models.Membership)
admin.site.register(models.UserGroup)
