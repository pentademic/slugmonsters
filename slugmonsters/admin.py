from django.contrib import admin

# Register your models here.
from .models import Slug
from .models import Equipement

admin.site.register(Slug)
admin.site.register(Equipement)