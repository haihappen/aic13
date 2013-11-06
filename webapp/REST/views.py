from models import Company
from models import SentimentAnalysis
from models import Paragraph

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist

from scraper import scrap_yahoo
from scraper import create_tasks

from JSONSerializer import JSONSerializer
from reportlab.platypus.para import Para

import urllib2

def sentiments(request):
    if request.method == 'GET':
        serializer = JSONSerializer()
        data = serializer.serialize(SentimentAnalysis.objects.all())
        return HttpResponse(data, content_type="application/json")

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def company(request):
    if request.method == 'GET':
        serializer = JSONSerializer()
        data = serializer.serialize(Company.objects.all())
        return HttpResponse(data, content_type="application/json")
    else:  # POST Request
        name = request.POST.get('name', '')
        company_instance = Company.objects.create(name=name)
        company_instance.save()
        # Upload tasks for this company
        messages.success(request, 'Sucessfully created company')
        return HttpResponseRedirect('/')
    
def new_company(request):
    if request.method == 'GET':
        return render_to_response('company/new.html', context_instance=RequestContext(request))
    
def parse_yahoo(request):
    # activate parser
    # Paragraph.objects.all().delete()
    try:
        latest = Paragraph.objects.latest("pub_date")
    except ObjectDoesNotExist:
        latest = None
    
    paragraphs = scrap_yahoo(latest)        
    
    for p in paragraphs:
        p.save()
    messages.success(request, 'Sucessfully parsed Yahoo!')
    
    count = Paragraph.objects.count()
    print("nr of paragraphs in db: %d" % count)
    

    for x in create_tasks("apple", None):
        print("-----------")
        print(x.text)
        print(x.yahoo_id)    
        print(x.pub_date)


    return render_to_response('index.html', context_instance=RequestContext(request))

def upload_tasks(request):
    # upload tasks to our Crowdsourcing platform
    url = "http://localhost:8000/api/tasks/"
    header = {'Content-type': 'application/json'}
    data = '{"title":"Test Question from python!","content":"yay this is a task","possible_answers":["a","b","c","d"],"price":23.42,"callback":"http://localhost:8001/callback/","answers_wanted":5}'
    req = urllib2.Request(url, data, header)
    base64string = base64.encodestring('%s:%s' % ("aic_c1", "aic")).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(req)
    answer = response.read()
    print answer
    messages.success(request, 'Sucessfully uploaded Tasks')
    return render_to_response('index.html', context_instance=RequestContext(request))

