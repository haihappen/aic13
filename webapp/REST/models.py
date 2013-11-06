from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=30)

class SentimentAnalysisType(models.Model):
    name = models.CharField(max_length=30)

class SentimentAnalysis(models.Model):
    company = models.ForeignKey(Company)
    type = models.ForeignKey(SentimentAnalysisType)
    sentiment = models.IntegerField()

class Paragraph(models.Model):
    pub_date = models.DateTimeField()
    yahoo_id = models.TextField()
    text = models.TextField()

class Task(models.Model):
    submitted = models.DateTimeField()
    company = models.ForeignKey(Company)
    paragraph = models.ForeignKey(Paragraph)
    crowdsourcing_id = models.IntegerField()

class Answer(models.Model):
    task = models.ForeignKey(Task)
    user = models.IntegerField()
    answer = models.TextField()
