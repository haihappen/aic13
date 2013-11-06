from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    possible_answers = models.TextField(null=True) # JSON-serialized (text) version of your possible answers
    price = models.DecimalField(max_digits=4,decimal_places=2)
    callback = models.URLField()
    answers_wanted = models.IntegerField()
    
class Answer(models.Model):
    task = models.ForeignKey(Task)
    user = models.ForeignKey(User)
    answer = models.TextField()
    
class Companyuser(models.Model):
    user = models.ForeignKey(User,unique=True)