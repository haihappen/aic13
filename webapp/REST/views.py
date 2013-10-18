from models import SentimentAnalysis

from random import randint #only needed for test

from django.http import HttpResponse
from JSONSerializer import JSONSerializer

def sentiments(request):
    if request.method == 'GET':
        serializer = JSONSerializer()
        data = serializer.serialize(SentimentAnalysis.objects.all())
        return HttpResponse(data, content_type="application/json")

def add_company(request, company_name):
    sentiment_val = randint(0, 100) #just a test
    sentiment_instance = SentimentAnalysis.objects.create(company=company_name,sentiment=sentiment_val)
    sentiment_instance.save()
    return HttpResponse("Added company %s for sentiment analysation." % company_name, content_type="text/plain")