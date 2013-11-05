from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=30)

class SentimentAnalysis(models.Model):
    company = models.CharField(max_length=30)
    sentiment = models.IntegerField()

class Paragraph(models.Model):
    pub_date = models.DateTimeField()
    yahoo_id = models.TextField()
    text = models.TextField()
