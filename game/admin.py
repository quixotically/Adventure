from django.contrib import admin

# Register your models here.
from .models import Situation, Choice

admin.site.register(Situation)
admin.site.register(Choice)
