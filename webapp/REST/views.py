from models import Company
from models import SentimentAnalysis
from models import Paragraph
from models import Task
from models import Answer

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist

from scraper import scrap_yahoo
from scraper import get_paragraphs

from JSONSerializer import JSONSerializer
from reportlab.platypus.para import Para
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt

import urllib2
import base64
import json

#Helper functions
def create_tasks(company):
    try:
        latest_timestamp = company.task_set.latest("pub_date")
    except ObjectDoesNotExist:
        latest_timestamp = None

    paragraphs = get_paragraphs(company.name,latest_timestamp)
    current_timestamp = datetime.now()
    #TODO: create tasks for paragraphs & upload them to our plattform
    crowdsourcing_id = 0 #this will be returned by the CrowdSouricng Webapp
    task = Task.objects.create(submitted=current_timestamp,company=company,paragraph=paragraphs[0],crowdsourcing_id=crowdsourcing_id)


def create_task_json(title,content,possible_answers,price,callback,answers_wanted):
    answers_json = json.dumps(possible_answers)
    task_json = '{"title":"%s","content":"%s","possible_answers":%s,"price":%d,"callback":"%s","answers_wanted":%i}' % (title,content,answers_json,price,callback,answers_wanted)
    return task_json

def upload_task(task_json):
    #BEGIN TODO: move to settings
    user = "aic_c1"
    password = "aic"
    url = "http://localhost:8000/api/tasks/"
    #END
    header = {'Content-type': 'application/json'}
    data = task_json
    req = urllib2.Request(url, data, header)
    base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(req)
    answer_json = response.read()
    answer = json.loads(answer_json)
    return answer

#Webapp functions
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

    return render_to_response('index.html', context_instance=RequestContext(request))

def upload_all_tasks(request):
    # upload tasks to our Crowdsourcing platform
    for company in Company.objects.all():
        create_tasks(company)
    messages.success(request, 'Sucessfully uploaded Tasks')
    return render_to_response('index.html', context_instance=RequestContext(request))

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        answers = json.loads(request.body,"ascii")
        #[{u'answer': u'a', u'task': 1, u'user': 1}, {u'answer': u'c', u'task': 1, ...]
        for answer in answers:
            task = Task.objects.get(id=answer["task"])
            Answer.objects.create(task=task,user=answer["user"],answer=answer["answer"])
        return HttpResponse('ok')
