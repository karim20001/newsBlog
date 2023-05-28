from django.contrib import admin
from weblog import models

admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Tag)
admin.site.register(models.Post)
