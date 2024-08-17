from django.db import models
from django.contrib.auth.models import User


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
    AnnotatorID = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0)
