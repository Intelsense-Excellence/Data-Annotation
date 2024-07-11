from django.db import models


# Create your models here.
# AnnotatorId
# BadAudio

class DataAnnotation(models.Model):
    # audio = models.FileField(upload_to='audio')
    audio = models.CharField(max_length=255)
    transcript = models.TextField(blank=True)
    annotatorId = models.CharField(max_length=100, blank=True, null=True)
    badAudio = models.BooleanField(default=False)
    isAnnotated = models.BooleanField(default=False)


class Annotator(models.Model):
    AnnotatorID = models.CharField(max_length=100, primary_key=True, unique=True)
    name = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0)
