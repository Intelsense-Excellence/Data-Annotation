from django.db import models


# Create your models here.

class DataAnnotation(models.Model):
    audio = models.FileField(upload_to='audio')
    transcript = models.TextField(blank=True)


class Annotator(models.Model):
    AnnotatorID = models.CharField(max_length=100, primary_key=True,unique=True)
    name = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0)
