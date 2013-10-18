from django.db import models

# Create your models here.
class SentimentAnalysis(models.Model):
    company = models.CharField(max_length=30)
    sentiment = models.IntegerField()
