from django.contrib import admin

# Register your models here.
from .models import DataAnnotation,Annotator

admin.site.register(DataAnnotation)
admin.site.register(Annotator)