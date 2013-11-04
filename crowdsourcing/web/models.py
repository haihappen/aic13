from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    possible_answers = models.TextField(null=True) # JSON-serialized (text) version of your possible answers
    price = models.DecimalField(max_digits=4,decimal_places=2)
    callback = models.URLField()
    
